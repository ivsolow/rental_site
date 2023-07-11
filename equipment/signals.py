from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.cache import cache

from feedback.models import Feedback
from .models import Equipment
from django.conf import settings


@receiver(post_delete, sender=Feedback)
@receiver(post_delete, sender=Equipment)
def delete_equipment_cache(sender, instance, **kwargs):
    cache.delete(settings.EQUIPMENT_LIST_CACHE_KEY)
    cache.delete(settings.EQUIPMENT_RETRIEVE_CACHE_KEY)
