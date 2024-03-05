from django.db import models


class Contact(models.Model):
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    order = models.ForeignKey("booking.Order", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.email
