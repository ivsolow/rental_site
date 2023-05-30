from _decimal import Decimal
from datetime import date
from django.db.models.functions import Concat
from rest_framework import viewsets, status
from django.db.models import Sum, F, IntegerField, Case, When, Value, CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart
from cart.serializers import AddCartSerializer, EquipmentAvailabilitySerializer, \
    AvailableEquipmentSerializer, CartSerializer
from equipment.models import Equipment


class AvailableEquipmentViewSet(viewsets.ViewSet):
    """
    Проверка на наличие доступного снаряжения.
    После ввода желаемых дат для аренды, пользователю
    будет предложено снаряжение и его количество, которое доступно
    на эти даты
    """
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        serializer = EquipmentAvailabilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date_start = serializer.validated_data['date_start']
        date_end = serializer.validated_data['date_end']
        if date_start < date.today() or date_end < date.today():
            return Response({'error': 'You cannot choose past time'}, status=status.HTTP_400_BAD_REQUEST)

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

        equipment_serializer = AvailableEquipmentSerializer(available_equipment, many=True)

        return Response(equipment_serializer.data)


class CartViewSet(viewsets.ViewSet):
    """
    Отображение содержимого корзины(GET-запрос)
    В ответ на GET-запрос, пользователь получает
    вложенный JSON вида:
    {"позиции _в _корзине": [{
            "Снаряжение": {"поля_модели_equipment": "..."},
            "Количество": 0,
            "Сумма": 0,
            "Даты_аренды": {"дата_начала": "", "дата_конца": ""}
            }],
    "Всего_позиций": 0,
    "Общая_сумма": 0 }
    Все таблицы с одинаковой датой и названием снаряжения
    записываются в одно поле с суммарным значением полей amount.

    Обращение к методу create происходит по маршруту: /add_cart/.
    При добавлении нового снаряжения, если снаряжение с указанными датами
    и названием уже существует в корзине, то к уже имеющемуся просто будет добавлено
    количество добавляемого. Иначе, будет создан новый объект.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = CartSerializer

    def list(self, request):
        user = request.user

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
                    'equipment__equipphoto__photo',
                    output_field=CharField()
                )
            )
            .values('equipment_info')  # Группировка результатов по полю equipment_info
            .annotate(  # Разделение поля equipment_info на отдельные поля
                equipment_name=F('equipment__name'),  # Обращение к полю name в модели equipment и создание
                date_concat=F('date_concat'),  # на его основе нового поля equipment_name
                photo=F('equipment__equipphoto__photo'),
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

        cart_items = []
        total_positions = 0
        total_summ = Decimal(0.0)

        for item in queryset:      # формирование содержимого корзины в виде вложенного JSON-а
            equipment_name = item['equipment__name']
            equipment_category = item['equipment__category__name']
            equipment_description = item['equipment__description']
            equipment_price = item['equipment__price']
            equipment_photo = item['photo']
            date_concat = item['date_concat']
            total_amount = item['total_amount']
            total_summ += Decimal(item['total_summ'])

            cart_items.append({
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

        response_data = {
            'cart_items': cart_items,
            'total_positions': total_positions,
            'total_summ': float(total_summ),
        }

        return Response(response_data)

    def create(self, request):
        serializer = AddCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        equipment_id = request.data.get('equipment')
        amount = request.data.get('amount')
        date_start = request.data.get('date_start')
        date_end = request.data.get('date_end')
        equipment = Equipment.objects.get(id=equipment_id)

        # Проверяем, существует ли уже объект корзины с заданными датами и id снаряжения
        cart_exsists = Cart.objects.filter(
            user=user,
            equipment=equipment,
            date_start=date_start,
            date_end=date_end
        ).first()

        if cart_exsists:
            # Если объект корзины уже существует, обновляем его количество
            cart_exsists.amount += int(amount)
            cart_exsists.save()
            message = {
                "name": f"{equipment_id}",
                "amount": f"{amount}"
            }
            return Response(message, status.HTTP_200_OK)

        else:
            # Создаем новый объект корзины
            cart = Cart.objects.create(
                user=user,
                equipment=equipment,
                amount=amount,
                date_start=date_start,
                date_end=date_end
            )

            serializer = AddCartSerializer(cart)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, amount=None):
        user = request.user

        try:
            cart_item = Cart.objects.get(pk=pk, user=user)
            if amount and amount <= cart_item.amount:
                cart_item.amount -= amount
                cart_item.save()
                message = {
                    "deleted": f"{cart_item.equipment.name}",
                    "amount": f"{amount}"
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

