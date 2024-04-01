import pytest

from django.core import mail
from django.test import Client
from django.urls import reverse

from booking.models import TicketCart
from orders.models import Order, OrderTicket
from users.models import User


@pytest.mark.django_db
def test_create_order_without_contact(client: Client, test_cart: TicketCart):
    test_cart.contact = None
    test_cart.save()

    referer_url = reverse("main:index")
    response = client.get(
        reverse("orders:checkout", kwargs={"cart_pk": test_cart.pk}),
        HTTP_REFERER=referer_url,
    )
    assert response.status_code == 302

    order = Order.objects.first()
    assert order is None


def test_order_with_wrong_tickets_amount(
    client: Client, test_cart: TicketCart
):
    test_cart.passenger_amount = 2
    test_cart.save()

    referer_url = reverse("main:index")
    response = client.get(
        reverse("orders:checkout", kwargs={"cart_pk": test_cart.pk}),
        HTTP_REFERER=referer_url,
    )
    assert response.status_code == 302

    order = Order.objects.first()
    assert order is None


def test_create_order(client: Client, test_cart: TicketCart):
    response = client.get(
        reverse("orders:checkout", kwargs={"cart_pk": test_cart.pk}),
    )
    assert response.status_code == 200

    order = Order.objects.first()
    assert order is not None


def test_checkout_return(client: Client, test_order_ticket: OrderTicket):
    order = test_order_ticket.order
    response = client.get(
        reverse("orders:checkout_return", kwargs={"order_pk": order.pk})
    )
    assert response.status_code == 302

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "AirTicket"


def test_auth_checkout_return(
    client: Client, test_order_ticket: OrderTicket, test_user: User
):
    client.login(email="test@gmail.com", password="test_password")
    order = test_order_ticket.order
    response = client.get(
        reverse("orders:checkout_return", kwargs={"order_pk": order.pk})
    )
    assert response.status_code == 302

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "AirTicket"


def test_order_detail(client: Client, test_order: Order):
    response = client.get(
        reverse("orders:detail", kwargs={"order_pk": test_order.pk})
    )
    assert response.status_code == 200
