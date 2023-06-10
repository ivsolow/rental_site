from rest_framework import serializers

from cart.models import Cart
from equipment.models import Equipment
from services.equipment.available_equipment import get_equipment_photo


class CartEquipmentSerializer(serializers.ModelSerializer):
    """Поле equipment сериализатора CartSerializer"""

    photo = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount = serializers.IntegerField()

    def get_photo(self, obj):
        return get_equipment_photo(obj)

    class Meta:
        model = Equipment
        fields = ['name', 'category', 'description', 'price', 'photo', 'amount']


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
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), source='equipment.id')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'equipment', 'amount', 'date_start', 'date_end']
        read_only_fields = ['user', ]
