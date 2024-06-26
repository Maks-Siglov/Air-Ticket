# Generated by Django 5.0.1 on 2024-02-29 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Airplane",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=80)),
                ("places_amount", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Flight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure_airport", models.CharField(max_length=100)),
                ("destination_airport", models.CharField(max_length=100)),
                ("departure_date", models.DateField()),
                ("destination_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "airplane",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="flight.airplane",
                    ),
                ),
            ],
        ),
    ]
