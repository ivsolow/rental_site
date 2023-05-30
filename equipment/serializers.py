from rest_framework import serializers
from equipment.models import Equipment, EquipPhoto


class EquipmentSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    category = serializers.CharField()

    def get_photo(self, obj):
        try:
            equip_photo = EquipPhoto.objects.get(equipment=obj)
            return equip_photo.photo.url
        except EquipPhoto.DoesNotExist:
            return None

    class Meta:
        model = Equipment
        fields = '__all__'
