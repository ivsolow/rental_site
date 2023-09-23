from _decimal import Decimal

from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Concat
from django.core.cache import cache
from django.conf import settings

from cart.models import Cart


def get_cart_queryset(user: int) -> dict:
    cache_key = settings.CART_LIST_CACHE_KEY
    cart_queryset = cache.get(cache_key)
    if not cart_queryset:
        cart_queryset = (
            Cart.objects
            .filter(user=user)
            .annotate(
                cart_id=F('id'),
                total_price=F('amount') * F('equipment__price'),
                date_concat=Concat('date_start', 'date_end')
            )
            .annotate(
                total_amount=Sum('amount'),
                total_summ=Sum('total_price')
            )
            .annotate(
                equipment_info=Concat(
                    'equipment__name',
                    Value(' '),
                    'date_concat',
                    Value(' '),
                    output_field=CharField()
                )
            )
            .values('equipment_info')
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
            .order_by('equipment__name',
                      'date_concat',
                      'total_amount')
        )
        cache.set(cache_key, cart_queryset, 60 * 10)
    return cart_queryset


def get_cart_item_data(queryset: dict) -> dict:
    """
    Calculate the total sum and quantity of all positions.
    Generate JSON data.
    """
    cart_item_data = []
    total_positions = 0
    total_summ = Decimal(0.0)

    for item in queryset:
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
