# Generated by Django 5.0 on 2024-04-15 13:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0013_alter_flight_ordered_seats_alter_flight_seats"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="ordered_seats",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(),
                blank=True,
                default=list,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="flight",
            name="seats",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, size=None
            ),
        ),
    ]
