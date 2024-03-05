from decimal import Decimal

from django.db import models


class Ticket(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lunch = models.BooleanField(default=False)
    luggage = models.BooleanField(default=False)
    seat = models.ForeignKey("flight.Seat", on_delete=models.PROTECT)
    passenger = models.ForeignKey(
        "customer.passenger", on_delete=models.PROTECT
    )
    order = models.ForeignKey("booking.Order", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.passenger}, seat: {self.seat}"

    @property
    def unit_amount(self) -> int:
        return int(self.price * 100)
