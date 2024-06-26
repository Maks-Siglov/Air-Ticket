# Generated by Django 5.0.1 on 2024-03-03 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0006_remove_flight_created_at_remove_flight_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airport",
            name="iata",
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name="airport",
            name="icao",
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name="airport",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
