from _decimal import Decimal

from rest_framework import serializers

from equipment.models import Equipment, EquipPhoto
from feedback.models import Feedback, FeedbackPhoto
from rentals.models import Rentals


class EquipPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipPhoto
        fields = ['photo', ]


class FeedbackPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackPhoto
        fields = ['photo', ]


class EquipmentFeedbackSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    feedback_photos = FeedbackPhotoSerializer(many=True,
                                              read_only=True,
                                              source='feedback_photo')

    class Meta:
        model = Feedback
        fields = ('id', 'username', 'content', 'rate', 'feedback_photos')

    def get_username(self, obj) -> str:
        name = obj.user.first_name
        if not name:
            name = 'user'
        return name


class EquipmentBaseSerializer(serializers.ModelSerializer):
    photos = EquipPhotoSerializer(many=True, read_only=True)
    category = serializers.CharField()

    class Meta:
        model = Equipment
        fields = '__all__'


class EquipmentDetailSerializer(EquipmentBaseSerializer):
    feedback = EquipmentFeedbackSerializer(many=True,
                                           read_only=True,
                                           source='eq_feedback')


class EquipmentListSerializer(EquipmentBaseSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj) -> Decimal:
        average = obj.rating
        if average is not None:
            average = Decimal(average).quantize(Decimal('0.00'))
        return average


class EquipmentAvailabilitySerializer(serializers.ModelSerializer):
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    class Meta:
        model = Rentals
        fields = '__all__'


class AvailableEquipmentSerializer(EquipmentListSerializer):
    available_amount = serializers.IntegerField()

    class Meta:
        model = Equipment
        exclude = ['amount', ]
