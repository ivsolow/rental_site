from cart.models import Cart
from cart.serializers import AddCartSerializer


def get_cart_fields(serializer: AddCartSerializer) -> dict:
    """Получаем значения для корзины из полей сериализатора"""
    print(type(serializer))
    user = serializer.validated_data['user']
    amount = serializer.validated_data['amount']
    date_start = serializer.validated_data['date_start']
    date_end = serializer.validated_data['date_end']
    equipment = serializer.validated_data['equipment']['id']

    cart_fields = {
        'user': user,
        'amount': amount,
        'date_start': date_start,
        'date_end': date_end,
        'equipment': equipment
    }

    return cart_fields


def is_cart_exists(cart_fields: dict) -> Cart:
    """Проверяем, существует ли объект корзины с такими же полями"""
    cart = Cart.objects.filter(
        user=cart_fields['user'],
        equipment=cart_fields['equipment'],
        date_start=cart_fields['date_start'],
        date_end=cart_fields['date_end']
    ).first()

    return cart


def cart_update(cart: Cart, amount: int) -> None:
    """Обновление данных существующего объекта корзины"""
    cart.amount += int(amount)
    cart.save()


def create_cart_object(cart_fields: dict) -> Cart:
    """Создание нового объекта корзины"""
    cart = Cart.objects.create(
        user=cart_fields['user'],
        amount=cart_fields['amount'],
        equipment=cart_fields['equipment'],
        date_start=cart_fields['date_start'],
        date_end=cart_fields['date_end']
    )
    return cart
