from django.contrib.postgres.fields import ArrayField
from django.db import models


class Flight(models.Model):
    number = models.CharField()
    iata = models.CharField()
    icao = models.CharField()
    airplane = models.ForeignKey(
        "flight.Airplane", on_delete=models.DO_NOTHING
    )
    arrival_airport = models.ForeignKey(
        "flight.Airport",
        on_delete=models.DO_NOTHING,
        related_name="arrival_flight",
    )
    departure_airport = models.ForeignKey(
        "flight.Airport",
        on_delete=models.DO_NOTHING,
        related_name="departure_flight",
    )
    arrival_scheduled = models.DateTimeField()
    departure_scheduled = models.DateTimeField()

    seats = ArrayField(models.IntegerField(), blank=True)
    ordered_seats = ArrayField(models.IntegerField(), default=list, blank=True)

    def save(self, *args, **kwargs):
        if not self.ordered_seats:
            self.ordered_seats = []
        if not self.seats:
            self.seats = list(range(1, self.airplane.seats_amount + 1))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.number
