# Generated by Django 5.0 on 2024-04-16 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flight", "0016_flight_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="flight",
            name="luggage_price",
            field=models.DecimalField(
                decimal_places=2, default=50, max_digits=8
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="lunch_price",
            field=models.DecimalField(
                decimal_places=2, default=15, max_digits=8
            ),
        ),
        migrations.AlterField(
            model_name="flight",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=120, max_digits=8
            ),
        ),
    ]
