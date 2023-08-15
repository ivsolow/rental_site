from drf_spectacular.utils import OpenApiExample

from services.rentals.swagger_examples import RENTAL_RESPONSE_EXAMPLE


RENTALS_LIST_DECORATOR_KWARGS = {
    "description": "List of all user's rentals",
    "summary": "Rentals list",
    "examples": [
        OpenApiExample(
            name="Rental response list",
            value=RENTAL_RESPONSE_EXAMPLE,
            response_only=True
        ),
    ],
}