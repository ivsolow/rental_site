from django.urls import path
from .views import CartCheckViewSet, PaymentApiView

urlpatterns = [
    path('api/v1/cart_check/', CartCheckViewSet.as_view({'get': 'list'}), name='cartcheck'),
    path('api/v1/payment/', PaymentApiView.as_view(), name='payment'),
]
