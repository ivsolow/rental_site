from django.urls import path

from cart.views import CartViewSet


urlpatterns = [
    path(
        'api/v1/cart',
        CartViewSet.as_view({'get': 'list'}),
        name='cart'
    ),
    path(
        'api/v1/add_cart/',
        CartViewSet.as_view({'post': 'create'}),
        name='add_cart'
    ),
    path(
        'api/v1/remove_from_cart/<int:pk>/<int:amount>/',
        CartViewSet.as_view({'delete': 'destroy'}),
        name='cart_delete'
    ),
]
