import json

import requests
import pytest

from django.urls import reverse

from cart.models import Cart
from .cart_test import cart_create, cart_create_2  # noqa: F401
from payment.models import CreatedPayment, UserPaymentDetails
from rentals.models import Rentals
from .rentals_test import rental_create  # noqa: F401
from .equipment_test import (user,  # noqa: F401
                             api_client,
                             equipment_1,
                             equipment_2)


@pytest.fixture
def yookassa_response_create(api_client):  # noqa: F811
    url = reverse('payment')
    data = {
        "payment_sum": "500",
        "commission": "3.5"
    }
    response = api_client.post(url, data)  # noqa: F841

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
def test_check_empty_cart(api_client):  # noqa: F811
    url = reverse('cart_check')
    response = api_client.get(url)
    assert response.status_code == 400
    assert response.data['detail'] == 'Корзина пуста'


@pytest.mark.django_db
def test_check_cart_all_correct(api_client,  # noqa: F811
                                cart_create,  # noqa: F811
                                cart_create_2):  # noqa: F811

    url = reverse('cart_check')
    response = api_client.get(url)
    assert response.status_code == 302
    assert response.url == "/api/v1/payment/"


@pytest.mark.django_db
def test_check_cart_incorrect_amount(api_client,  # noqa: F811
                                     rental_create,  # noqa: F811
                                     cart_create,  # noqa: F811
                                     cart_create_2):  # noqa: F811
    url = reverse('cart_check')
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == 400
    assert response.data['params']['exceeding_amount'] == 3


@pytest.mark.django_db
def test_payment_api_view(api_client):  # noqa: F811
    # Подготовка данных для запроса
    url = reverse('payment')
    data = {
        "payment_sum": "500",
        "commission": "3.5"
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    yokassa_url = response.data['confirmation_url']
    assert 'https://yoomoney.ru/checkout/payments/v2/contract' in yokassa_url
    response_get = requests.get(yokassa_url)
    assert response_get.status_code == 200


@pytest.mark.django_db
def test_yokassa_successful_response(api_client,  # noqa: F811
                                     cart_create,  # noqa: F811
                                     cart_create_2,  # noqa: F811
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
    response_post = api_client.post(url,
                                    data=data,
                                    content_type='application/json')
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
    assert response_rentals.data[
               0]['equipment']['name'] == 'Giant Trance Advanced Pro'
    assert response_rentals.data[1]['amount'] == 3

    # проверяем запись данных платежа
    payment_details = (UserPaymentDetails.objects.
                       filter(idempotence_key=idempotence_key))
    assert len(payment_details) == 1
    assert payment_details.first().income_amount_value == 500


@pytest.mark.django_db
def test_yokassa_bad_response(api_client,  # noqa: F811
                              cart_create,  # noqa: F811
                              cart_create_2,  # noqa: F811
                              yookassa_response_create):
    # проверка некорректного idempotence_key
    yookassa_response = yookassa_response_create[0]
    idempot_key = 'b8b9364d-cbcf-4754-9183-20ad03397c00'
    yookassa_response['object']['metadata']['idempotence_key'] = idempot_key
    url = reverse('payment_response')
    data = json.dumps(yookassa_response)
    response_post = api_client.post(url,
                                    data=data,
                                    content_type='application/json')
    assert response_post.status_code == 400
