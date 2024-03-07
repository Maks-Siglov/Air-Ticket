import pytest

from users.models import User


@pytest.fixture
def test_user(db) -> User:
    user = User.objects.create_user(
        email="test@gmail.com",
        password="test_password",
    )
    yield user

    user.delete()
