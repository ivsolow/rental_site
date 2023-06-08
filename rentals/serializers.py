from rest_framework import serializers

from cart.serializers import CartEquipmentSerializer
from equipment.models import EquipPhoto, Equipment
from rentals.models import Rentals


class EquipPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipPhoto
        fields = ('photo',)


class EquipmentSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        try:
            equip_photo = EquipPhoto.objects.get(equipment=obj)
            return equip_photo.photo.url
        except EquipPhoto.DoesNotExist:
            return None

    class Meta:
        model = Equipment
        fields = ('name', 'description', 'category', 'price', 'photos')


class RentalsSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = Rentals
        fields = ('equipment', 'user', 'amount', 'date_start', 'date_end', 'is_started', 'is_closed')
