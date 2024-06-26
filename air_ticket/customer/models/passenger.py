from django.db import models


class Passenger(models.Model):
    passport_id = models.CharField(unique=True, max_length=12)
    first_name = models.CharField()
    last_name = models.CharField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
