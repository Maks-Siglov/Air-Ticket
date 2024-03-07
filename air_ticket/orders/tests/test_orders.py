import pytest

from django.test import Client
from django.urls import reverse

from booking.models import Ticket, TicketCart
from booking.tests.conftest import (
    test_airplane_with_seats,
    test_cart,
    test_contact,
    test_flight,
    test_ticket,
)
from customer.models import Contact
from orders.models import Order


@pytest.mark.django_db
def test_create_order_without_contact(client: Client, test_cart: TicketCart):
    referer_url = reverse("main:index")
    response = client.get(
        reverse("orders:checkout", kwargs={"cart_pk": test_cart.pk}),
        HTTP_REFERER=referer_url,
    )
    assert response.status_code == 302

    order = Order.objects.first()
    assert order is None


def test_create_order_with_wrong_tickets(
    client: Client, test_ticket: Ticket, test_contact: Contact
):
    cart = test_ticket.cart
    cart.contact = test_contact

    referer_url = reverse("main:index")
    response = client.get(
        reverse("orders:checkout", kwargs={"cart_pk": cart.pk}),
        HTTP_REFERER=referer_url,
    )
    assert response.status_code == 302

    order = Order.objects.first()
    assert order is None


def test_create_order(
    client: Client, test_ticket: Ticket, test_contact: Contact
):
    cart = test_ticket.cart
    cart.contact = test_contact
    cart.passenger_amount = 1
    cart.save()

    response = client.get(
        reverse("orders:checkout", kwargs={"cart_pk": cart.pk}),
    )
    assert response.status_code == 200

    order = Order.objects.first()
    assert order is not None
