from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache

from users.models import CustomUser


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    equipment = models.ForeignKey('equipment.Equipment',
                                  on_delete=models.PROTECT)
    amount = models.PositiveSmallIntegerField(default=1)
    date_start = models.DateField(default=timezone.now)
    date_end = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(settings.CART_LIST_CACHE_KEY)

    def __str__(self):
        return self.user.email
