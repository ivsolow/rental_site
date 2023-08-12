from cart.models import Cart


def cart_update(user, cart_fields, amount) -> dict:
    equipment = cart_fields['equipment']
    date_start = cart_fields['date_start']
    date_end = cart_fields['date_end']
    cart_queryset = Cart.objects.get(
        user=user,
        equipment=equipment,
        date_start=date_start,
        date_end=date_end,
    )
    cart_queryset.amount += int(amount)
    cart_queryset.save()
    message = {
        "status": "Cart updated successfully",
        "equipment": f"{cart_fields['equipment']}",
        "amount": f"{amount}"
    }
    return message


def create_new_object(cart_fields) -> Cart:
    cart = Cart.objects.create(
        user=cart_fields['user'],
        amount=cart_fields['amount'],
        equipment=cart_fields['equipment'],
        date_start=cart_fields['date_start'],
        date_end=cart_fields['date_end']
        )

    return cart
