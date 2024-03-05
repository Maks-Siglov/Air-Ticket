from django.db.models import QuerySet

from booking.models import Ticket
from orders.models import Order


def get_order(order_pk: int) -> Order:
    return Order.objects.select_related("flight").get(pk=order_pk)


def get_order_tickets(order: Order) -> QuerySet[Ticket]:
    return Ticket.objects.filter(order=order).select_related(
        "passenger", "seat"
    )
