from rest_framework import routers
from django.urls import include, path

from equipment.views import EquipmentViewSet, AvailableEquipmentViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/equipment', EquipmentViewSet, basename='equipment')
router.register(r'api/v1/equipment_dates', AvailableEquipmentViewSet, basename='free_equipment')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

