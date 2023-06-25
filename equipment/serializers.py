from rest_framework import serializers

from equipment.models import Equipment, EquipPhoto
from rentals.models import Rentals


class EquipPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipPhoto
        fields = ['photo', ]


class EquipmentSerializer(serializers.ModelSerializer):
    photos = EquipPhotoSerializer(many=True, read_only=True)
    category = serializers.CharField()

    class Meta:
        model = Equipment
        fields = '__all__'


class EquipmentAvailabilitySerializer(serializers.ModelSerializer):
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    class Meta:
        model = Rentals
        fields = '__all__'


class AvailableEquipmentSerializer(serializers.ModelSerializer):
    available_amount = serializers.IntegerField()
    category = serializers.CharField()
    photos = EquipPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Equipment
        exclude = ['amount', ]
