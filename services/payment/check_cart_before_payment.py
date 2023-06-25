from django.db.models import Sum

from cart.models import Cart
from equipment.models import Equipment
from rentals.models import Rentals


def availability_check(request):
    """
    Проверка на пустую корзину.
    Если она не пустая, то проверяем, не
    превышает ли количество снаряжения доступное количество
    """
    user = request.user
    cart = Cart.objects.filter(user=user)
    if not cart:
        return None
    for item in cart:
        equipment = Equipment.objects.get(id=item.equipment.id)
        date_start = item.date_start
        date_end = item.date_end
        occupied_amount = get_occupied_amount(equipment, date_start, date_end)
        available_amount = equipment.amount - occupied_amount
        if item.amount > available_amount:
            exceeding_amount = item.amount - available_amount
            error_message = "Снаряжение на некоторые даты недоступно, проверьте корзину"
            error_data = {
                'exceeding_amount': exceeding_amount,
                'equipment_name': equipment.name,
                'date_start': date_start,
                'date_end': date_end,
                'message': error_message
            }
            return error_data
    return True


def get_occupied_amount(equipment, date_start, date_end):
    """Возвращаем количество занятого снаряжения на конкретные даты"""
    occupied_amount = Rentals.objects.filter(
        equipment=equipment,
        date_start__lte=date_end,
        date_end__gte=date_start
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    return occupied_amount
