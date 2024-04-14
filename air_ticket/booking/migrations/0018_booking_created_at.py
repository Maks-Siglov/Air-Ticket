# Generated by Django 5.0 on 2024-04-05 16:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0017_booking"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]