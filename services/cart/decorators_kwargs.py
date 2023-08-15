from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from cart.serializers import CartSerializer
from services.cart.swagger_examples import CART_LIST_RESPONSE, CART_CREATE_REQUEST, CART_CREATE_RESPONSE, \
    CART_UPDATE_RESPONSE, CART_DELETE_ITEMS, CART_DELETE_OBJECT, CART_ITEM_NOT_FOUND


CART_LIST_DECORATOR_KWARGS = {
    "description": "Retrieve all cart items from the database. "
                   "If different cart instances have the same equipment and dates,"
                   "they will be combined into a single entry.",
    "summary": "Retrieve cart items",
    "examples": [
        OpenApiExample(
            name="Cart list",
            value=CART_LIST_RESPONSE,
        )
    ],
}

CART_CREATE_DECORATOR_KWARGS = {
    "description": "When adding a new equipment to the cart, a validation check is performed: "
                   "if an item with the same equipment and dates already exists, the existing "
                   "object will be updated. "
                   "If not, a new cart object will be created.",
    "summary": "Add a new equipment to the cart",
    "examples": [
        OpenApiExample(
            name="Cart request",
            value=CART_CREATE_REQUEST,
            request_only=True
        ),
        OpenApiExample(
            name="Cart response for a newly created cart object",
            value=CART_CREATE_RESPONSE,
            response_only=True
        ),
        OpenApiExample(
            name="Cart response for an existing cart object with updated amount",
            value=CART_UPDATE_RESPONSE,
            response_only=True
        )
    ],
}


CART_DESTROY_DECORATOR_KWARGS = {
    "description": "Deletes a cart item or the entire cart object, depending on the amount of deleting equipment.",
    "summary": "Delete cart items",
    "responses": {
        200: OpenApiResponse(
            response=CartSerializer,
            description="The item (or object) was successfully removed.",
            examples=[
                OpenApiExample(
                    name="Response if cart items were deleted",
                    value=CART_DELETE_ITEMS,
                    response_only=True
                ),
                OpenApiExample(
                    name="Response if the entire cart object was deleted",
                    value=CART_DELETE_OBJECT,
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            response=CartSerializer,
            description="Invalid cart ID",
            examples=[
                OpenApiExample(
                    name="Response if the cart ID is not valid",
                    value=CART_ITEM_NOT_FOUND,
                    response_only=True
                )
            ]
        ),
    },
}
