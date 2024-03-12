from django.db import models


class OrderTicket(models.Model):
    ticket = models.ForeignKey("booking.Ticket", on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    seat = models.ForeignKey(
        "flight.Seat", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.order}, seat: {self.seat}"
