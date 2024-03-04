from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("Preorder", "preorder"),
        ("Processed", "processed"),
        ("Completed", "completed"),
        ("Canceled", "canceled"),
    )
    passenger_amount = models.PositiveIntegerField()
    flight = models.ForeignKey("flight.Flight", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="preorder"
    )
