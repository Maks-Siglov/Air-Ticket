from django.contrib.auth.models import Permission
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name
