# Generated by Django 5.0.1 on 2024-03-03 21:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0007_alter_airport_iata_alter_airport_icao_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="airplane",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="flight.airplane",
            ),
        ),
    ]
