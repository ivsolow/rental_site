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
        .filter(user=user)  # Фильтрация по пользователю
        .select_related('equipment__category')  # Загрузка связанных объектов (категория снаряжения)
        .annotate(
            cart_id=F('id'),
            total_price=F('amount') * F('equipment__price'),  # Вычисление общей стоимости снаряжения
            date_concat=Concat('date_start', 'date_end')  # Объединение даты начала и окончания в одно поле
        )
        .annotate(
            total_amount=Sum('amount'),  # Вычисление суммарного количества снаряжения
            total_summ=Sum('total_price')  # Вычисление суммарной стоимости снаряжения
        )
        .annotate(
            equipment_info=Concat(  # Создание поля с объединенной информацией о снаряжении
                'equipment__name',
                Value(' '),
                'date_concat',
                Value(' '),
                'equipment__photos__photo',
                output_field=CharField()
            )
        )
        .values('equipment_info')  # Группировка результатов по полю equipment_info
        .annotate(  # Разделение поля equipment_info на отдельные поля
            equipment_name=F('equipment__name'),  # Обращение к полю name в модели equipment и создание
            date_concat=F('date_concat'),  # на его основе нового поля equipment_name
            photo=F('equipment__photos__photo'),
            total_amount=Sum('amount'),
            total_summ=Sum('total_price')
        )
        .values(
            'id',
            'equipment__name',  # Выбор полей снаряжения
            'equipment__category__name',
            'equipment__description',
            'equipment__price',
            'equipment__amount',
            'date_concat',  # Выбор объединенного поля даты
            'total_amount',  # Выбор суммарного количества
            'total_summ',  # Выбор суммарной стоимости
            'photo'  # Выбор поля фотографии
        )
        .order_by('equipment__name',  # Сортировка по имени, дате и суммарному количеству
                  'date_concat',
                  'total_amount')
    )
    return queryset


def get_cart_item_data(queryset):
    """Подсчет общей суммы и количества позиций всего """
    cart_item_data = []
    total_positions = 0
    total_summ = Decimal(0.0)

    for item in queryset:  # формирование содержимого корзины в виде вложенного JSON-а
        equipment_name = item['equipment__name']
        equipment_category = item['equipment__category__name']
        equipment_description = item['equipment__description']
        equipment_price = item['equipment__price']
        equipment_photo = item['photo']
        date_concat = item['date_concat']
        total_amount = item['total_amount']
        total_summ += Decimal(item['total_summ'])

        cart_item_data.append({
            'id': item['id'],
            'equipment': {
                'name': equipment_name,
                'category': equipment_category,
                'description': equipment_description,
                'price': str(equipment_price),
                'photo': equipment_photo,
            },
            'amount': total_amount,
            'summ': Decimal(item['total_summ']),
            'dates': {
                'date_start': date_concat[:10],
                'date_end': date_concat[10:],
            }
        })

        total_positions += total_amount

    return cart_item_data, total_positions, total_summ
