import pytest
import datetime

from rest_framework import status
from django.urls import reverse

from equipment.models import Equipment, Category
from rest_framework.test import APIClient
from rentals.models import Rentals
from users.models import CustomUser


@pytest.fixture
def equipment_1():
    category = Category.objects.create(name='Hiking')
    equipment = Equipment.objects.create(
        id=1,
        name='Tent MSR Freelite 2',
        category=category,
        description='Good balance of weight & livability for solo hikers',
        price=1000,
        amount=10
    )
    return equipment


@pytest.fixture
def equipment_2():
    category = Category.objects.create(name='Bikes')
    equipment = Equipment.objects.create(
        id=2,
        name='Giant Trance Advanced Pro',
        category=category,
        description='best for enduro mountain bike',
        price=3000,
        amount=5
    )
    return equipment


@pytest.fixture
def equipment_3():
    category = Category.objects.create(name='Winter sports')
    equipment = Equipment.objects.create(
        id=3,
        name='Salomon XDR 80 TI',
        category=category,
        description='Ski provides excellent precision'
                    ' and stability when riding the slopes',
        price=1500,
        amount=8
    )
    return equipment


@pytest.fixture
def user():
    # Создание пользователя
    user = CustomUser.objects.create_user(
        id=1,
        email='test_user',
        password='testpassword123_'
    )
    return user


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_equipment(equipment_1, equipment_2):
    api_client = APIClient()
    get_url = reverse('equipment')
    response = api_client.get(get_url)
    # проверка полей
    equipment = response.data[0]
    assert equipment['name'] == 'Tent MSR Freelite 2'
    assert equipment['category'] == 'Hiking'
    assert equipment['description'] == ('Good balance of weight '
                                        '& livability for solo hikers')
    assert equipment['price'] == '1000.0'
    assert equipment['amount'] == 10

    # проверка количества добавленных объектов
    assert len(response.data) == 2


@pytest.mark.django_db
def test_search_and_filter(api_client, equipment_1, equipment_2, equipment_3):
    # api_client = APIClient()

    # без фильтрации
    get_url = reverse('equipment')
    response = api_client.get(get_url)
    assert len(response.data) == 3

    # поиск
    get_url = reverse('equipment') + '?search=ski'
    response = api_client.get(get_url)
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Salomon XDR 80 TI'
    get_url = reverse('equipment') + '?search=for'
    response = api_client.get(get_url)
    assert len(response.data) == 2
    assert response.data[0]['category'] == 'Hiking'
    assert response.data[1]['category'] == 'Bikes'

    # без сортировки
    get_url = reverse('equipment')
    response = api_client.get(get_url)
    assert response.data[0]['name'] == 'Tent MSR Freelite 2'

    # сортировка
    get_url = reverse('equipment') + '?ordering=category__name'
    response = api_client.get(get_url)
    assert response.data[0]['category'] == 'Bikes'
    assert response.data[1]['category'] == 'Hiking'
    assert response.data[2]['category'] == 'Winter sports'
    get_url = reverse('equipment') + '?ordering=-price'
    response = api_client.get(get_url)
    assert response.data[0]['price'] == '3000.0'
    assert response.data[1]['price'] == '1500.0'
    assert response.data[2]['price'] == '1000.0'


from .feedback_test import feedback_1, feedback_2, feedback_3  # noqa: F401, E402, E501
# keep import here to avoid circular import error


@pytest.mark.django_db
def test_feedback_from_equipment(equipment_3,
                                 feedback_1,   # noqa: F811
                                 feedback_2,   # noqa: F811
                                 feedback_3):   # noqa: F811
    """Проверка отзывов у снаряжения по url 'api/v1/equipment/'"""
    api_client = APIClient()
    list_url = reverse('equipment')
    response = api_client.get(list_url)

    assert len(response.data)
    assert response.data[0]['rating'] == 5.00
    assert response.data[1]['rating'] == 3.50
    assert response.data[2]['rating'] is None

    detail_url = '/api/v1/equipment/2/'
    response = api_client.get(detail_url)
    assert len(response.data['feedback']) == 2
    assert response.data['feedback'][0]['rate'] == 4
    assert response.data['feedback'][1]['rate'] == 3


@pytest.mark.django_db
def test_cart_availability(equipment_1, equipment_2, api_client, user):
    """
    Проверка наличия в корзине снаряжения на выбранную дату
    """
    today = datetime.date.today()
    delta = datetime.timedelta(days=5)
    first_buy = Rentals.objects.create(  # noqa: F841
        user=user,
        equipment=equipment_1,
        amount=2,
        date_start=f'{today}',
        date_end=f'{today + delta}'
    )

    # проверка на прошедшее время
    get_url = (reverse('free_equipment') +
               '?date_start=2023-05-29&date_end=2023-05-30')
    response = api_client.get(get_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # наличие в указанные даты
    get_url_1 = (reverse('free_equipment') +
                 '?date_start={today}&date_end={today + delta}')
    response = api_client.get(get_url_1)
    assert len(response.data) == 2
    assert response.data[0]['available_amount'] == 5
    assert response.data[1]['available_amount'] == 8

    # если в наличии 0 снаряжения, оно не отображается
    second_buy = Rentals.objects.create(   # noqa: F841
        user=user,
        equipment=equipment_2,
        amount=5,
        date_start=f'{today}',
        date_end=f'{today + delta}'
    )
    response = api_client.get(get_url_1)
    assert len(response.data) == 1
    print(response.data)
    assert response.data[0]['available_amount'] == 8

    # наличие в даты, которые пересекаются с занятой датой хотя бы в 1 день
    delta_1 = datetime.timedelta(days=5)
    delta_2 = datetime.timedelta(days=10)
    get_url_2 = (reverse('free_equipment') +
                 f'?date_start={today + delta_1}&date_end={today + delta_2}')
    response = api_client.get(get_url_2)
    assert len(response.data) == 1
    assert response.data[0]['available_amount'] == 8

    # наличие в даты, когда всё свободно
    delta_3 = datetime.timedelta(days=6)
    delta_4 = datetime.timedelta(days=8)
    get_url_3 = (reverse('free_equipment') +
                 f'?date_start={today + delta_3}&date_end={today + delta_4}')
    response = api_client.get(get_url_3)
    assert len(response.data) == 2
    assert response.data[0]['available_amount'] == 5
    assert response.data[1]['available_amount'] == 10
