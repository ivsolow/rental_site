from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rentals.models import Rentals
from rentals.serializers import RentalsSerializer


from rest_framework.generics import ListAPIView
from .models import Rentals
from .serializers import RentalsSerializer


class RentalsListView(ListAPIView):
    serializer_class = RentalsSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Rentals.objects.filter(user=user).order_by('equipment__name')

