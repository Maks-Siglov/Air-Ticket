# Generated by Django 5.0.1 on 2024-03-06 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0013_ticketcart"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="order",
        ),
        migrations.AddField(
            model_name="ticket",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="booking.ticketcart",
            ),
            preserve_default=False,
        ),
    ]
