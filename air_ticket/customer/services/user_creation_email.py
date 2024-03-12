from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from flight.selectors import get_flight
from orders.models import Order
from orders.selectors import get_passenger_order_tickets
from users.models import User


def send_creation_user_email(order: Order):
    order_tickets = get_passenger_order_tickets(order)
    flight = get_flight(order.flight_id)

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
