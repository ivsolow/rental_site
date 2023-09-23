from django.urls import reverse
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import PaymentSerializer, PaymentStatusSerializer
from services.payment.check_cart_before_payment import availability_check
from services.payment.payment_preparations import get_confirmation_url
from services.payment.payment_status import get_payment_status
from services.payment.received_payment_operations import create_new_payment
from services.payment.exceptions import (
                                UnavailableCartItemsException,
                                NotRelevantCartException,
                                InvalidKeyPaymentException
                                )
from services.payment.decorator_kwargs import (
                                        CHECK_CART_DECORATOR_KWARGS,
                                        COMPOSE_PAYMENT_DECORATOR_KWARGS,
                                        PAYMENT_STATUS_DECORATOR_KWARGS
                                        )


class CartCheckViewSet(viewsets.ModelViewSet):
    """
        Check the cart before making a purchase.
        The cart is checked for emptiness first,
         then for exceeding the quantity and
         outdated dates (later than today).
        Check: Compares the total equipment quantity minus
         the rented equipment quantity with the cart quantity
          on the specified date. If there's more in the cart
           than available, an error message is returned;
         if everything is okay, redirection to payment occurs.
        """
    permission_classes = [IsAuthenticated, ]

    @extend_schema(**CHECK_CART_DECORATOR_KWARGS)
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
    """Compose a payment request and forward it to YooKassa."""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, ]

    @extend_schema(**COMPOSE_PAYMENT_DECORATOR_KWARGS)
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            payment_sum = serializer.validated_data.get('payment_sum')
            commission = serializer.validated_data.get('commission')
            user = request.user
            payment_response = get_confirmation_url(user,
                                                    payment_sum,
                                                    commission)

            return Response(payment_response,
                            status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class YookassaResponseApiView(APIView):
    """
    Handle and process webhooks from YooKassa.
    This endpoint is not utilized in the frontend.
    """

    def post(self, response):
        webhook_data = response.data

        try:
            payment_status = create_new_payment(webhook_data)
        except (ValueError, InvalidKeyPaymentException) as e:
            return Response({'detail': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(payment_status, status=status.HTTP_200_OK)


class PaymentStatusApiView(APIView):
    """Retrieve payment status."""
    serializer_class = PaymentStatusSerializer
    permission_classes = [IsAuthenticated, ]

    @extend_schema(**PAYMENT_STATUS_DECORATOR_KWARGS)
    def post(self, request):
        idempotence_key = request.data['idempotence_key']

        try:
            payment_status = get_payment_status(idempotence_key)
        except InvalidKeyPaymentException as e:
            message = {"Error": e.message}
            return Response(message, status=e.status_code)

        return Response(payment_status, status=status.HTTP_200_OK)
