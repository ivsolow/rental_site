from django.db.models import Sum
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from cart.views import CartViewSet
from equipment.models import Equipment
from rentals.models import Rentals
from .serializers import PaymentSerializer, PaymentCheckSerializer


class CartCheckViewSet(viewsets.ModelViewSet):
    """
    Проверка корзины перед покупкой.
    Если пользователь добавил снаряжение, а зашел оплатить
    какое-то время спустя, то нужного количества на
    указанную дату может не быть.
    Проверка: берем список cart_items из CartViewSet().list(request),
    перебираем его и сопоставляем с количеством сняряжения,
    которое свободно(всего имеется за вычетом оплаченного).
    Если в корзине больше, чем свободно, то возвращается сообщение об ошибке,
    если все ок - идет перенаправление на оплату
    """
    serializer_class = PaymentCheckSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        cart_viewset = CartViewSet()
        response = cart_viewset.list(request)
        cart_items = response.data['cart_items']

        for item in cart_items:
            equipment = get_object_or_404(Equipment, name=item['equipment']['name'])
            date_start = item['dates']['date_start']
            date_end = item['dates']['date_end']

            occupied_amount = Rentals.objects.filter(
                equipment=equipment,
                date_start__lte=date_end,
                date_end__gte=date_start
            ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

            available_amount = equipment.amount - occupied_amount
            if item['amount'] > available_amount:
                difference = item['amount'] - available_amount
                error_message = "Снаряжение на некоторые даты недоступно, проверьте корзину"
                error_data = {
                    'difference': difference,
                    'equipment_name': equipment.name,
                    'date_start': date_start,
                    'date_end': date_end,
                    'message': error_message
                }
                return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        return redirect(reverse('payment'))


class PaymentApiView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return Response(result, status=status.HTTP_200_OK)

