from django.urls import reverse
from django.shortcuts import redirect

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import PaymentSerializer, PaymentStatusSerializer
from services.payment.check_cart_before_payment import availability_check
from services.payment.payment_preparations import get_confirmation_url
from services.payment.payment_status import get_payment_status
from services.payment.received_payment_operations import create_new_payment
from services.payment.exceptions import UnavailableCartItemsException, NotRelevantCartException, \
                                                                       InvalidKeyPaymentException


class CartCheckViewSet(viewsets.ModelViewSet):
    """
    Проверка корзины перед покупкой.
    Сначала проверка на пустую корзину, затем на превышение количества
    и неактуальную дату(позже, чем сегодня).
    Проверка: сравнивается количество снаряжения всего минус количество
     сняряжения в аренде с количеством в корзине на указанную дату.
    Если в корзине больше, чем свободно, то возвращается сообщение об ошибке,
    если все ок - идет перенаправление на оплату
    """
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        try:
            availability_check(request)
        except (NotRelevantCartException, UnavailableCartItemsException) as e:
            error_details = {
                'message': e.message,
                'params': e.params
            }
            return Response(error_details, status=e.status_code)

        return redirect(reverse('payment'))


class PaymentApiView(APIView):
    """Формирование запроса на оплату и отправка запроса Юкассе"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            payment_sum = serializer.validated_data.get('payment_sum')
            commission = serializer.validated_data.get('commission')
            user = request.user
            payment_response = get_confirmation_url(user, payment_sum, commission)

            return Response(payment_response, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YookassaResponseApiView(APIView):
    """Получение и обработка вебхука от Юкассы"""
    def post(self, response):
        webhook_data = response.data

        try:
            payment_status = create_new_payment(webhook_data)
        except (ValueError, InvalidKeyPaymentException) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(payment_status, status=status.HTTP_200_OK)


class PaymentStatusApiView(APIView):
    """Представление для получения статуса оплаты"""
    serializer_class = PaymentStatusSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        idempotence_key = request.data['idempotence_key']

        try:
            payment_status = get_payment_status(idempotence_key)
        except InvalidKeyPaymentException as e:
            return Response(e.message, status=e.status_code)

        return Response(payment_status, status=status.HTTP_200_OK)
