from celery import shared_task

from cart.models import Cart
from cart.serializers import AddCartSerializer
from equipment.models import Equipment
from users.models import CustomUser


@shared_task
def task_cart_add(cart, amount):
    """Обновление данных существующего объекта корзины"""
    user = cart['user_id']
    equipment = cart['equipment_id']
    date_start = cart['date_start']
    date_end = cart['date_end']
    cart_queryset = Cart.objects.get(
        user=user,
        equipment=equipment,
        date_start=date_start,
        date_end=date_end,
    )
    cart_queryset.amount += int(amount)
    cart_queryset.save()

    return 'Cart updated succefully'


@shared_task
def task_cart_create(cart_fields):
    user_id = int(cart_fields['user'])
    equipment_id = int(cart_fields['equipment'])
    user = CustomUser.objects.get(id=user_id)
    equipment = Equipment.objects.get(id=equipment_id)

    cart = Cart.objects.create(
        user=user,
        amount=cart_fields['amount'],
        equipment=equipment,
        date_start=cart_fields['date_start'],
        date_end=cart_fields['date_end']
        )

    serializer = AddCartSerializer(cart)
    return serializer.data


# def task_cart_create_sync(cart_fields):
#     user_id = int(cart_fields['user'])
#     equipment_id = int(cart_fields['equipment'])
#     user = CustomUser.objects.get(id=user_id)
#     equipment = Equipment.objects.get(id=equipment_id)
#
#     cart = Cart.objects.create(
#         user=user,
#         amount=cart_fields['amount'],
#         equipment=equipment,
#         date_start=cart_fields['date_start'],
#         date_end=cart_fields['date_end']
#         )
#
#     serializer = AddCartSerializer(cart)
#     return serializer.data
