from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from feedback.serializers import AddFeedbackSerializer
from services.feedback.swagger_examples import (
    FEEDBACK_CREATE_REQUEST, FEEDBACK_CREATE_RESPONSE,
    FEEDBACK_CREATE_REQUEST_WITH_PHOTO, FEEDBACK_CREATE_RESPONSE_WITH_PHOTO,
    FEEDBACK_NO_FIELD, FEEDBACK_INVALID_ID,
    EQUIPMENT_FOR_FEEDBACK_RESPONSE, FEEDBACK_LIST,
    FEEDBACK_RETRIEVE_RESPONSE, UPDATED_FEEDBACK_RESPONSE,
    UPDATED_FEEDBACK_REQUEST, DELETE_FEEDBACK_RESPONSE,
    DELETE_FEEDBACK_NOT_FOUND_RESPONSE
)

FEEDBACK_LIST_DECORATOR_KWARGS = {
    "description": "Get the list of all user feedback.",
    "summary": "Feedback List",
    "examples": [
        OpenApiExample(
            name="List of all feedback",
            value=FEEDBACK_LIST,
            response_only=True
        ),
    ],
}

FEEDBACK_RETRIEVE_DECORATOR_KWARGS = {
    "description": "Retrieve feedback by its ID.",
    "summary": "Feedback Retrieve",
    "examples": [
        OpenApiExample(
            name="Get feedback item",
            value=FEEDBACK_RETRIEVE_RESPONSE,
            response_only=True
        ),
    ],
}

FEEDBACK_CREATE_DECORATOR_KWARGS = {
    "description": "Add new feedback after passing"
                   " standard Django serializer validation.",
    "summary": "Add New Feedback",
    "request": AddFeedbackSerializer,
    "responses": {
        200: OpenApiResponse(
            response=AddFeedbackSerializer,
            description="Feedback successfully added.",
            examples=[
                OpenApiExample(
                    name="Feedback response with no photo",
                    value=FEEDBACK_CREATE_RESPONSE,
                    response_only=True
                ),
                OpenApiExample(
                    name="Feedback response with photo",
                    value=FEEDBACK_CREATE_RESPONSE_WITH_PHOTO,
                    response_only=True
                ),
            ]
        ),
        400: OpenApiResponse(
            response=AddFeedbackSerializer,
            description="Bad request.",
            examples=[
                OpenApiExample(
                    name="Response if one of the fields is not provided.",
                    value=FEEDBACK_NO_FIELD,
                    response_only=True
                ),
                OpenApiExample(
                    name="Response if no such equipment ID.",
                    value=FEEDBACK_INVALID_ID,
                    response_only=True
                )
            ]
        ),
    },
    "examples": [
        OpenApiExample(
            name="Feedback request",
            value=FEEDBACK_CREATE_REQUEST,
            request_only=True
        ),
        OpenApiExample(
            name="Feedback request with photo",
            value=FEEDBACK_CREATE_REQUEST_WITH_PHOTO,
            request_only=True
        ),
    ]
}

FEEDBACK_UPDATE_DECORATOR_KWARGS = {
    "description": "Update existing feedback.",
    "summary": "Update Feedback",
    "examples": [
        OpenApiExample(
            name="Update feedback request",
            value=UPDATED_FEEDBACK_REQUEST,
            request_only=True
        ),
        OpenApiExample(
            name="Updated feedback response",
            value=UPDATED_FEEDBACK_RESPONSE,
            response_only=True
        ),
    ],
}

FEEDBACK_DELETE_DECORATOR_KWARGS = {
    "description": "Delete feedback item by ID.",
    "summary": "Delete Feedback",
    "request": AddFeedbackSerializer,
    "responses": {
        200: OpenApiResponse(
            response=AddFeedbackSerializer,
            description="Feedback successfully removed.",
            examples=[
                OpenApiExample(
                    name="Feedback delete response",
                    value=DELETE_FEEDBACK_RESPONSE,
                    response_only=True
                ),
            ]
        ),
        400: OpenApiResponse(
            response=AddFeedbackSerializer,
            description="Bad request.",
            examples=[
                OpenApiExample(
                    name="Feedback not found",
                    value=DELETE_FEEDBACK_NOT_FOUND_RESPONSE,
                    response_only=True
                )
            ],
        )
    },
}

EQUIPMENT_FOR_FEEDBACK_DECORATOR_KWARGS = {
    "description": "Once the user's rental has ended,"
                   " they can leave feedback about the used equipment. "
                   "This endpoint lists the available equipment for feedback.",
    "summary": "Equipment for Feedback",
    "examples": [
        OpenApiExample(
            name="List of equipment available for feedback",
            value=EQUIPMENT_FOR_FEEDBACK_RESPONSE,
            response_only=True
        ),
    ],
}
