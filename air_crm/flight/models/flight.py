from django.db import models


class Flight(models.Model):
    number = models.CharField()
    iata = models.CharField()
    icao = models.CharField()
    airplane = models.ForeignKey("flight.Airplane", on_delete=models.CASCADE)
    arrival = models.ForeignKey(
        "flight.Place",
        on_delete=models.CASCADE,
        related_name='arriving_flight'
    )
    departure = models.ForeignKey(
        "flight.Place",
        on_delete=models.CASCADE,
        related_name='departure_flight'
    )

    def __str__(self) -> str:
        return f"{self.airplane},"
