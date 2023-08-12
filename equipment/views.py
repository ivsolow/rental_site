from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from equipment.models import Equipment
from equipment.serializers import EquipmentListSerializer, EquipmentDetailSerializer, EquipmentAvailabilitySerializer, \
    AvailableEquipmentSerializer
from services.equipment.available_equipment import dates_is_valid, get_available_equipment
from services.equipment.equipment_querysets import get_list_queryset, get_retrieve_queryset


class EquipmentViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['category__name', 'name', 'price', ]

    # @extend_schema(tags=["Posts"])
    def get_queryset(self):
        if self.action == 'list':
            return get_list_queryset()
        elif self.action == 'retrieve':
            return get_retrieve_queryset()
        return Equipment.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = EquipmentListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EquipmentDetailSerializer(instance)
        return Response(serializer.data)


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
        try:
            dates_is_valid(date_start, date_end)
        except ValidationError:
            return Response({'error': 'You cannot choose past time'}, status=status.HTTP_400_BAD_REQUEST)

        equipment = get_available_equipment(date_start, date_end)
        equipment_serializer = AvailableEquipmentSerializer(equipment, many=True)

        return Response(equipment_serializer.data)
