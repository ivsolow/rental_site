from django.db import models

from equipment.models import Equipment
from services.equipment.upload_photos_path import upload_path
from users.models import CustomUser


class Feedback(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=1000)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True)
    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f'{self.user.email} about {self.equipment.name}'


class FeedbackPhoto(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.PROTECT, null=True, related_name='feedback_photo')
    photo = models.ImageField(upload_to=upload_path)

    def __str__(self):
        return f"{self.feedback.user.email} about {self.feedback.equipment.name}"
