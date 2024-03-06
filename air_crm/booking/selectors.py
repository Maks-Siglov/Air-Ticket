from booking.models import Ticket


def get_ticket(ticket_pk: int) -> Ticket:
    return Ticket.objects.select_related("passenger", "seat").get(pk=ticket_pk)
