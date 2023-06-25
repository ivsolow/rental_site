from django.urls import path

from equipment.views import EquipmentViewSet, AvailableEquipmentViewSet


urlpatterns = [
    path('api/v1/equipment/', EquipmentViewSet.as_view({'get': 'list'}), name='equipment'),
    path('api/v1/equipment_dates/', AvailableEquipmentViewSet.as_view({'get': 'list'}), name='free_equipment'),
]
