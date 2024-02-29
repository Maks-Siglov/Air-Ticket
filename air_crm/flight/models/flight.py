from django.db import models


class Flight(models.Model):
    airplane = models.ForeignKey("flight.Airplane", on_delete=models.CASCADE)
    departure_place = models.CharField(max_length=100)
    destination_place = models.CharField(max_length=100)
    departure_date = models.DateField()
    destination_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            f"{self.airplane},"
            f" {self.departure_place} to {self.destination_place}"
        )

