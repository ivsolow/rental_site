from datetime import date

from django.db.models import Sum, F, IntegerField, Case, When, Avg
from django.core.cache import cache
from django.conf import settings

from rest_framework.exceptions import ValidationError

from equipment.models import Equipment


def dates_is_valid(date_start: date, date_end: date) -> bool:
    """Проверка дат, если они позже, чем сегодня"""
    if date_start < date.today() or date_end < date.today():
        raise ValidationError()
    return True


def get_available_equipment(date_start: date, date_end: date) -> dict:
    """Выборка снаряжения, доступного в необходимые даты"""
    check_dates_in_cache(date_start, date_end)

    cache_key = settings.AVAIL_EQUIPMENT_CACHE_KEY
    available_equipment = cache.get(cache_key)
    if not available_equipment:
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

        cache.set(cache_key, available_equipment, 60 * 5)
    return available_equipment


def check_dates_in_cache(date_start: date, date_end: date) -> None:
    """Проверка дат. Если дата в запросе поменялась, то кэш инвалидируется"""
    requested_dates = str(date_start) + str(date_end)
    cache_key = settings.AVAIL_EQUIPMENT_DATES
    cached_dates = cache.get(cache_key)
    if requested_dates != cached_dates:
        cache.delete(settings.AVAIL_EQUIPMENT_CACHE_KEY)
        cache.set(cache_key, requested_dates, 60 * 5)
    return
