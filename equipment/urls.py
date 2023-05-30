from rest_framework import routers
from django.urls import include, path
from equipment.views import EquipmentViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/equipment', EquipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

