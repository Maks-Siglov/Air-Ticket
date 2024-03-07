from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from booking.selectors import get_cart_tickets
from flight.selectors import get_flight
from orders.models import Order
from users.models import User


def send_tickets_email(user: User, order: Order):

    cart = order.cart
    tickets = get_cart_tickets(cart)
    flight = get_flight(cart.flight.pk)

    html_content = render_to_string(
        template_name="customer/email/tickets_email.html",
        context={
            "domain": settings.DOMAIN,
            "tickets": tickets,
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
