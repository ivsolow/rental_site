from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.core.cache import cache

from cart.models import Cart
from cart.serializers import AddCartSerializer, CartSerializer
from cart.tasks import task_cart_add, task_cart_create
from equipment_rental_site.swagger_examples import CART_LIST_EXAMPLE
from services.cart.cart_delete import get_cart_object, reduce_equipment_amount, cart_object_remove
from services.cart.cart_items_list import get_cart_queryset, get_cart_item_data
from services.cart.existing_cart_check import is_cart_exists


class CartViewSet(viewsets.ViewSet):
    """
    View for managing cart contents.

    GET:
    Returns a nested JSON with information about the items in the cart.
    Each cart entry represents a combination of equipment, its amount, and associated dates.
    All cart entries with the same date and equipment name are combined into a single entry with the total amount.

    POST:
    Adds an item to the cart. If an item with the same dates and equipment name already exists,
    its amount will be increased by the added amount. If the item does not exist, a new entry will be created.

    DELETE:
    Deletes a cart item by its ID. If an `amount` query parameter is provided, it will reduce the amount
    of the item by the specified value. If the amount becomes zero or negative, the item will be completely removed.
    Returns a success message upon successful deletion.
    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = CartSerializer

    @extend_schema(
        description="get cart items",
        summary="Test description of cart",
        examples=[
            OpenApiExample(
                name="Cart list",
                value=CART_LIST_EXAMPLE,
            )
        ],
    )
    def list(self, request):
        user = request.user
        queryset = get_cart_queryset(user)
        response_data = get_cart_item_data(queryset)

        return Response(response_data)

    # @extend_schema(description="create the cart")
    def create(self, request):
        serializer = AddCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        cart_fields = serializer.validated_data

        cache.delete(settings.CART_LIST_CACHE_KEY)

        cart = is_cart_exists(cart_fields)

        if cart:
            amount = cart_fields['amount']
            result = task_cart_add.delay(cart, amount)
            message = {
                "name": f"{cart_fields['equipment']}",
                "amount": f"{amount}"
            }
            return Response(message, status.HTTP_201_CREATED)

        else:
            cart_fields['user'] = cart_fields['user'].id
            cart_fields['equipment'] = cart_fields['equipment'].id
            task_result = task_cart_create.delay(cart_fields)
            return Response(cart_fields, status=status.HTTP_201_CREATED)

    # @extend_schema(description="endpoint for deleting cart")
    def destroy(self, request, pk=None, amount=None):
        user = request.user

        try:
            cart_object = get_cart_object(pk, user)

            cache.delete(settings.CART_LIST_CACHE_KEY)

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
