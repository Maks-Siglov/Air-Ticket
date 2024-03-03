from django.db import models


class Passenger(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
