from django.db import models
from django.core.cache import cache
from django.conf import settings

from services.equipment.upload_photos_path import upload_path


class Equipment(models.Model):
    """Модель для снаряжения"""
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=1)
    amount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 related_name='category')

    class Meta:
        verbose_name = 'Снаряжение'
        verbose_name_plural = 'Снаряжение'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(settings.EQUIPMENT_LIST_CACHE_KEY)
        cache.delete(settings.EQUIPMENT_RETRIEVE_CACHE_KEY)
        cache.delete(settings.AVAIL_EQUIPMENT_CACHE_KEY)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий"""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class EquipPhoto(models.Model):
    """Модель для хранения фото снаряжения"""
    photo = models.ImageField(upload_to=upload_path)
    equipment = models.ForeignKey(Equipment,
                                  on_delete=models.CASCADE,
                                  default=None, null=True,
                                  related_name='photos')

    def __str__(self):
        return self.equipment.name
