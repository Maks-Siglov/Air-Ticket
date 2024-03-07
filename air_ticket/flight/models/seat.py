from django.db import models


class Seat(models.Model):
    TYPE_CHOICES = (
        ("Economy", "economy"),
        ("Business", "business"),
        ("First Class", "first class"),
    )
    airplane = models.ForeignKey(
        "flight.Airplane", on_delete=models.CASCADE, related_name="seats"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} in {self.airplane}"
