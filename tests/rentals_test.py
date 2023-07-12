import datetime

import pytest

from django.urls import reverse

from rentals.models import Rentals
from .equipment_test import equipment_1, equipment_2, user, api_client


@pytest.fixture
def rental_create(api_client, equipment_1, user):
    today = datetime.date.today()
    delta = datetime.timedelta(days=5)
    rental = Rentals.objects.create(
        equipment=equipment_1,
        user=user,
        amount=10,
        date_start=f'{today}',
        date_end=f'{today + delta}'
    )
    return


@pytest.fixture
def rental_create_2(api_client, equipment_2, user):
    today = datetime.date.today()
    delta = datetime.timedelta(days=6)
    rental = Rentals.objects.create(
        equipment=equipment_2,
        user=user,
        amount=5,
        date_start=f'{today}',
        date_end=f'{today + delta}'
    )
    return


@pytest.fixture
def closed_rental_create(api_client, equipment_1, user):
    today = datetime.date.today()
    delta = datetime.timedelta(days=7)
    rental = Rentals.objects.create(
        equipment=equipment_1,
        user=user,
        amount=5,
        date_start=f'{today}',
        date_end=f'{today + delta}',
        is_started=True,
        is_closed=True
    )
    return


@pytest.mark.django_db
def test_rentals_list(api_client, user, rental_create, rental_create_2):
    url = reverse('rentals-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['equipment']['name'] == 'Giant Trance Advanced Pro'
    assert response.data[0]['date_start'] == str(datetime.date.today())
