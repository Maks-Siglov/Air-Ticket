from django.db.models import QuerySet

from customer.models import Contact
from orders.models import Order
from orders.models.order_ticket import OrderTicket
from users.models import User


def get_order(order_pk: int) -> Order:
    return Order.objects.get(pk=order_pk)


def get_user_orders(user: User) -> QuerySet[Order]:
    return Order.objects.filter(user=user).order_by("created_at")


def get_order_tickets(order: Order) -> QuerySet[OrderTicket]:
    return OrderTicket.objects.filter(order=order).select_related("ticket")
