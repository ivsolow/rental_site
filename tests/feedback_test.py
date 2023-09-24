from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status

from equipment.models import Equipment
from .equipment_test import (user,  # noqa: F401
                             api_client,
                             equipment_1,
                             equipment_2)
from .rentals_test import (rental_create,  # noqa: F401
                           rental_create_2,
                           closed_rental_create)
from feedback.models import Feedback


@pytest.fixture
def feedback_1(user, api_client, equipment_1):  # noqa: F811
    eq_id_1 = equipment_1.id
    data = {
        'content': 'Test feedback',
        'equipment': eq_id_1,
        'rate': 5
    }
    response = api_client.post(reverse('feedback-list'),
                               data=data,
                               format='json')
    return response


@pytest.fixture
def feedback_2(user, api_client, equipment_2):  # noqa: F811
    eq_id_2 = equipment_2.id
    data = {
        'content': 'Test feedback 2',
        'equipment': eq_id_2,
        'rate': 4
    }
    response = api_client.post(reverse('feedback-list'),  # noqa: F811
                               data=data,
                               format='json')
    return response


@pytest.fixture
def feedback_3(user, api_client, equipment_2):  # noqa: F811
    eq_id_2 = equipment_2.id
    data = {
        'content': 'Test feedback 3',
        'equipment': eq_id_2,
        'rate': 3
    }
    response = api_client.post(reverse('feedback-list'),
                               data=data,
                               format='json')
    return response


@pytest.mark.django_db
def test_create_feedback(feedback_1):
    response = feedback_1
    assert response.status_code == status.HTTP_201_CREATED
    assert Feedback.objects.count() == 1
    feedback = Feedback.objects.first()
    assert feedback.content == 'Test feedback'
    assert feedback.equipment.id == 1
    assert feedback.rate == 5


@pytest.mark.django_db
def test_create_invalid_feedback(api_client):  # noqa: F811
    data = {
        'content': 'Test invalid feedback',
        'equipment': 10,
        'rate': 5
    }

    response = api_client.post(reverse('feedback-list'),
                               data=data,
                               format='json')
    assert response.data[0] == 'No such equipment'
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_feedback_list(user,  # noqa: F811
                           api_client,  # noqa: F811
                           feedback_1,
                           feedback_2):
    client = api_client
    response = feedback_2
    print(response.data, response.status_code)
    eq = Equipment.objects.filter(id=2)
    print(eq)
    response = client.get(reverse('feedback-list'))
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == Feedback.objects.count()
    assert len(response.data) == 2
    assert response.data[0]['equipment']['id'] == 1
    assert response.data[1]['rate'] == 4
    assert response.data[1]['equipment']['name'] == 'Giant Trance Advanced Pro'
    assert response.data[1]['date_created'] == str(date.today())


@pytest.mark.django_db
def test_no_equipment_for_feedback(user,  # noqa: F811
                                   api_client,  # noqa: F811
                                   rental_create,  # noqa: F811
                                   rental_create_2):  # noqa: F811
    url = reverse('feedback-available-equipment')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_one_equipment_for_feedback(user,  # noqa: F811
                                    api_client,  # noqa: F811
                                    closed_rental_create):  # noqa: F811
    url = reverse('feedback-available-equipment')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Tent MSR Freelite 2'
