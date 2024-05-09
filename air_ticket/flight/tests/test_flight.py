from django.test import Client
from django.urls import reverse

import pytest
from flight.models import Flight


@pytest.mark.django_db
def test_search_flights(client: Client):
    post_data = {
        "departure_airport": "Vienna",
        "arrival_airport": "Berlin",
        "departure_date": "2024-03-03 00:00:00+02:00",
        "passenger_amount": 2,
    }

    response = client.post(reverse("flight:search"), post_data)

    assert response.status_code == 200


def test_flight_details(client: Client, test_flight: Flight):
    response = client.get(
        reverse("flight:detail", kwargs={"flight_pk": test_flight.pk})
    )
    assert response.status_code == 302
