from django.contrib import admin

from equipment.models import EquipPhoto, Equipment, Category


# Добавление дополнительных полей фото для загрузки
class EquipPhotoInline(admin.TabularInline):
    model = EquipPhoto
    extra = 10


class EquipmentAdmin(admin.ModelAdmin):
    inlines = [EquipPhotoInline, ]


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Category)
