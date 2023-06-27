from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import AddCartSerializer, CartSerializer
from cart.tasks import task_cart_add, task_cart_create

from services.cart.cart_delete import get_cart_object, reduce_equipment_amount, cart_object_remove
from services.cart.cart_items_list import get_cart_queryset, get_cart_item_data
from services.cart.existing_cart_check import is_cart_exists
from services.payment.received_payment_operations import send_email_success_payment, start_new_rental


class CartViewSet(viewsets.ViewSet):
    """
    Отображение содержимого корзины(GET-запрос)
    В ответ на GET-запрос, пользователь получает
    вложенный JSON.
    Все таблицы с одинаковой датой и названием снаряжения
    записываются в одно поле с суммарным значением полей amount.

    Обращение к методу create происходит по маршруту: /add_cart/.
    При добавлении нового снаряжения, если снаряжение с указанными датами
    и названием уже существует в корзине, то к уже имеющемуся просто будет добавлено
    количество добавляемого. Иначе, будет создан новый объект.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = CartSerializer

    def list(self, request):
        user = request.user
        queryset = get_cart_queryset(user)
        cart_item_data, total_positions, total_summ = get_cart_item_data(queryset)
        response_data = {
            'cart_item_data': cart_item_data,
            'total_positions': total_positions,
            'total_summ': float(total_summ),
        }

        # user_id = user.id
        # start_new_rental(user_id)
        # print(user_id)
        # total_paid_sum = 10000.0
        # new_rental_detail = start_new_rental(user_id)
        # send_email_success_payment(new_rental_detail, total_paid_sum, user_id)
        return Response(response_data)

    def create(self, request):
        serializer = AddCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        cart_fields = serializer.validated_data
        cart = is_cart_exists(cart_fields)
        error_message = 'Cart data is not added'

        if cart:
            amount = cart_fields['amount']
            result = task_cart_add.delay(cart, amount)
            task_data = result.get()
            if result.ready():
                message = {
                    "name": f"{cart_fields['equipment']}",
                    "amount": f"{amount}"
                }

                return Response(message, status.HTTP_201_CREATED)
            return Response(error_message, status.HTTP_400_BAD_REQUEST)

        else:
            cart_fields['user'] = cart_fields['user'].id
            cart_fields['equipment'] = cart_fields['equipment'].id
            task_result = task_cart_create.delay(cart_fields)
            task_data = task_result.get()
            if task_result.ready():
                return Response(task_data, status=status.HTTP_201_CREATED)
            return Response(error_message, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, amount=None):
        user = request.user

        try:
            cart_object = get_cart_object(pk, user)
            if amount and amount < cart_object.amount:
                reduce_equipment_amount(cart_object, amount)
                message = {
                    "deleted": f"{cart_object.equipment.name}",
                    "amount": int(f"{amount}"),

                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                cart_object_remove(cart_object)
                return Response("Cart object deleted successfully", status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)
