
METHOD_NOT_ALLOWED_MESSAGE = {"detail": "Method \"GET\" is not allowed"}

CART_SUCCESSFUL_REDIRECT = ("No content, redirect to URL `api/v1/payment/`. "
                            f"There will be a message in Swagger: "
                            f"{METHOD_NOT_ALLOWED_MESSAGE}")

CART_INVALID_DATES_RESPONSE = {
    "message": "Some dates are not relevant, please check your cart",
    "params": {
        "equipment_name": "Canyon Strive CFR",
        "date_start": "2023-08-11",
        "date_end": "2023-08-24"
    }
}

CART_INVALID_AMOUNT_RESPONSE = {
    "message": "Certain equipment is no longer available on some dates,"
               " please check your cart",
    "params": {
        "exceeding_amount": 2,
        "equipment_name": "Canyon Strive CFR",
        "date_start": "2023-08-16",
        "date_end": "2023-08-31"
    }
}

CART_IS_EMPTY = {
    "detail": "The cart is empty"
}

PAYMENT_REQUEST = {
    "payment_sum": 1000,
    "commission": "3.5"
}

PAYMENT_RESPONSE = {
    "confirmation_url":
        "https://yoomoney.ru/checkout/"
        "payments/v2/"
        "contract?orderId=2c6d3be1-000f-5000-a000-1a70d29b12fb",
    "idempotence_key": "e00fa3b7-7185-47f6-9a94-186e525d09ba"
}

STATUS_REQUEST = {
    "idempotence_key": "e00fa3b7-7185-47f6-9a94-186e525d09ba"
}

STATUS_RESPONSE_SUCCESS = {
    "amount": 1000,
    "status": "payment.succeeded"
}

STATUS_RESPONSE_CREATED = {
    "amount": 1000,
    "status": "Created"
}

INVALID_STATUS_RESPONSE = {
    "Error": "Invalid key payment"
}
