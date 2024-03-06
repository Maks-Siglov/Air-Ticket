from decimal import Decimal

from django.db.models import QuerySet, Sum

from booking.models import Ticket
from orders.models import Order


def get_order(order_pk: int) -> Order:
    return Order.objects.select_related("flight", "contact").get(pk=order_pk)


def get_order_tickets(order: Order) -> QuerySet[Ticket]:
    return Ticket.objects.filter(order=order).select_related(
        "passenger", "seat"
    )


def get_order_total_price(order: Order) -> Decimal:
    return Ticket.objects.filter(order=order).aggregate(
        total_price=Sum("price")
    )["total_price"] or Decimal("0.00")
