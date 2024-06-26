# Generated by Django 5.0 on 2024-04-18 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0022_ticket_flight"),
        (
            "flight",
            "0018_alter_flight_airplane_alter_flight_arrival_airport_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="flight",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="flight.flight",
            ),
        ),
    ]
