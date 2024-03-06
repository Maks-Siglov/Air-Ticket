from django.db import models


class Contact(models.Model):
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.email
