from orders.models import Order


def get_order(order_pk: int) -> Order:
    return Order.objects.select_related("cart").get(pk=order_pk)
