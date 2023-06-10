from cart.models import Cart


def get_cart_object(pk: int, user: int) -> Cart:
    cart_object = Cart.objects.get(pk=pk, user=user)
    return cart_object


def reduce_equipment_amount(cart_object: Cart, amount: int) -> None:
    cart_object.amount -= amount
    cart_object.save()


def cart_object_remove(cart_object: Cart) -> None:
    cart_object.delete()