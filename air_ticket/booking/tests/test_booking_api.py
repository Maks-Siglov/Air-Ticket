import pytest

from django.test import Client
from django.urls import reverse

from booking.models import Ticket, TicketCart
from customer.models import Contact


@pytest.mark.django_db
def test_create_ticket(client: Client, test_empty_cart: TicketCart):
    cart = test_empty_cart

    post_data = {
        "seat_type": "Economy",
        "first_name": "test_name",
        "last_name": "test_last_name",
        "passport_id": "2155835962",
        "price": 200,
        "lunch": True,
        "luggage": False,
    }

    url = reverse("api-booking:create_ticket", kwargs={"cart_pk": cart.pk})
    response = client.post(url, post_data)

    assert response.status_code == 201

    ticket = Ticket.objects.first()
    assert ticket is not None
    assert ticket.price == post_data["price"]
    assert ticket.lunch == post_data["lunch"]
    assert ticket.luggage == post_data["luggage"]

    passenger = ticket.passenger
    assert passenger.first_name == post_data["first_name"]
    assert passenger.last_name == post_data["last_name"]
    assert passenger.passport_id == post_data["passport_id"]


@pytest.mark.django_db
def test_update_ticket(client: Client, test_cart: TicketCart):
    ticket = Ticket.objects.filter(cart=test_cart).first()

    update_post_data = {
        "seat_type": "Business",
        "first_name": "updated_test_name",
        "last_name": "updated_test_last_name",
        "passport_id": "2155725962",
        "price": 450,
        "lunch": True,
        "luggage": True,
    }

    url = reverse("api-booking:update_ticket", kwargs={"ticket_pk": ticket.pk})
    response = client.put(
        url, update_post_data, content_type="application/json"
    )

    assert response.status_code == 200

    ticket = Ticket.objects.first()
    assert ticket is not None
    assert ticket.price == update_post_data["price"]
    assert ticket.lunch == update_post_data["lunch"]
    assert ticket.luggage == update_post_data["luggage"]

    passenger = ticket.passenger
    assert passenger.first_name == update_post_data["first_name"]
    assert passenger.last_name == update_post_data["last_name"]
    assert passenger.passport_id == update_post_data["passport_id"]


@pytest.mark.django_db
def test_create_contact(client: Client, test_empty_cart: TicketCart):
    cart = test_empty_cart

    post_data = {"phone_number": "0673335623", "email": "test@gmail.com"}

    url = reverse("api-booking:create_contact", kwargs={"cart_pk": cart.pk})
    response = client.post(url, post_data)

    assert response.status_code == 201

    contact = Contact.objects.first()
    assert contact is not None

    assert contact.phone_number == post_data["phone_number"]
    assert contact.email == post_data["email"]


@pytest.mark.django_db
def test_update_contact(client: Client, test_contact: Contact):
    contact = test_contact

    update_post_data = {
        "phone_number": "773258032",
        "email": "new_test@gmail.com",
    }

    url = reverse(
        "api-booking:update_contact", kwargs={"contact_pk": contact.pk}
    )
    response = client.put(
        url, update_post_data, content_type="application/json"
    )

    assert response.status_code == 200

    contact = Contact.objects.first()
    assert contact is not None

    assert contact.phone_number == update_post_data["phone_number"]
    assert contact.email == update_post_data["email"]