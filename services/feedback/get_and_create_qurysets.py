from equipment.models import Equipment
from feedback.models import Feedback, FeedbackPhoto
from rentals.models import Rentals


def get_feedback_queryset(user):
    queryset = (
        Feedback.objects.filter(user=user)
        .select_related('equipment')
        .prefetch_related('feedback_photo')
    )
    return queryset


def get_equipment_for_feedback_queryset(user):
    rented_equipment = Rentals.objects.filter(user=user).values_list('equipment', flat=True)
    feedback_equipment = Feedback.objects.filter(user=user).values_list('equipment', flat=True)
    queryset = Equipment.objects.filter(id__in=rented_equipment).exclude(id__in=feedback_equipment)
    return queryset


def create_feedback_photos(feedback, feedback_photos):
    for photo in feedback_photos:
        FeedbackPhoto.objects.create(feedback=feedback, photo=photo)
    return


def create_feedback_obj(user, equipment, validated_data):
    feedback = Feedback.objects.create(
        user=user,
        content=validated_data['content'],
        equipment=equipment,
        rate=validated_data['rate']
    )
    return feedback
