from django.db import models


class Feedback(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    content = models.CharField(max_length=1000)
    rental = models.ForeignKey('rentals.Rentals', on_delete=models.PROTECT)
    date_created = models.DateField()
    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f'{self.rental.user.first_name} about {self.rental.equipment.name}'


def upload_path(instance, filename):
    """Определяем путь для папки хранения фотографий отзывов"""
    name = instance.equipment_1.name
    return '{}/{}'.format(instance.rental.equipment_1, filename)


class FeedbackPhoto(models.Model):
    equipment = models.ForeignKey(Feedback, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to=upload_path)
