from django.conf import settings
from django.core.cache import cache

from rentals.models import Rentals


def get_rentals_queryset(user):
    cache_key = settings.RENTALS_CACHE_KEY
    rentals_queryset = cache.get(cache_key)
    if not rentals_queryset:
        rentals_queryset = (
            Rentals.objects.filter(user=user)
            .order_by('equipment__name')
            .select_related('equipment__category')
            .prefetch_related('equipment__photos')
        )

    cache.set(cache_key, rentals_queryset, 60 * 10)

    return rentals_queryset
