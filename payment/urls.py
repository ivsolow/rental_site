from django.urls import path
from .views import CartCheckViewSet, PaymentApiView, YookassaResponseApiView, PaymentStatusApiView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api/v1/cart_check/', CartCheckViewSet.as_view({'get': 'list'}), name='cartcheck'),
    path('api/v1/payment/', PaymentApiView.as_view(), name='payment'),
    path('api/v1/payment_response/', YookassaResponseApiView.as_view(), name='payment_response'),
    path('api/v1/payment_status/', PaymentStatusApiView.as_view(), name='payment_status'),
]
