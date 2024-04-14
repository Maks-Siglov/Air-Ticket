from django.db import models


class TicketCart(models.Model):
    contact = models.ForeignKey(
        "customer.Contact", on_delete=models.SET_NULL, null=True, blank=True
    )
    passenger_amount = models.PositiveIntegerField()
    flight = models.ForeignKey("flight.Flight", on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart: {self.flight}, passengers {self.passenger_amount}"
