from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from flight.selectors import get_flight
from orders.models import Order
from orders.selectors import get_order_tickets
from users.models import User


def send_tickets_email(user: User, order: Order):

    order_tickets = get_order_tickets(order)
    flight = get_flight(order.flight_id)

    html_content = render_to_string(
        template_name="customer/email/tickets_email.html",
        context={
            "domain": settings.DOMAIN,
            "order_tickets": order_tickets,
            "flight": flight,
        },
    )

    mail = EmailMultiAlternatives(
        subject="AirTicket",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    mail.attach_alternative(html_content, "text/html")

    mail.send()
