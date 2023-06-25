from django.urls import include, path
from rest_framework import routers

from cart.views import CartViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/cart', CartViewSet.as_view({'get': 'list'}), name='cart'),
    path('api/v1/remove_from_cart/<int:pk>/<int:amount>/',
         CartViewSet.as_view({'delete': 'destroy'}), name='cart_delete'),
    path('api/v1/add_cart/', CartViewSet.as_view({'post': 'create'}), name='add_cart'),
    ]
