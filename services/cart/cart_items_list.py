from _decimal import Decimal

from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Concat

from cart.models import Cart


def get_cart_queryset(user: int) -> dict:
    """
    queryset, в котором делается выборка со следующими полями:
    {"Снаряжение": {"поля_модели_equipment": "..."},
            "Количество": 0,
            "Сумма": 0,
            "Даты_аренды": {"дата_начала": "", "дата_конца": ""}}
    """
    queryset = (
        Cart.objects
        .filter(user=user)
        .annotate(
            cart_id=F('id'),
            total_price=F('amount') * F('equipment__price'),
            date_concat=Concat('date_start', 'date_end')  # Объединение даты начала и окончания в одно поле
        )
        .annotate(
            total_amount=Sum('amount'),
            total_summ=Sum('total_price')
        )
        .annotate(
            equipment_info=Concat(      # Создание поля, по которому бы будем
                'equipment__name',      # группировать несколько объектов корзины в один
                Value(' '),
                'date_concat',
                Value(' '),
                output_field=CharField()
            )
        )
        .values('equipment_info')       # Группировка результатов по полю equipment_info
        .annotate(
            equipment_name=F('equipment__name'),
            date_concat=F('date_concat'),
            total_amount=Sum('amount'),
            total_summ=Sum('total_price')
        ).values(
            'id',
            'equipment__id',
            'equipment__name',
            'equipment__price',
            'date_concat',
            'total_amount',
            'total_summ'
        )
        .order_by('equipment__name',  # Сортировка по имени, дате и суммарному количеству
                  'date_concat',
                  'total_amount')
    )
    return queryset


def get_cart_item_data(queryset: dict) -> dict:
    """
    Подсчет общей суммы и количества всех позиций.
    Формирование queryset'a
    """
    cart_item_data = []
    total_positions = 0
    total_summ = Decimal(0.0)

    for item in queryset:  # формирование содержимого корзины в виде вложенного JSON-а
        equipment_name = item['equipment__name']
        equipment_id = item['equipment__id']
        equipment_price = item['equipment__price']
        date_concat = item['date_concat']
        total_amount = item['total_amount']
        total_summ += Decimal(item['total_summ'])

        cart_item_data.append({
            'cart_id': item['id'],
            'equipment': {
                'equipment_id': equipment_id,
                'name': equipment_name,
                'price': str(equipment_price),
            },
            'amount': total_amount,
            'summ': Decimal(item['total_summ']),
            'dates': {
                'date_start': date_concat[:10],
                'date_end': date_concat[10:],
            }
        })

        total_positions += total_amount

    response_data = {
        'cart_item_data': cart_item_data,
        'total_positions': total_positions,
        'total_summ': float(total_summ),
    }

    return response_data
