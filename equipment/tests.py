import pytest
from django.urls import reverse

from equipment.models import Equipment, Category
from rest_framework.test import APIClient



@pytest.fixture
def equipment_1():
    category = Category.objects.create(name='Hiking')
    equipment = Equipment.objects.create(
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
        name='Salomon XDR 80 TI',
        category=category,
        description='Ski provides excellent precision and stability when riding the slopes',
        price=1500,
        amount=8
    )
    return equipment


@pytest.mark.django_db
def test_equipment(equipment_1, equipment_2):
    api_client = APIClient()
    get_url = reverse('equipment-list')
    response = api_client.get(get_url)

    # проверка полей
    equipment = response.data[0]
    assert equipment['name'] == 'Tent MSR Freelite 2'
    assert equipment['category'] == 'Hiking'
    assert equipment['description'] == 'Good balance of weight & livability for solo hikers'
    assert equipment['price'] == '1000.0'
    assert equipment['amount'] == 10

    # проверка количества добавленных объектов
    assert len(response.data) == 2


@pytest.mark.django_db
def test_search_and_filter(equipment_1, equipment_2, equipment_3):
    api_client = APIClient()

    # без фильтрации
    get_url = reverse('equipment-list')
    response = api_client.get(get_url)
    assert len(response.data) == 3

    # поиск
    get_url = reverse('equipment-list') + f'?search=ski'
    response = api_client.get(get_url)
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Salomon XDR 80 TI'
    get_url = reverse('equipment-list') + f'?search=for'
    response = api_client.get(get_url)
    assert len(response.data) == 2
    assert response.data[0]['category'] == 'Hiking'
    assert response.data[1]['category'] == 'Bikes'

    # без сортировки
    get_url = reverse('equipment-list')
    response = api_client.get(get_url)
    assert response.data[0]['name'] == 'Tent MSR Freelite 2'

    # сортировка
    get_url = reverse('equipment-list') + '?ordering=category__name'
    response = api_client.get(get_url)
    assert response.data[0]['category'] == 'Bikes'
    assert response.data[1]['category'] == 'Hiking'
    assert response.data[2]['category'] == 'Winter sports'
    get_url = reverse('equipment-list') + '?ordering=-price'
    response = api_client.get(get_url)
    assert response.data[0]['price'] == '3000.0'
    assert response.data[1]['price'] == '1500.0'
    assert response.data[2]['price'] == '1000.0'

