from datetime import date

from rest_framework.request import Request

from django.db.models import Sum

from cart.models import Cart
from equipment.models import Equipment
from rentals.models import Rentals
from services.payment.exceptions import (NotRelevantCartException,
                                         UnavailableCartItemsException,
                                         EmptyCartException)


def availability_check(request: Request) -> bool:
    """
    Check for an empty cart and past dates.
    If the cart is not empty, verify that the equipment quantity
    does not exceed availability, and there is no equipment
    in the cart for dates later than today.
    """
    user = request.user
    cart = Cart.objects.filter(user=user)
    if not cart:
        raise EmptyCartException(
            message='Корзина пуста'
                    )

    for item in cart:
        equipment = Equipment.objects.get(id=item.equipment.id)
        date_start = item.date_start
        date_end = item.date_end
        occupied_amount = get_occupied_amount(equipment, date_start, date_end)
        available_amount = equipment.amount - occupied_amount
        if date_start < date.today():
            raise NotRelevantCartException(
                params={
                    'equipment_name': equipment.name,
                    'date_start': date_start,
                    'date_end': date_end
                }
            )

        elif item.amount > available_amount:
            exceeding_amount = item.amount - available_amount
            raise UnavailableCartItemsException(
                params={
                    'exceeding_amount': exceeding_amount,
                    'equipment_name': equipment.name,
                    'date_start': date_start,
                    'date_end': date_end
                }
            )
    return True


def get_occupied_amount(equipment: Equipment, date_start: date, date_end: date) -> Rentals:
    """Retrieve the amount of occupied equipment for specific dates."""
    occupied_amount = Rentals.objects.filter(
        equipment=equipment,
        date_start__lte=date_end,
        date_end__gte=date_start
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    return occupied_amount
