FEEDBACK_LIST = [
    {
        "id": 2,
        "equipment": {
            "id": 4,
            "name": "Canyon Strive CFR"
        },
        "rate": 5,
        "content": "It's absolutely crazy shit",
        "date_created": "2023-08-12",
        "feedback_photo": [
            {
                "photo": "some_address/media/"
                         "Feedback/user%40example."
                         "com%20about%20Canyon%20Strive%20CFR"
                         "/Canyon_Strive_CFR_1.webp"
            }
        ]
    },
    {
        "id": 4,
        "equipment": {
            "id": 4,
            "name": "Canyon Strive CFR"
        },
        "rate": 4,
        "content": "Good stuff",
        "date_created": "2023-08-13",
        "feedback_photo": []
    }
]

FEEDBACK_RETRIEVE_RESPONSE = {
    "id": 2,
    "equipment": {
        "id": 4,
        "name": "Canyon Strive CFR"
    },
    "rate": 5,
    "content": "It's absolutely crazy shit",
    "date_created": "2023-08-12",
    "feedback_photo": [
        {
            "photo": "some_address/media/"
                     "Feedback/user%40example."
                     "com%20about%20Canyon%20Strive%20CFR"
                     "/Canyon_Strive_CFR_1.webp"
        }
    ]
}

FEEDBACK_CREATE_REQUEST = {
    "equipment": 4,
    "content": "Some feedback content",
    "rate": 4
}

FEEDBACK_CREATE_REQUEST_WITH_PHOTO = {
    "equipment": 4,
    "content": "Some feedback content",
    "rate": 4,
    "feedback_photo": [
        'photo_1/url',
        'photo_2/url'
    ]
}

FEEDBACK_CREATE_RESPONSE = {
    "id": 3,
    "equipment": {
        "id": 4,
        "name": "Canyon Strive CFR"
    },
    "rate": 4,
    "content": "Some feedback content",
    "date_created": "2023-08-13",
    "feedback_photo": []
}

FEEDBACK_CREATE_RESPONSE_WITH_PHOTO = {
    "id": 3,
    "equipment": {
        "id": 4,
        "name": "Canyon Strive CFR"
    },
    "rate": 4,
    "content": "Some feedback content",
    "date_created": "2023-08-13",
    "feedback_photo": [
        'photo_1/url',
        'photo_2/url'
    ]
}

FEEDBACK_NO_FIELD = {
    "equipment": [
        "This field is required."
    ]
}

FEEDBACK_INVALID_ID = [
    "No such equipment"
]

UPDATED_FEEDBACK_RESPONSE = {
    "id": 2,
    "equipment": {
        "id": 4,
        "name": "Canyon Strive CFR"
    },
    "rate": 4,
    "content": "New content",
    "date_created": "2023-08-12",
    "feedback_photo": []
}

UPDATED_FEEDBACK_REQUEST = {
    "equipment": {"id": 4, "name": "Canyon Strive CFR"},
    "content": "New content",
    "rate": 4,
    "feedback_photo": []
}

DELETE_FEEDBACK_RESPONSE = {
    "id": 5
}

DELETE_FEEDBACK_NOT_FOUND_RESPONSE = {"detail": "Object not found."}

EQUIPMENT_FOR_FEEDBACK_RESPONSE = [
    {
        "id": 3,
        "name": "Canyon Strive CFR"
    },
    {
        "id": 5,
        "name": "MSR Tindheim"
    }
]
