from datetime import date

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from equipment.models import Equipment
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer, AddFeedbackSerializer, FeedbackEquipmentSerializer
from rentals.models import Rentals
from services.feedback.get_and_create_qurysets import get_feedback_queryset, get_equipment_for_feedback_queryset


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=False, methods=['get'])
    def get_equipment_for_feedback(self, request):
        user = request.user
        equipment_for_feedback_queryset = get_equipment_for_feedback_queryset(user)
        serializer = FeedbackEquipmentSerializer(equipment_for_feedback_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        return get_feedback_queryset(user)

    def create(self, request, *args, **kwargs):
        serializer = AddFeedbackSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        feedback = serializer.save()
        response_serializer = FeedbackSerializer(feedback)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)