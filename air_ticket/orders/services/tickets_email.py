from django.conf import settings
from django.template.loader import render_to_string

from orders.models import Order
from orders.crud import get_passenger_order_tickets
from orders.tasks import send_tickets_email
from users.models import User


def tickets_email(user: User, order: Order):

    order_tickets = get_passenger_order_tickets(order)

    order.user = user
    order.save()

    html_content = render_to_string(
        template_name="customer/email/tickets_email.html",
        context={
            "domain": settings.DOMAIN,
            "order_tickets": order_tickets,
            "flight": order.flight,
        },
    )

    send_tickets_email.delay(html_content, user.email)
