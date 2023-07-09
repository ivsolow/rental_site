from rest_framework import serializers

from equipment.models import Equipment
from equipment.serializers import EquipPhotoSerializer
from rentals.models import Rentals


class EquipmentSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    photos = EquipPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'category', 'photos']


class RentalsSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(read_only=True)

    class Meta:
        model = Rentals
        fields = ('equipment', 'amount', 'date_start', 'date_end', 'is_started', 'is_closed')
