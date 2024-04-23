from django.conf import settings
from django.template.loader import render_to_string

from orders.crud import get_passenger_order_tickets
from orders.models import Order
from orders.services.email.send_email import send_tickets_email
from users.models import User


def creation_user_email(order: Order):
    order_tickets = get_passenger_order_tickets(order)

    order_ticket = order_tickets.first()
    contact = order_ticket.ticket.cart.contact

    password = User.objects.make_random_password()
    user = User.objects.create_user(
        email=contact.email,
        password=password,
        phone_number=contact.phone_number,
    )

    order.user = user
    order.save()

    html_content = render_to_string(
        template_name="customer/email/creation_email_with_tickets.html",
        context={
            "domain": settings.DOMAIN,
            "email": contact.email,
            "password": password,
            "order_tickets": order_tickets,
            "flight": order.flight,
        },
    )

    send_tickets_email(html_content, user.email)
