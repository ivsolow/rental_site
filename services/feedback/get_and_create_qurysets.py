from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models.query import QuerySet

from equipment.models import Equipment
from feedback.models import Feedback, FeedbackPhoto
from rentals.models import Rentals
from users.models import CustomUser


@receiver(pre_delete, sender=CustomUser)
def set_user_deleted(sender, instance: CustomUser, **kwargs) -> None:
    """
    When a user requests to delete their account,
     their associated feedback will not be removed.
    Instead, the feedback will be transferred to another
     user identified as 'Deleted_user@rentals.com'.
    This action is managed through the "pre_delete" signal.
    """
    deleted_user, created = (CustomUser.objects.
                             get_or_create(email='Deleted_user@rentals.com'))
    feedback_list = Feedback.objects.filter(user=instance)
    for feedback in feedback_list:
        feedback.user = deleted_user
        feedback.save()


def get_feedback_queryset(user: CustomUser) -> QuerySet:
    queryset = (
        Feedback.objects.filter(user=user)
        .select_related('equipment')
        .prefetch_related('feedback_photo')
    )

    return queryset


def get_equipment_for_feedback_queryset(user: CustomUser) -> QuerySet:
    """
    Retrieves equipment available for feedback
    submission by the user. This equipment includes
     items that the user rented and have the 'is_closed' flag set to True.
    """
    rented_equipment = (
        Rentals.objects.filter(user=user, is_started=True, is_closed=True)
        .values_list('equipment', flat=True)
        )
    feedback_equipment = (Feedback.objects.filter(user=user).
                          values_list('equipment', flat=True))
    queryset = (Equipment.objects.filter(id__in=rented_equipment).
                exclude(id__in=feedback_equipment))
    return queryset


def create_feedback_photos(feedback: QuerySet, feedback_photos: list) -> None:
    for photo in feedback_photos:
        FeedbackPhoto.objects.create(feedback=feedback, photo=photo)
    return


def create_feedback_obj(user: CustomUser,
                        equipment: Equipment,
                        validated_data: dict) -> QuerySet:
    feedback = Feedback.objects.create(
        user=user,
        content=validated_data['content'],
        equipment=equipment,
        rate=validated_data['rate']
    )

    return feedback
