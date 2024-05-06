from django.conf import settings
from django.template.loader import render_to_string

import requests
from orders.crud import get_passenger_order_tickets
from orders.models import Order
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

    response = requests.post(
        f"http://{settings.BOOKING_MANAGEMENT_DOMAIN}/send-email/",
        json={"html_content": html_content, "user_email": user.email},
    )
