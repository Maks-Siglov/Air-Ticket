# Generated by Django 5.0 on 2024-04-18 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0017_flight_luggage_price_flight_lunch_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="airplane",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="flight.airplane",
            ),
        ),
        migrations.AlterField(
            model_name="flight",
            name="arrival_airport",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="arrival_flight",
                to="flight.airport",
            ),
        ),
        migrations.AlterField(
            model_name="flight",
            name="departure_airport",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="departure_flight",
                to="flight.airport",
            ),
        ),
    ]
