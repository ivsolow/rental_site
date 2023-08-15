from rest_framework import serializers

from equipment.models import Equipment
from equipment.serializers import FeedbackPhotoSerializer
from feedback.models import Feedback, FeedbackPhoto
from services.feedback.get_and_create_qurysets import create_feedback_photos, create_feedback_obj


# class FeedbackPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FeedbackPhoto
#         fields = ['photo', ]


class FeedbackEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', ]


class FeedbackSerializer(serializers.ModelSerializer):
    feedback_photo = FeedbackPhotoSerializer(read_only=True, many=True)
    date_created = serializers.DateField(read_only=True)
    equipment = FeedbackEquipmentSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'equipment', 'rate', 'content', 'date_created', 'feedback_photo']


class AddFeedbackSerializer(serializers.ModelSerializer):
    equipment = serializers.IntegerField()
    feedback_photo = serializers.ListField(child=serializers.ImageField(), required=False)

    class Meta:
        model = Feedback
        fields = ['content', 'equipment', 'rate', 'feedback_photo']

    def create(self, validated_data):
        equipment = Equipment.objects.filter(id=validated_data['equipment']).first()
        if not equipment:
            raise serializers.ValidationError("No such equipment")
        user = self.context['request'].user
        feedback = create_feedback_obj(user, equipment, validated_data)

        feedback_photos = validated_data.get('feedback_photo', [])
        create_feedback_photos(feedback, feedback_photos)

        return feedback





