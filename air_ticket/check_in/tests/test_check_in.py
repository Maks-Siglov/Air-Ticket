from django.test import Client
from django.urls import reverse

import pytest
from orders.models import Order
from users.models import User


@pytest.mark.django_db
def test_check_id(client: Client, test_order: Order, test_user: User):
    client.login(email="test@gmail.com", password="test_password")

    url = reverse("check_in:check_in", kwargs={"order_pk": test_order.pk})
    response = client.get(url)

    assert response.status_code == 200
