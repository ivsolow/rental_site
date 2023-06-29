from django.urls import path, include
from rest_framework import routers

from .views import FeedbackViewSet

router = routers.DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/equipment_for_feedback/',
         FeedbackViewSet.as_view({'get': 'get_equipment_for_feedback'}),
         name='feedback-available-equipment'),
]
