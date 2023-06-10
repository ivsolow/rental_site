from datetime import date

from django.db.models import Sum, F, IntegerField, Case, When

from equipment.models import Equipment, EquipPhoto


def dates_is_valid(date_start: date, date_end: date) -> bool:
    """Проверка дат, если они позже, чем сегодня"""
    if date_start < date.today() or date_end < date.today():
        return False
    return True


def get_available_equipment(date_start: date, date_end: date) -> dict:
    """Выборка снаряжения, доступного в необходимые даты"""
    available_equipment = Equipment.objects.annotate(
        occupied_amount=Sum(
            Case(
                When(rentals__date_start__lte=date_end, rentals__date_end__gte=date_start,
                     then=F('rentals__amount')),
                default=0,
                output_field=IntegerField()
            )
        )
    ).annotate(
        available_amount=F('amount') - F('occupied_amount')
    ).order_by('name',
               'available_amount').filter(
        available_amount__gt=0
    )
    return available_equipment


def get_equipment_photo(obj: Equipment) -> str:
    """Возвращает фото, связанные с данным снаряжением"""
    try:
        equip_photo = EquipPhoto.objects.get(equipment=obj)
        return equip_photo.photo.url
    except EquipPhoto.DoesNotExist:
        return None
