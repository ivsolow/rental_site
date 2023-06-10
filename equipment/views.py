from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer, EquipmentAvailabilitySerializer, AvailableEquipmentSerializer
from services.equipment.available_equipment import dates_is_valid, get_available_equipment


class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all().order_by('id')
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['category__name', 'name', 'price', ]


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
        if not dates_is_valid(date_start, date_end):
            return Response({'error': 'You cannot choose past time'}, status=status.HTTP_400_BAD_REQUEST)

        equipment = get_available_equipment(date_start, date_end)
        equipment_serializer = AvailableEquipmentSerializer(equipment, many=True)

        return Response(equipment_serializer.data)
