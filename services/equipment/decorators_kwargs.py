from drf_spectacular.utils import (OpenApiExample,
                                   OpenApiResponse,
                                   OpenApiParameter)
from equipment.serializers import (EquipmentDetailSerializer,
                                   AvailableEquipmentSerializer)
from services.equipment.swagger_examples import (
    EQUIPMENT_LIST_RESPONSE,
    EQUIPMENT_ITEM_RESPONSE,
    AVAIL_EQUIPMENT_INVALID_RESPONSE,
)

EQUIPMENT_LIST_DECORATOR_KWARGS = {
    "description": "Retrieve a list of all equipment items from the database.",
    "summary": "Get all equipment items",
    "examples": [
        OpenApiExample(
            name="Equipment list",
            value=EQUIPMENT_LIST_RESPONSE,
        )
    ],
}

EQUIPMENT_ITEM_DECORATOR_KWARGS = {
    "description": "Retrieve details of a specific equipment item by its ID. "
                   "This endpoint offers additional information,"
                   " including list user feedback.",
    "summary": "Get equipment item by ID",
    "responses": {
        200: OpenApiResponse(
            response=EquipmentDetailSerializer,
            examples=[
                OpenApiExample(
                    name="Equipment item",
                    value=EQUIPMENT_ITEM_RESPONSE,
                )
            ]
        )
    }
}

AVAIL_EQUIPMENT_DECORATOR_KWARGS = {
    "description": "Retrieve all available equipment for"
                   " the specified rental dates.",
    "summary": "Get available equipment for rental dates",
    "responses": {
        200: OpenApiResponse(
            response=AvailableEquipmentSerializer,
            examples=[
                OpenApiExample(
                    name="Valid dates",
                    value=EQUIPMENT_LIST_RESPONSE,
                )
            ]
        ),
        400: OpenApiResponse(
            response=AvailableEquipmentSerializer,
            examples=[
                OpenApiExample(
                    name="Invalid dates",
                    value=AVAIL_EQUIPMENT_INVALID_RESPONSE,
                )
            ]
        )
    },
    "parameters": [
        OpenApiParameter(
            name='date_start',
            location=OpenApiParameter.QUERY,
            description='Start date of the rental period',
            required=True,
            type=str
        ),
        OpenApiParameter(
            name='date_end',
            location=OpenApiParameter.QUERY,
            description='End date of the rental period',
            required=True,
            type=str
        ),
    ]
}
