from django.db import models
from django.utils import timezone

from equipment.models import Equipment
from users.models import CustomUser


class Rentals(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    amount = models.PositiveSmallIntegerField(default=0)
    date_start = models.DateField(default=timezone.now)
    date_end = models.DateField(default=timezone.now)
    is_started = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.equipment.name}: {self.date_start} - {self.date_end}'

