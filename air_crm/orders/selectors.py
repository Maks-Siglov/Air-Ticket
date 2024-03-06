from decimal import Decimal

from django.db.models import QuerySet, Sum

from booking.models import Ticket
from orders.models import Order


def get_order(order_pk: int) -> Order:
    return Order.objects.select_related("cart").get(pk=order_pk)
