from rest_framework.exceptions import APIException


class CartCheckException(APIException):
    status_code = 400
    message = None
    params = None

    def __init__(self, message=None, params=None):
        if self.default_code is None:
            raise NotImplementedError(
                "Subclasses of CustomAPIException "
                "must define default_code and default_message properties."
            )

        super().__init__(message, code=self.default_code)
        self.params = params


class NotRelevantCartException(CartCheckException):
    default_code = 'Invalid dates'
    message = 'Some dates are not relevant, please check your cart'


class UnavailableCartItemsException(CartCheckException):
    default_code = 'Some equipment is not available'
    message = ('Some equipment is no longer available for certain dates.'
               ' Please review the contents of your cart."')


class EmptyCartException(CartCheckException):
    default_code = 'Cart is empty'


class InvalidKeyPaymentException(APIException):
    status_code = 400
    message = 'Invalid key payment'
    default_code = 'invalid_key_payment'
