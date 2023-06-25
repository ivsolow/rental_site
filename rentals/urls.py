from django.urls import path

from .views import RentalsListView

urlpatterns = [
    path('api/v1/rentals/', RentalsListView.as_view(), name='rentals-list'),
]
