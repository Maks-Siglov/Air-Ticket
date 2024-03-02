from django.db import models


class Place(models.Model):
    airport = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    iata = models.CharField(max_length=255)
    icao = models.CharField(max_length=255)
    terminal = models.CharField(max_length=255, null=True, blank=True)
    gate = models.CharField(max_length=255, null=True, blank=True)
    scheduled = models.DateTimeField()

    def __str__(self):
        return f"{self.airport} - {self.timezone}"
