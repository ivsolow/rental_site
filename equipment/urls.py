from django.urls import path, include

from rest_framework import routers

from equipment.views import EquipmentViewSet, AvailableEquipmentViewSet


router = routers.DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')

urlpatterns = [
    # path('api/v1/equipment/', EquipmentViewSet.as_view({'get': 'list'}), name='equipment'),
    path('api/v1/', include(router.urls)),
    path('api/v1/equipment_dates/', AvailableEquipmentViewSet.as_view({'get': 'list'}), name='free_equipment'),
]
