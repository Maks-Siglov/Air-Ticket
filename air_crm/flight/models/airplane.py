from django.db import models


class Airplane(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self) -> str:
        return self.name
