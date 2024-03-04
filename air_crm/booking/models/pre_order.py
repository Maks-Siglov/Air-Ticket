from django.db import models


class PreOrder(models.Model):
    passenger_amount = models.PositiveIntegerField()
    flight = models.ForeignKey("flight.Flight", on_delete=models.CASCADE)
