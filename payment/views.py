from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from services.payment.check_cart_before_payment import availability_check
from services.payment.payment import get_confirmation_url
from services.payment.payment_status import get_payment_status
from services.payment.yookassa_webhook import validate_and_create_payment
from .serializers import PaymentSerializer, PaymentStatusSerializer


class CartCheckViewSet(viewsets.ModelViewSet):
    """
    Проверка корзины перед покупкой.
    Сначала проверка на пустую корзину, затем на превышение количества.
    Проверка: сравнивается количество снаряжения всего минус количество
     сняряжения в аренде с количеством в корзине на указанную дату.
    Если в корзине больше, чем свободно, то возвращается сообщение об ошибке,
    если все ок - идет перенаправление на оплату
    """
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        result = availability_check(request)
        if not result:
            return Response('Корзина пуста', status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(result, dict):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return redirect(reverse('payment'))


class PaymentApiView(APIView):
    """Формирование запроса на оплату и отправка запроса Юкассе"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.POST)
        if serializer.is_valid():
            serialized_data = serializer.validated_data
        else:
            answer = 'Serialized data is not valid!'
            return Response(answer, status=status.HTTP_400_BAD_REQUEST)
        payment_summ = serialized_data.get('total_summ')
        commission = serialized_data.get('commission')
        user = request.user
        confirmation_url = get_confirmation_url(user, payment_summ, commission)

        return Response(confirmation_url, status=status.HTTP_200_OK)


class YookassaResponseApiView(APIView):
    """Получение и обработка вебхука от Юкассы"""

    def post(self, response):
        webhook_data = response.data
        if not validate_and_create_payment(webhook_data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class PaymentStatusApiView(APIView):
    """Представление для получения статуса оплаты"""
    serializer_class = PaymentStatusSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        idempotence_key = request.data['idempotence_key']
        payment_status = get_payment_status(idempotence_key)
        if payment_status:
            return Response(payment_status, status=status.HTTP_200_OK)
        return Response({"error": "Invalid idempotence_key"}, status=status.HTTP_204_NO_CONTENT)
