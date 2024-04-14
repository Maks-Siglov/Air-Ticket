from django.db import models

from booking.models.ticket import Ticket
from booking.models.ticket_cart import TicketCart
from flight.models.flight import Flight


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(TicketCart, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(
        Ticket, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    is_ordered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
