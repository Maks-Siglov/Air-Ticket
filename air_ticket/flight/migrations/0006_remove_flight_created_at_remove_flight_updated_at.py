# Generated by Django 5.0.1 on 2024-03-03 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0005_airport_remove_flight_departure_and_more"),
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