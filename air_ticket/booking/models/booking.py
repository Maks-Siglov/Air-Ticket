from django.db import models


class Booking(models.Model):
    flight = models.ForeignKey("flight.Flight", on_delete=models.DO_NOTHING)
    cart = models.ForeignKey("booking.TicketCart", on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(
        "booking.Ticket", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    is_ordered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"Flight: {self.flight}, Ticket: {self.ticket}, "
            f"Ordered: {self.is_ordered}, Active: {self.is_active}"
        )
