from django.db import models


class OrderTicket(models.Model):
    ticket = models.ForeignKey("booking.Ticket", on_delete=models.RESTRICT)
    order = models.ForeignKey("orders.Order", on_delete=models.RESTRICT)
    seat_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.order}, seat: {self.seat_number}"
