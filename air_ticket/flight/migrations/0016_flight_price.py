# Generated by Django 5.0 on 2024-04-16 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0015_flight_booked_seats"),
    ]

    operations = [
        migrations.AddField(
            model_name="flight",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=120, max_digits=10
            ),
        ),
    ]
