# Generated by Django 5.0 on 2024-04-15 07:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="staff.role"
            ),
        ),
        migrations.AlterField(
            model_name="staff",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
