# Generated by Django 5.0.1 on 2024-03-02 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0003_place_remove_flight_departure_airport_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="flight",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="flight",
            name="updated_at",
        ),
    ]
