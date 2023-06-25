from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from services.rentals.rentals_queryset import get_rentals_queryset
from .serializers import RentalsSerializer


class RentalsListView(ListAPIView):
    serializer_class = RentalsSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return get_rentals_queryset(user)
