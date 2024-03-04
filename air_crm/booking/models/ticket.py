from decimal import Decimal

from django.db import models


class Ticket(models.Model):
    price = models.PositiveIntegerField()
    seat = models.ForeignKey("flight.Seat", on_delete=models.PROTECT)
    passenger = models.ForeignKey(
        "customer.passenger", on_delete=models.PROTECT
    )
    order = models.ForeignKey("booking.Order", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.passenger}, seat: {self.seat}"

    def get_decimal_price(self) -> Decimal:
        return Decimal(self.price) / 100
