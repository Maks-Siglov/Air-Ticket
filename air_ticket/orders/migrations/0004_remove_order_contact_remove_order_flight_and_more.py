# Generated by Django 5.0.1 on 2024-03-06 17:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0013_ticketcart"),
        ("orders", "0003_alter_order_contact"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="contact",
        ),
        migrations.RemoveField(
            model_name="order",
            name="flight",
        ),
        migrations.RemoveField(
            model_name="order",
            name="passenger_amount",
        ),
        migrations.AddField(
            model_name="order",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="booking.ticketcart",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Processed", "processed"),
                    ("Completed", "completed"),
                    ("Canceled", "canceled"),
                ],
                default="Processed",
                max_length=20,
            ),
        ),
    ]
