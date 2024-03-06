from booking.models import Ticket
from customer.models.contact import Contact
from orders.models import Order


def get_ticket(ticket_pk: int) -> Ticket:
    return Ticket.objects.select_related("passenger", "seat").get(pk=ticket_pk)


def get_contact(order: Order) -> Contact:
    return Contact.objects.filter(order=order).first()
