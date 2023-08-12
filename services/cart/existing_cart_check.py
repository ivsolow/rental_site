from cart.models import Cart


def is_cart_exists(cart_fields: dict) -> Cart:
    """Check if a cart object with the same fields exists"""
    cart = Cart.objects.filter(
        user=cart_fields['user'],
        equipment=cart_fields['equipment'],
        date_start=cart_fields['date_start'],
        date_end=cart_fields['date_end']
    ).values().first()

    return cart
