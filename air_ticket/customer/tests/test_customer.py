from django.test import Client
from django.urls import reverse

from users.models import User


def test_profile(client: Client, test_user: User):
    client.login(email="test@gmail.com", password="test_password")

    response = client.get(reverse("customer:profile"))

    assert response.status_code == 200


def test_customer_orders(client: Client, test_user: User):
    client.login(email="test@gmail.com", password="test_password")

    response = client.get(reverse("customer:orders"))

    assert response.status_code == 200


def test_customer_flights(client: Client, test_user: User):
    client.login(email="test@gmail.com", password="test_password")

    response = client.get(reverse("customer:flights"))

    assert response.status_code == 200


def test_customer_check_in(client: Client, test_user: User):
    client.login(email="test@gmail.com", password="test_password")

    response = client.get(reverse("customer:check-in"))

    assert response.status_code == 200
