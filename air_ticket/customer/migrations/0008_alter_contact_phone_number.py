# Generated by Django 5.0.1 on 2024-04-03 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0007_alter_contact_email_alter_contact_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="phone_number",
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
