import pytest
from equipment.models import Equipment, Category


@pytest.mark.django_db
def test_equipment():
    # Создание объекта снаряжения
    category = Category.objects.create(name='Hiking')
    equipment = Equipment.objects.create(
        name='Tent MSR Freelite 2',
        category=category,
        description='Good balance of weight & livability for solo hikers',
        price=1000,
        amount=10
    )

    # проверка полей
    assert equipment.name == 'Tent MSR Freelite 2'
    assert equipment.category == category
    assert equipment.description == 'Good balance of weight & livability for solo hikers'
    assert equipment.price == 1000
    assert equipment.amount == 10

    # проверка количества добавленных объектов
    category = Category.objects.create(name='Hiking')
    equipment = Equipment.objects.create(
        name='Giant Trance Advanced Pro',
        category=category,
        description='best for enduro mountain bike',
        price=3000,
        amount=5
    )
    query = Equipment.objects.all()
    assert len(query) == 2

