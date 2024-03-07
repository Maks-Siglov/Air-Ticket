from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from booking.selectors import get_cart_tickets
from flight.selectors import get_flight
from orders.models import Order
from users.models import User


def send_creation_user_email(order: Order):
    contact = order.cart.contact
    password = User.objects.make_random_password()
    user = User.objects.create_user(
        email=contact.email,
        password=password,
        phone_number=contact.phone_number,
    )

    order.user = user
    order.save()

    cart = order.cart
    tickets = get_cart_tickets(cart)
    flight = get_flight(cart.flight.pk)

    html_content = render_to_string(
        template_name="customer/email/creation_email_with_tickets.html",
        context={
            "domain": settings.DOMAIN,
            "email": contact.email,
            "password": password,
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
