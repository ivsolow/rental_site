from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart
from cart.serializers import AddCartSerializer, CartSerializer
from services.cart.cart_delete import get_cart_object, reduce_equipment_amount, cart_object_remove
from services.cart.cart_items_list import get_cart_queryset, get_cart_item_data
from services.cart.cart_update_or_create import create_cart_object, is_cart_exists,\
                                                cart_update, get_cart_fields


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

        return Response(response_data)

    def create(self, request):
        serializer = AddCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        cart_fields = get_cart_fields(serializer)
        cart = is_cart_exists(cart_fields)

        if cart:
            amount = cart_fields['amount']
            cart_update(cart, amount)
            message = {
                "name": f"{cart_fields['equipment']}",
                "amount": f"{amount}"
            }

            return Response(message, status.HTTP_200_OK)

        else:
            cart = create_cart_object(cart_fields)
            serializer = AddCartSerializer(cart)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)
