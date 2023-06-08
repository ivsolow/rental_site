import datetime
from equipment.tests import equipment_1, equipment_2
from cart.models import Cart
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from equipment.models import Equipment, Category
from rentals.models import Rentals
from users.models import CustomUser


@pytest.fixture
def user():
    # Создание пользователя
    user = CustomUser.objects.create_user(
        id=1,
        email='testuser',
        password='testpassword123_'
    )
    return user


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def cart_create(api_client, equipment_1):
    url = reverse('add_cart')
    data = {
        'equipment': equipment_1.id,
        'amount': 3,
        'date_start': '2023-05-20',
        'date_end': '2023-05-22'
    }
    response = api_client.post(url, data)
    return response


@pytest.fixture
def cart_create_2(api_client, equipment_2):
    url = reverse('add_cart')
    data = {
        'equipment': equipment_2.id,
        'amount': 1,
        'date_start': '2023-05-25',
        'date_end': '2023-05-28'
    }
    response = api_client.post(url, data)
    return response


@pytest.mark.django_db
def test_list_cart_items(api_client):
    """
    Проверка полей пустой корзины
    """
    # Отправляем GET-запрос на получение списка позиций корзины
    url = reverse('cart')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Проверяем структуру и данные возвращаемого ответа
    assert 'cart_items' in response.data
    assert 'total_positions' in response.data
    assert 'total_summ' in response.data

    cart_items = response.data['cart_items']
    assert isinstance(cart_items, list)

    # Проверяем, что список позиций корзины пустой
    assert len(cart_items) == 0

    # Проверяем структуру и данные каждой позиции корзины
    for item in cart_items:
        assert 'id' in item
        assert 'equipment' in item
        assert 'amount' in item
        assert 'summ' in item
        assert 'dates' in item

        assert 'name' in item['equipment']
        assert 'category' in item['equipment']
        assert 'description' in item['equipment']
        assert 'price' in item['equipment']
        assert 'photo' in item['equipment']

        assert 'date_start' in item['dates']
        assert 'date_end' in item['dates']


@pytest.mark.django_db
def test_create_cart_item(cart_create, equipment_1):
    """
    Создание 1 объекта корзины и проверка полей
    """
    response = cart_create
    # Проверяем, что запрос завершился успешно (статус 201 Created)
    assert response.status_code == status.HTTP_201_CREATED

    # Проверяем структуру и данные возвращаемого ответа
    assert 'id' in response.data
    assert 'equipment' in response.data
    assert 'amount' in response.data
    # assert 'summ' in response.data
    assert 'date_start' in response.data
    assert 'date_end' in response.data

    equipment_id = response.data['equipment']
    created_equipment = Equipment.objects.get(id=equipment_id)
    assert created_equipment.name == equipment_1.name
    assert response.data['amount'] == 3
    assert response.data['date_start'] == '2023-05-20'
    assert response.data['date_end'] == '2023-05-22'


@pytest.mark.django_db
def test_add_cart_same_instance(api_client, cart_create, equipment_1):
    """
    Проверка на добавление количества к тому же объекту корзину
    присовпадении дат и и названия снаряжения
    """
    cart_instance = cart_create
    post_url = reverse('add_cart')
    get_url = reverse('cart')
    get_response_before_adding = api_client.get(get_url)
    data = {
        'equipment': equipment_1.id,
        'amount': 4,
        'date_start': '2023-05-20',
        'date_end': '2023-05-22'
    }
    post_response = api_client.post(post_url, data)
    get_response_after_adding = api_client.get(get_url)

    assert get_response_before_adding.data['cart_items'][0]['amount'] == 3
    assert get_response_after_adding.data['cart_items'][0]['amount'] == 7


@pytest.mark.django_db
def test_add_cart_different_instances(api_client, cart_create, equipment_1, equipment_2):
    """
    Проверка на добавление количества к разным объектам корзины
    при несовпадении дат и/или названия снаряжения
    """
    cart_instance = cart_create
    post_url = reverse('add_cart')
    get_url = reverse('cart')
    data_diff_date = {
        'equipment': equipment_1.id,
        'amount': 4,
        'date_start': '2023-05-20',
        'date_end': '2023-05-25'  # different date
    }
    data_diff_equipment = {
        'equipment': equipment_2.id,
        'amount': 1,
        'date_start': '2023-05-20',
        'date_end': '2023-05-25'  # different equipment
    }

    post_request = api_client.post(post_url, data_diff_date)
    post_request = api_client.post(post_url, data_diff_equipment)
    result = api_client.get(get_url)
    assert result.data['cart_items'][0]['amount'] == 1
    assert result.data['cart_items'][1]['amount'] == 3
    assert result.data['cart_items'][2]['amount'] == 4


@pytest.mark.django_db
def test_cart_availability(equipment_1, equipment_2, api_client, user):
    """
    Проверка наличия в корзине снаряжения на выбранную дату
    """
    today = datetime.date.today()
    delta = datetime.timedelta(days=5)
    first_buy = Rentals.objects.create(
        user=user,
        equipment=equipment_1,
        amount=2,
        date_start=f'{today}',
        date_end=f'{today + delta}'
    )

    # проверка на прошедшее время
    get_url = reverse('dates-list') + f'?date_start=2023-05-29&date_end=2023-05-30'
    response = api_client.get(get_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # наличие в указанные даты
    get_url_1 = reverse('dates-list') + f'?date_start={today}&date_end={today + delta}'
    response = api_client.get(get_url_1)
    assert len(response.data) == 2
    print(response.data)
    assert response.data[0]['available_amount'] == 5
    assert response.data[1]['available_amount'] == 8

    # если в наличие 0 снаряжения, оно не отображается
    second_buy = Rentals.objects.create(
        user=user,
        equipment=equipment_2,
        amount=5,
        date_start=f'{today}',
        date_end=f'{today + delta}'
    )
    response = api_client.get(get_url_1)
    assert len(response.data) == 1
    assert response.data[0]['available_amount'] == 8

    # наличие в даты, которые пересекаются с занятой датой хотя бы в 1 день
    delta_1 = datetime.timedelta(days=5)
    delta_2 = datetime.timedelta(days=10)
    get_url_2 = reverse('dates-list') + f'?date_start={today + delta_1}&date_end={today + delta_2}'
    response = api_client.get(get_url_2)
    assert len(response.data) == 1
    assert response.data[0]['available_amount'] == 8

    # наличие в даты, когда всё свободно
    delta_3 = datetime.timedelta(days=6)
    delta_4 = datetime.timedelta(days=8)
    get_url_3 = reverse('dates-list') + f'?date_start={today + delta_3}&date_end={today + delta_4}'
    response = api_client.get(get_url_3)
    assert len(response.data) == 2
    print(response.data)
    assert response.data[0]['available_amount'] == 5
    assert response.data[1]['available_amount'] == 10
