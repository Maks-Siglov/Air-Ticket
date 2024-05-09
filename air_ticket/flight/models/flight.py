from django.contrib.postgres.fields import ArrayField
from django.db import models


class Flight(models.Model):
    number = models.CharField()
    iata = models.CharField()
    icao = models.CharField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=120)
    lunch_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=15
    )
    luggage_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=50
    )
    airplane = models.ForeignKey("flight.Airplane", on_delete=models.RESTRICT)
    arrival_airport = models.ForeignKey(
        "flight.Airport",
        on_delete=models.RESTRICT,
        related_name="arrival_flight",
    )
    departure_airport = models.ForeignKey(
        "flight.Airport",
        on_delete=models.RESTRICT,
        related_name="departure_flight",
    )
    arrival_scheduled = models.DateTimeField()
    departure_scheduled = models.DateTimeField()

    seats = ArrayField(models.IntegerField(), blank=True)
    booked_seats = ArrayField(models.IntegerField(), default=list, blank=True)
    ordered_seats = ArrayField(models.IntegerField(), default=list, blank=True)

    def save(self, *args, **kwargs):
        if not self.seats:
            self.seats = list(range(1, self.airplane.seats_amount + 1))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.number)
