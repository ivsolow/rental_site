from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError

from equipment.models import Equipment
from services.equipment.available_equipment import (dates_are_valid,
                                                    get_available_equipment)
from services.equipment.equipment_querysets import (get_list_queryset,
                                                    get_retrieve_queryset)
from equipment.serializers import (
    EquipmentListSerializer,
    EquipmentDetailSerializer,
    EquipmentAvailabilitySerializer,
    AvailableEquipmentSerializer,
)

from services.equipment.decorators_kwargs import (
    EQUIPMENT_LIST_DECORATOR_KWARGS,
    EQUIPMENT_ITEM_DECORATOR_KWARGS,
    AVAIL_EQUIPMENT_DECORATOR_KWARGS,
)


class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['category__name', 'name', 'price', ]

    def get_queryset(self):
        if self.action == 'list':
            return get_list_queryset()
        elif self.action == 'retrieve':
            return get_retrieve_queryset()
        return Equipment.objects.none()

    @extend_schema(**EQUIPMENT_LIST_DECORATOR_KWARGS)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = EquipmentListSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(**EQUIPMENT_ITEM_DECORATOR_KWARGS)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EquipmentDetailSerializer(instance)
        return Response(serializer.data)


class AvailableEquipmentViewSet(viewsets.ViewSet):
    """
    Check for the availability of equipment.
    After entering desired rental dates,
    the user will be presented with available equipment and its quantity
    for those dates.
    """
    serializer_class = AvailableEquipmentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['category__name', 'name', 'price', ]

    @extend_schema(**AVAIL_EQUIPMENT_DECORATOR_KWARGS)
    def list(self, request):
        serializer = EquipmentAvailabilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date_start = serializer.validated_data['date_start']
        date_end = serializer.validated_data['date_end']
        try:
            dates_are_valid(date_start, date_end)
        except ValidationError:
            err_message = {
                "Error": "Check your dates. "
                         "They are either in the past"
                         "or the start date is greater than the end date."
            }
            return Response(err_message, status=status.HTTP_400_BAD_REQUEST)

        equipment = get_available_equipment(date_start, date_end)
        equipment_serializer = AvailableEquipmentSerializer(equipment,
                                                            many=True)

        return Response(equipment_serializer.data)
