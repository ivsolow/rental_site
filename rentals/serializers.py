from rest_framework import serializers

from equipment.serializers import EquipmentSerializer
from rentals.models import Rentals


class RentalsSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = Rentals
        fields = ('equipment', 'amount', 'date_start', 'date_end', 'is_started', 'is_closed')
