from cart.models import Cart
import pytest
from django.urls import reverse
from rest_framework import status
from equipment.tests import user, api_client, equipment_1, equipment_2


@pytest.fixture
def cart_create(user, equipment_1):
    cart = Cart.objects.create(
        user=user,
        amount=3,
        equipment=equipment_1,
        date_start='2023-05-20',
        date_end='2023-05-22'
    )
    return cart


@pytest.fixture
def cart_create_2(user, equipment_2):
    cart = Cart.objects.create(
        user=user,
        amount=1,
        equipment=equipment_2,
        date_start="2023-05-25",
        date_end="2023-05-28"
    )
    return cart


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
    assert 'cart_item_data' in response.data
    assert 'total_positions' in response.data
    assert 'total_summ' in response.data

    cart_item_data = response.data['cart_item_data']
    assert isinstance(cart_item_data, list)

    # Проверяем, что список позиций корзины пустой
    assert len(cart_item_data) == 0

    # Проверяем структуру и данные каждой позиции корзины
    for item in cart_item_data:
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
def test_add_cart_same_instance(api_client, cart_create, equipment_1):
    """
    Проверка на добавление количества к тому же объекту корзину
    при совпадении дат и и названия снаряжения
    """

    get_url = reverse('cart')
    get_response = api_client.get(get_url)
    print(get_response.data)
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.data['cart_item_data'][0]['amount'] == 3
    assert get_response.data['cart_item_data'][0]['equipment']['name'] == equipment_1.name


@pytest.mark.django_db
def test_add_cart_different_instances(api_client, cart_create, cart_create_2):
    """
    Проверка на добавление количества к разным объектам корзины
    при несовпадении дат и/или названия снаряжения
    """
    get_url = reverse('cart')

    result = api_client.get(get_url)
    print(result.data)
    assert len(result.data['cart_item_data']) == 2
    assert result.data['cart_item_data'][0]['amount'] == 1
    assert result.data['cart_item_data'][1]['amount'] == 3



@pytest.mark.django_db
def test_delete_cart_items(cart_create, api_client):
    get_url = reverse('cart')
    get_response = api_client.get(get_url)
    pk = get_response.data['cart_item_data'][0]['id']
    # проверяем количество в корзине до удаления
    assert get_response.data['cart_item_data'][0]['amount'] == 3
    url = reverse('cart_delete', kwargs={'pk': pk, 'amount': 2})
    delete_response = api_client.delete(url)
    # ответ сервера после удаления
    assert delete_response.status_code == 200
    assert delete_response.data['amount'] == 2
    get_response = api_client.get(get_url)
    # количество после удаления
    assert get_response.data['cart_item_data'][0]['amount'] == 1


@pytest.mark.django_db
def test_delete_cart_object(cart_create, api_client):
    get_url = reverse('cart')
    get_response = api_client.get(get_url)
    pk = get_response.data['cart_item_data'][0]['id']

    url = reverse('cart_delete', kwargs={'pk': pk, 'amount': 3})
    delete_response = api_client.delete(url)
    # ответ сервера после удаления
    assert delete_response.status_code == 204
    assert delete_response.data is None
    get_response = api_client.get(get_url)
    # количество после удаления
    assert len(get_response.data['cart_item_data']) == 0


@pytest.mark.django_db
def test_delete_by_invalid_pk(api_client):
    get_url = reverse('cart')
    get_response = api_client.get(get_url)
    pk = 1

    url = reverse('cart_delete', kwargs={'pk': pk, 'amount': 3})
    delete_response = api_client.delete(url)
    # ответ сервера после удаления
    assert delete_response.status_code == 404
    assert delete_response.data['error'] == 'Cart item not found.'
    get_response = api_client.get(get_url)
    assert len(get_response.data['cart_item_data']) == 0
#
