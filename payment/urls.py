from django.urls import path

from .views import (CartCheckViewSet,
                    PaymentApiView,
                    YookassaResponseApiView,
                    PaymentStatusApiView)


urlpatterns = [
    path('api/v1/cart_check/',
         CartCheckViewSet.as_view({'get': 'list'}),
         name='cart_check'),
    path('api/v1/payment/',
         PaymentApiView.as_view(),
         name='payment'),
    path('api/v1/payment_response/',
         YookassaResponseApiView.as_view(),
         name='payment_response'),
    path('api/v1/payment_status/',
         PaymentStatusApiView.as_view(),
         name='payment_status'),
]
