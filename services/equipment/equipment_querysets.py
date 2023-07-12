from django.db.models import Avg, Prefetch
from django.core.cache import cache
from django.conf import settings

from equipment.models import Equipment
from users.models import CustomUser


def get_list_queryset():
    cache_key = settings.EQUIPMENT_LIST_CACHE_KEY
    equipment_list = cache.get(cache_key)
    if not equipment_list:
        equipment_list = (
            Equipment.objects.all()
            .select_related('category')
            .prefetch_related('photos')
            .annotate(rating=Avg('eq_feedback__rate'))
            .order_by('id')
        )

        cache.set(cache_key, equipment_list, 60 * 10)
    return equipment_list


def get_retrieve_queryset():
    cache_key = settings.EQUIPMENT_RETRIEVE_CACHE_KEY
    equipment_item = cache.get(cache_key)
    if not equipment_item:
        equipment_item = (
            Equipment.objects.all()
            .select_related('category')
            .prefetch_related('photos',
                              'eq_feedback',
                              'eq_feedback__feedback_photo',
                              Prefetch('eq_feedback__user',
                                       queryset=CustomUser.objects.only('id', 'first_name'))
                              )
                        )

        cache.set(cache_key, equipment_item, 60 * 10)
    return equipment_item

