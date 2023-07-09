from django.db.models import Avg, Prefetch

from equipment.models import Equipment
from users.models import CustomUser


def get_list_queryset():
    queryset = (
        Equipment.objects.all()
        .select_related('category')
        .prefetch_related('photos')
        .annotate(rating=Avg('eq_feedback__rate'))
    )
    return queryset


def get_retrieve_queryset():
    queryset = (
        Equipment.objects.all()
        .select_related('category')
        .prefetch_related('photos',
                          'eq_feedback',
                          'eq_feedback__feedback_photo',
                          Prefetch('eq_feedback__user',
                                   queryset=CustomUser.objects.only('id', 'first_name'))
                          )
                    )
    return queryset
