from django.db import models


class OrderTicket(models.Model):
    ticket = models.ForeignKey("booking.Ticket", on_delete=models.DO_NOTHING)
    order = models.ForeignKey("orders.Order", on_delete=models.DO_NOTHING)
    seat = models.ForeignKey(
        "flight.Seat", on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def __str__(self):
        return f"{self.order}, seat: {self.seat}"
