from rest_framework import serializers

from cart.models import Cart
from rentals.models import Rentals


class PaymentCheckSerializer(serializers.ModelSerializer):
    response = serializers.CharField()

    class Meta:
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """
    Нужно реализовать проверку на пустую корзину!!
    """
    payment_code = serializers.CharField()

    # class Meta:
    #     model = Cart
    #     fields = '__all__'

    def validate_payment_code(self, value):
        if value != "123":
            raise serializers.ValidationError("Invalid payment code")
        return value

    def create(self, validated_data):
        # Получение пользователя из контекста запроса
        user = self.context['request'].user

        # Получение записей в корзине пользователя
        cart_items = Cart.objects.filter(user=user)

        # Создание записей в таблице Rentals на основе корзины пользователя
        rentals = []
        for cart_item in cart_items:
            rental = Rentals.objects.create(
                equipment=cart_item.equipment_1,
                user=user,
                amount=cart_item.amount,
                date_start=cart_item.date_start,
                date_end=cart_item.date_end
            )
            rentals.append(rental)

        # Удаление записей из таблицы Cart
        cart_items.delete()

        return "Payment successful"
