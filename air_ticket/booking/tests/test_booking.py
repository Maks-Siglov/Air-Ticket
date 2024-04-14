from django.test import Client
from django.urls import reverse

import pytest
from booking.models import TicketCart
from flight.models import Flight


@pytest.mark.django_db
def test_create_cart(client: Client, test_flight: Flight):
    flight = test_flight
    passenger_amount = 2

    url = reverse("booking:create_order", kwargs={"flight_pk": flight.pk})
    url += f"?passenger_amount={passenger_amount}"

    response = client.get(url)
    assert response.status_code == 302

    cart = TicketCart.objects.first()
    assert cart is not None

    assert cart.flight == flight
    assert cart.passenger_amount == passenger_amount


@pytest.mark.django_db
def test_book(client: Client, test_cart: TicketCart):
    cart = test_cart

    response = client.get(reverse("booking:book", kwargs={"cart_pk": cart.pk}))
    assert response.status_code == 200
