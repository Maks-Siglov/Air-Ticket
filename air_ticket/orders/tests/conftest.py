import pytest

from booking.models import TicketCart
from users.tests.conftest import test_user
from booking.tests.conftest import (
    test_cart,
    test_flight,
    test_contact,
    test_airplane_with_seats,
)

from orders.models import Order


@pytest.fixture
def test_order(db, test_cart: TicketCart) -> Order:
    order = Order.objects.create(cart=test_cart, total_price=200)

    yield order

    order.delete()
