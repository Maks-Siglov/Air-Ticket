from django.db.models import QuerySet

from orders.models import Order
from users.models import User


def get_order(order_pk: int) -> Order:
    return Order.objects.select_related("cart").get(pk=order_pk)


def get_user_orders(user: User) -> QuerySet[Order]:
    return Order.objects.filter(user=user).order_by("created_at")
