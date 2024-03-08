# Generated by Django 5.0.1 on 2024-03-03 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0001_initial"),
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="user",
        ),
        migrations.AddField(
            model_name="ticket",
            name="passenger",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="customer.passenger",
            ),
            preserve_default=False,
        ),
    ]