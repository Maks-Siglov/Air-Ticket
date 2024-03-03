from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    timezone = models.CharField(max_length=255)
    iata = models.CharField(max_length=6)
    icao = models.CharField(max_length=6)

    def __str__(self):
        return self.name
