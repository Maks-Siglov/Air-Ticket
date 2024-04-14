import pytest
from booking.models import Ticket, TicketCart
from booking.tests.conftest import (
    test_airplane_with_seats,
    test_cart,
    test_contact,
    test_flight
)
from flight.models import Flight
from orders.models import Order
from orders.models.order_ticket import OrderTicket
from users.tests.conftest import test_user


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
