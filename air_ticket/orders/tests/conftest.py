import pytest

from booking.models import TicketCart, Ticket
from flight.models import Flight
from orders.models.order_ticket import OrderTicket
from users.tests.conftest import test_user
from booking.tests.conftest import (
    test_cart,
    test_flight,
    test_contact,
    test_airplane_with_seats,
)

from orders.models import Order


@pytest.fixture
def test_order(db, test_flight: Flight) -> Order:
    order = Order.objects.create(total_price=200, flight=test_flight)

    yield order

    order.delete()


@pytest.fixture
def test_order_ticket(
    db, test_order: Order, test_cart: TicketCart
) -> OrderTicket:
    ticket = Ticket.objects.first()
    order_ticket = OrderTicket.objects.create(order=test_order, ticket=ticket)

    yield order_ticket

    order_ticket.delete()
