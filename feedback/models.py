from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from equipment.models import Equipment
from rentals.models import Rentals
from users.models import CustomUser


@receiver(pre_delete, sender=CustomUser)
def set_user_deleted(sender, instance, **kwargs):
    Feedback.objects.filter(user=instance).update(user='Deleted')


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
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f'{self.user.first_name} about {self.equipment.name}'


# def upload_path(instance, filename):
#     """Определяем путь для папки хранения фотографий отзывов"""
#     name = instance.equipment
#     return '{}/{}/{}'.format("Feedback", name, filename)

class Upload:
    """Переменные, используемые в функции upload_path"""
    NAME_CACHE = set()
    PHOTO_ID = 1


def upload_path(instance, filename):
    """Определяем имена файлов и путь для папки хранения фотографий снаряжения"""
    name = instance.feedback.equipment.name
    if name in Upload.NAME_CACHE:
        Upload.PHOTO_ID += 1
    else:
        Upload.NAME_CACHE.clear()
        Upload.NAME_CACHE.add(name)
        Upload.PHOTO_ID = 1
    filename = '{}_{}.{}'.format(name, Upload.PHOTO_ID, filename.split('.')[-1].lower())
    return '{}/{}/{}'.format("Feedback", instance.feedback, filename)


class FeedbackPhoto(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.PROTECT, related_name='feedback_photo')
    photo = models.ImageField(upload_to=upload_path)
