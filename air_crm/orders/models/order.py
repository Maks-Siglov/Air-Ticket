from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("Processed", "processed"),
        ("Completed", "completed"),
        ("Canceled", "canceled"),
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    cart = models.ForeignKey(
        "booking.TicketCart", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Processed"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
