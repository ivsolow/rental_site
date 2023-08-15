
CART_LIST_RESPONSE = {
    "cart_item_data": [
        {
            "cart_id": 9,
            "equipment": {
                "equipment_id": 4,
                "name": "Canyon Strive CFR",
                "price": "3000.0"
            },
            "amount": 2,
            "total_sum": 6000.0,
            "dates": {
                "date_start": "2023-08-11",
                "date_end": "2023-08-24"
            }
        }
    ],
    "total_positions": 2,
    "total_sum": 6000.0
}

CART_CREATE_REQUEST = {
    "equipment": "1",
    "amount": "2",
    "date_start": "2024-08-05",
    "date_end": "2024-08-08",
}

CART_CREATE_RESPONSE = {
    "equipment": "1",
    "amount": "2",
    "date_start": "2024-08-05",
    "date_end": "2024-08-08",
}

CART_UPDATE_RESPONSE = {
    "status": "Cart updated successfully",
    "equipment": "1",
    "amount": "2"
}

CART_DELETE_ITEMS = {
    "deleted": "Canyon Strive CFR",
    "amount": "3",
}

CART_DELETE_OBJECT = {
    "response": "Cart object deleted successfully"
}

CART_ITEM_NOT_FOUND = {
    "error": "Cart item not found."
}
