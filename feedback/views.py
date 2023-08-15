from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from feedback.serializers import (
    FeedbackSerializer,
    AddFeedbackSerializer,
    FeedbackEquipmentSerializer
)
from services.feedback.get_and_create_qurysets import get_feedback_queryset, get_equipment_for_feedback_queryset
from services.feedback.decorators_kwargs import (
    FEEDBACK_CREATE_DECORATOR_KWARGS,
    EQUIPMENT_FOR_FEEDBACK_DECORATOR_KWARGS,
    FEEDBACK_UPDATE_DECORATOR_KWARGS,
    FEEDBACK_LIST_DECORATOR_KWARGS,
    FEEDBACK_DELETE_DECORATOR_KWARGS,
    FEEDBACK_RETRIEVE_DECORATOR_KWARGS
)


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, ]

    @extend_schema(**EQUIPMENT_FOR_FEEDBACK_DECORATOR_KWARGS)
    @action(detail=False, methods=['get'])
    def get_equipment_for_feedback(self, request):
        user = request.user
        equipment_for_feedback_queryset = get_equipment_for_feedback_queryset(user)
        serializer = FeedbackEquipmentSerializer(equipment_for_feedback_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        return get_feedback_queryset(user)

    @extend_schema(**FEEDBACK_LIST_DECORATOR_KWARGS)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(**FEEDBACK_RETRIEVE_DECORATOR_KWARGS)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(**FEEDBACK_CREATE_DECORATOR_KWARGS)
    def create(self, request, *args, **kwargs):
        serializer = AddFeedbackSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        feedback = serializer.save()
        response_serializer = FeedbackSerializer(feedback)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(**FEEDBACK_UPDATE_DECORATOR_KWARGS)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(**FEEDBACK_DELETE_DECORATOR_KWARGS)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance_id = instance.id
            self.perform_destroy(instance)
            message_data = {"id": instance_id}
            return Response(data=message_data, status=status.HTTP_200_OK)
        else:
            message_data = {"detail": "Object not found."}
            return Response(data=message_data, status=status.HTTP_400_BAD_REQUEST)
