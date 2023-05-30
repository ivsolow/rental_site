from django.db import models


class Equipment(models.Model):
    """Модель для снаряжения"""
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category')
    price = models.DecimalField(max_digits=6, decimal_places=1)
    amount = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Снаряжение'
        verbose_name_plural = 'Снаряжение'

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


class Upload:
    """Переменные, используемые в функции upload_path"""
    NAME_CACHE = set()
    PHOTO_ID = 1


def upload_path(instance, filename):
    """Определяем имена файлов и путь для папки хранения фотографий снаряжения"""
    name = instance.equipment_1.name
    if name in Upload.NAME_CACHE:
        Upload.PHOTO_ID += 1
    else:
        Upload.NAME_CACHE.clear()
        Upload.NAME_CACHE.add(name)
        Upload.PHOTO_ID = 1
    filename = '{}_{}.{}'.format(name, Upload.PHOTO_ID, filename.split('.')[-1].lower())
    return '{}/{}'.format(instance.equipment_1.category, filename)


class EquipPhoto(models.Model):
    """Модель для хранения фото снаряжения"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, default=None, null=True)
    photo = models.ImageField(upload_to=upload_path)

    def __str__(self):
        return self.equipment.name
