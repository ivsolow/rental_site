import json
from cart.models import Cart
from cart.tests import cart_create, cart_create_2, user, api_client, user
from equipment.tests import equipment_1, equipment_2
import requests
import pytest
from django.urls import reverse
from yookassa import Payment
from payment.models import CreatedPayment, UserPaymentDetails
from rentals.models import Rentals


@pytest.fixture
def rental_create(api_client, equipment_1, user):
    rental = Rentals.objects.create(
        equipment=equipment_1,
        user=user,
        amount=10,
        date_start='2023-05-20',
        date_end='2023-05-22'
    )
    return

@pytest.fixture
def yookassa_response_create(api_client):
    url = reverse('payment')
    data = {
        "total_summ": "500",
        "commission": "3.5"
    }
    response = api_client.post(url, data)

    idempotence_key = CreatedPayment.objects.first().idempotence_key
    yookassa_response = {
        'type': 'notification',
        'event': 'payment.succeeded',
        'object': {
            'id': '2c113bb2-000f-5000-8000-1aaa25238201',
            'status': 'succeeded',
            'amount': {
                'value': '518.13',
                'currency': 'RUB'
            },
            'income_amount':
                {
                    'value': '500.00',
                    'currency': 'RUB'
                },
            'description': 'Оплата 518.13 рублей, включая комиссию 3.5 %',
            'recipient':
                {
                    'account_id': '216213',
                    'gateway_id': '2082708'
                },
            'payment_method': {
                'type': 'bank_card',
                'id': '2c113bb2-000f-5000-8000-1aaa25238201',
                'saved': False,
                'title': 'Bank card *4444',
                'card': {
                    'first6': '555555',
                    'last4': '4444',
                    'expiry_year': '2025',
                    'expiry_month': '05',
                    'card_type': 'MasterCard',
                    'issuer_country': 'US'
                }
            },
            'captured_at': '2023-06-06T12:35:11.949Z',
            'created_at': '2023-06-06T12:34:58.191Z',
            'test': True, 'refunded_amount': {
                'value': '0.00',
                'currency': 'RUB'
            },
            'paid': True,
            'refundable': True,
            'metadata': {
                'user_id': '1',
                'idempotence_key': idempotence_key,
            },
            'authorization_details':
                {
                    'rrn': '321773340639081',
                    'auth_code': '624659',
                    'three_d_secure': {
                        'applied': False,
                        'method_completed': False,
                        'challenge_completed': False
                    }
                }
        }
    }
    return yookassa_response, idempotence_key


@pytest.mark.django_db
def test_check_empty_cart(api_client):
    url = reverse('cart_check')
    response = api_client.get(url)
    assert response.status_code == 400
    assert response.data == 'Корзина пуста'


@pytest.mark.django_db
def test_check_cart_all_correct(api_client, cart_create, cart_create_2):
    url = reverse('cart_check')
    response = api_client.get(url)
    assert response.status_code == 302
    assert response.url == "/api/v1/payment/"


@pytest.mark.django_db
def test_check_cart_uncorrect_amount(api_client, rental_create, cart_create, cart_create_2):
    url = reverse('cart_check')
    response = api_client.get(url)
    assert response.status_code == 400
    assert response.data['exceeding_amount'] == 3


@pytest.mark.django_db
def test_payment_api_view(api_client):
    # Подготовка данных для запроса
    url = reverse('payment')
    data = {
        "total_summ": "500",
        "commission": "3.5"
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert type(response.data) == str
    assert 'https://yoomoney.ru/checkout/payments/v2/contract' in response.data
    yokassa_url = response.data
    response_get = requests.get(yokassa_url)
    assert response_get.status_code == 200


@pytest.mark.django_db
def test_yokassa_successful_response(api_client,
                                     cart_create,
                                     cart_create_2,
                                     yookassa_response_create):
    yookassa_response, idempotence_key = yookassa_response_create

    # проверяем, что в корзине есть нужное нам снаряжение
    cart = Cart.objects.filter(user=1).order_by('equipment__name')
    assert cart[0].amount + cart[1].amount == 4
    assert cart[0].equipment.name == 'Giant Trance Advanced Pro'

    # проверяем, что у данного пользователя еще нет аренды
    rentals = Rentals.objects.filter(user=1)
    rentals_url = reverse('rentals-list')
    response_rentals = api_client.get(rentals_url)
    assert len(rentals) == 0
    assert len(response_rentals.data) == 0

    # получаем ответ от нашего сервера
    url = reverse('payment_response')
    data = json.dumps(yookassa_response)
    response_post = api_client.post(url, data=data, content_type='application/json')
    assert response_post.status_code == 200

    # проверяем, что корзина пустая
    assert len(cart) == 0
    url = reverse('cart')
    response_cart = api_client.get(url)
    assert response_cart.data.get('cart_item_data') == []

    # проверяем появившуюся аренду
    rentals = Rentals.objects.filter(user=1).order_by('equipment__name')
    assert len(rentals) == 2
    assert rentals[1].amount == 3
    rentals_url = reverse('rentals-list')
    response_rentals = api_client.get(rentals_url)
    assert len(response_rentals.data) == 2
    assert response_rentals.data[0]['equipment']['name'] == 'Giant Trance Advanced Pro'
    assert response_rentals.data[1]['amount'] == 3

    # проверяем запись данных платежа
    # idempotence_key = 'b8b9364d-cbcf-4754-9183-20ad03397c00'
    payment_details = UserPaymentDetails.objects.filter(idempotence_key=idempotence_key)
    assert len(payment_details) == 1
    assert payment_details.first().income_amount_value == 500


@pytest.mark.django_db
def test_yokassa_bad_response(api_client,
                              cart_create,
                              cart_create_2,
                              yookassa_response_create):
    # проверка некорректного idempotence_key
    yookassa_response = yookassa_response_create[0]
    yookassa_response['object']['metadata']['idempotence_key'] = 'b8b9364d-cbcf-4754-9183-20ad03397c00'
    url = reverse('payment_response')
    data = json.dumps(yookassa_response)
    response_post = api_client.post(url, data=data, content_type='application/json')
    assert response_post.status_code == 400
