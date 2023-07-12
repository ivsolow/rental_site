
class Upload:
    """Переменные, используемые в функции upload_path"""
    NAME_CACHE: dict = {}
    PHOTO_ID: int = 1


def get_unique_filename(name: str, extension: str) -> str:
    """Генерирует уникальное имя файла"""
    if name in Upload.NAME_CACHE:
        Upload.NAME_CACHE[name] += 1
    else:
        Upload.NAME_CACHE[name] = 1
    return f'{name}_{Upload.NAME_CACHE[name]}.{extension}'


def upload_path(instance, filename: str) -> str:
    """Определяет имена файлов и путь для папки хранения фотографий"""

    from equipment.models import EquipPhoto
    from feedback.models import FeedbackPhoto

    if isinstance(instance, FeedbackPhoto):
        name = instance.feedback.equipment.name
        folder = 'Feedback'
    elif isinstance(instance, EquipPhoto):
        name = instance.equipment.name
        folder = 'Equipment'
    else:
        raise ValueError("Invalid instance type")

    extension = filename.split('.')[-1].lower()
    filename = get_unique_filename(name, extension)

    return f'{folder}/{instance}/{filename}'
