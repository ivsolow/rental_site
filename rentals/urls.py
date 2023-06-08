from django.urls import path
from .views import RentalsListView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api/v1/rentals/', RentalsListView.as_view(), name='rentals-list'),
]
