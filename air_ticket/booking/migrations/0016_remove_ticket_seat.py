# Generated by Django 5.0.1 on 2024-03-12 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0015_alter_ticket_cart_alter_ticket_passenger_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="seat",
        ),
    ]
