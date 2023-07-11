from datetime import date

from rest_framework import serializers

from cart.models import Cart
from equipment.models import Equipment


class CartEquipmentSerializer(serializers.ModelSerializer):
    """Поле equipment сериализатора CartSerializer"""
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Equipment
        fields = ['name', 'price', ]


class CartSerializer(serializers.ModelSerializer):
    equipment = CartEquipmentSerializer()
    summ = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'equipment', 'amount', 'summ', 'dates']

    def get_summ(self, obj):
        return obj.amount * obj.equipment.price

    def get_dates(self, obj):
        return {'date_start': obj.date_start, 'date_end': obj.date_end}


class AddCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    amount = serializers.CharField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        date_start = attrs.get('date_start')
        date_end = attrs.get('date_end')
        if date_start and date_end:
            if date_start < date.today():
                raise serializers.ValidationError("Start date cannot be in the past.")
            if date_end <= date_start:
                raise serializers.ValidationError("End date cannot be earlier than start date or the same.")
        return attrs

    class Meta:
        model = Cart
        fields = ['id', 'user', 'equipment', 'amount', 'date_start', 'date_end']
        read_only_fields = ['user', ]
