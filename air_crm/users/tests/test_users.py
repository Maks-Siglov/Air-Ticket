import pytest

from django.test import Client
from django.urls import reverse

from users.models import User


@pytest.mark.django_db
def test_register(client: Client):
    response = client.get(reverse('users:register'))
    assert response.status_code == 200

    post_data = {
        "email": "test@gmail.com",
        "password1": "test_password",
        "password2": "test_password",
    }

    response = client.post(reverse('users:register'), data=post_data)
    assert response.status_code == 302

    user = User.objects.get(email="test@gmail.com")
    assert user is not None


def test_login(client: Client, test_user: User):
    response = client.get(reverse('users:login'))
    assert response.status_code == 200

    post_data = {
        "email": "test@gmail.com",
        "password": "test_password"
    }

    response = client.post(reverse('users:login'), data=post_data)
    assert response.status_code == 200


def test_logout(client: Client, test_user: User):
    client.login(email="test@gmail.com", password="test_password")

    response = client.get(reverse('users:logout'))
    assert response.status_code == 302

    forbidden_response = client.get(reverse('customer:profile'))
    assert forbidden_response.status_code == 302


def test_change_password(client: Client, test_user: User):
    client.login(email="test@gmail.com", password="test_password")

    response = client.get(reverse('users:change_password'))
    assert response.status_code == 200

    post_data = {
        "old_password": "test_password",
        "new_password1": "new_test_password",
        "new_password2": "new_test_password"
    }

    response = client.post(reverse('users:change_password'), data=post_data)
    assert response.status_code == 302

    client.logout()

    new_login_post_data = {
        "email": "test@gmail.com",
        "password": "new_test_password"
    }
    response = client.post(reverse('users:login'), data=new_login_post_data)
    assert response.status_code == 200
