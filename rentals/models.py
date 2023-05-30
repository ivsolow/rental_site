from django.db import models
from equipment.models import Equipment
from users.models import CustomUser
from django.utils import timezone


class Rentals(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    amount = models.PositiveSmallIntegerField(default=0)
    date_start = models.DateField(default=timezone.now)
    date_end = models.DateField(default=timezone.now)
    is_started = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    # feedback = models.ForeignKey('feedback.Feedback', on_delete=models.CASCADE)

    def __str__(self):
        return self.equipment.name

