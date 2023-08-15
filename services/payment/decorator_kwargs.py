from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from rest_framework import serializers
from payment.serializers import PaymentStatusSerializer
from services.payment.swagger_examples import (
    CART_SUCCESSFUL_REDIRECT, CART_INVALID_AMOUNT_RESPONSE, CART_INVALID_DATES_RESPONSE,
    CART_IS_EMPTY, PAYMENT_REQUEST, PAYMENT_RESPONSE, STATUS_REQUEST,
    INVALID_STATUS_RESPONSE, STATUS_RESPONSE_SUCCESS, STATUS_RESPONSE_CREATED
)

CHECK_CART_DECORATOR_KWARGS = {
    "description": "Perform validation on the cart before proceeding with the payment.",
    "summary": "Cart validation before payment",
    "responses": {
        301: OpenApiResponse(
            response=serializers.CharField(),
            description="Successful redirect to the payment page",
            examples=[
                OpenApiExample(
                    name="Redirect to payment",
                    value=CART_SUCCESSFUL_REDIRECT,
                    response_only=True
                ),
            ]
        ),
        400: OpenApiResponse(
            response=serializers.CharField(),
            description="Bad request.",
            examples=[
                OpenApiExample(
                    name="Invalid rental dates",
                    value=CART_INVALID_DATES_RESPONSE,
                    response_only=True
                ),
                OpenApiExample(
                    name="Invalid amount of available equipment",
                    value=CART_INVALID_AMOUNT_RESPONSE,
                    response_only=True
                ),
                OpenApiExample(
                    name="Empty cart",
                    value=CART_IS_EMPTY,
                    response_only=True
                )
            ]
        ),
    },
}

COMPOSE_PAYMENT_DECORATOR_KWARGS = {
    "description": "Compose payment data and send it to Yookassa for processing.",
    "summary": "Sending payment data",
    "examples": [
        OpenApiExample(
            name="Payment request",
            value=PAYMENT_REQUEST,
            request_only=True
        ),
        OpenApiExample(
            name="Payment response",
            value=PAYMENT_RESPONSE,
            response_only=True
        ),
    ],
}

PAYMENT_STATUS_DECORATOR_KWARGS = {
    "description": "After initiating a payment, the server awaits a response from the payment system "
                   "via a webhook. During this time, the frontend sends POST requests to this endpoint "
                   "using a previously saved idempotence key. If the payment is successfully received, "
                   "the server responds with the payment status. Otherwise, the status will be 'Created'.",
    "summary": "Receive payment status",
    "responses": {
        200: OpenApiResponse(
            response=PaymentStatusSerializer,
            description="Valid idempotence key",
            examples=[
                OpenApiExample(
                    name="Successful status response",
                    value=STATUS_RESPONSE_SUCCESS,
                    response_only=True
                ),
                OpenApiExample(
                    name="Created status response",
                    value=STATUS_RESPONSE_CREATED,
                    response_only=True
                ),
            ]
        ),
        400: OpenApiResponse(
            response=PaymentStatusSerializer,
            description="Invalid idempotence key",
            examples=[
                OpenApiExample(
                    name="Bad request",
                    value=INVALID_STATUS_RESPONSE,
                    response_only=True
                ),
            ]
        ),
    },
    "examples": [
        OpenApiExample(
            name="Status request",
            value=STATUS_REQUEST,
            request_only=True
        ),
    ],
}
