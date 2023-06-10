from rest_framework import serializers
from equipment.models import Equipment
from rentals.models import Rentals
from services.equipment.available_equipment import get_equipment_photo


class EquipmentSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    category = serializers.CharField()

    class Meta:
        model = Equipment
        fields = '__all__'

    def get_photo(self, obj):
        return get_equipment_photo(obj)


class EquipmentAvailabilitySerializer(serializers.ModelSerializer):
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    class Meta:
        model = Rentals
        fields = '__all__'


class AvailableEquipmentSerializer(serializers.ModelSerializer):
    available_amount = serializers.IntegerField()
    category = serializers.CharField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        exclude = ['amount', ]

    def get_photo(self, obj):
        return get_equipment_photo(obj)

