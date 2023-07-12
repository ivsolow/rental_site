from rest_framework.exceptions import APIException


class CartCheckException(APIException):
    status_code = 400
    message = None
    params = None

    def __init__(self, message=None, params=None):
        if self.default_code is None:
            raise NotImplementedError(
                f"Subclasses of CustomAPIException must define default_code and default_message properties."
            )

        super().__init__(message, code=self.default_code)
        self.params = params


class NotRelevantCartException(CartCheckException):
    default_code = 'Invalid dates'
    message = 'Некоторые даты неактуальны, проверьте корзину'


class UnavailableCartItemsException(CartCheckException):
    default_code = 'Some equipment is not available'
    message = 'Снаряжение на некоторые даты уже нет в наличии, проверьте корзину'


class EmptyCartException(CartCheckException):
    default_code = 'Cart is empty'


class InvalidKeyPaymentException(APIException):
    status_code = 400
    default_detail = 'Invalid key payment'
    default_code = 'invalid_key_payment'
