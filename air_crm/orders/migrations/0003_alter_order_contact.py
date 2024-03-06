# Generated by Django 5.0.1 on 2024-03-06 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0006_remove_contact_order"),
        ("orders", "0002_order_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="customer.contact",
            ),
        ),
    ]