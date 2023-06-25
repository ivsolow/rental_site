from rentals.models import Rentals


def get_rentals_queryset(user):
    queryset = (
        Rentals.objects.filter(user=user)
        .order_by('equipment__name')
        .select_related('equipment__category')
        .prefetch_related('equipment__photos')
    )

    return queryset
