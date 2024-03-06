from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("Preorder", "preorder"),
        ("Processed", "processed"),
        ("Completed", "completed"),
        ("Canceled", "canceled"),
    )
    passenger_amount = models.PositiveIntegerField()
    contact = models.ForeignKey(
        "customer.Contact", on_delete=models.CASCADE, null=True, blank=True
    )
    flight = models.ForeignKey("flight.Flight", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="preorder"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
