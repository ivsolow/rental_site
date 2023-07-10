from datetime import date

from django.db.models import Sum, F, IntegerField, Case, When, Avg

from rest_framework.exceptions import ValidationError

from equipment.models import Equipment


def dates_is_valid(date_start: date, date_end: date) -> bool:
    """Проверка дат, если они позже, чем сегодня"""
    if date_start < date.today() or date_end < date.today():
        raise ValidationError()
    return True


def get_available_equipment(date_start: date, date_end: date) -> dict:
    """Выборка снаряжения, доступного в необходимые даты"""
    available_equipment = (
        Equipment.objects.
        select_related('category')
        .prefetch_related('photos')
        .annotate(
            rating=Avg('eq_feedback__rate'),
            occupied_amount=Sum(
                Case(
                    When(
                        rentals__date_start__lte=date_end,
                        rentals__date_end__gte=date_start,
                        then=F('rentals__amount')),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        .annotate(
            available_amount=F('amount') - F('occupied_amount')
        )
        .order_by(
            'name',
            'available_amount'
        )
        .filter(
            available_amount__gt=0
        ))

    return available_equipment
