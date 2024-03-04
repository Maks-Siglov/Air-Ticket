from django.db import models


class Flight(models.Model):
    number = models.CharField()
    iata = models.CharField()
    icao = models.CharField()
    airplane = models.ForeignKey(
        "flight.Airplane", on_delete=models.CASCADE, null=True
    )
    arrival_airport = models.ForeignKey(
        "flight.Airport",
        on_delete=models.CASCADE,
        related_name="arrival_flight",
    )
    departure_airport = models.ForeignKey(
        "flight.Airport",
        on_delete=models.CASCADE,
        related_name="departure_flight",
    )
    arrival_scheduled = models.DateTimeField()
    departure_scheduled = models.DateTimeField()

    def __str__(self) -> str:
        return self.number
