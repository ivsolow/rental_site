from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all().order_by('id')
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['category__name', 'name', 'price', ]
