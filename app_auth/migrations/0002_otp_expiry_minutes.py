# Generated by Django 5.0.1 on 2024-06-24 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_auth", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="otp",
            name="expiry_minutes",
            field=models.IntegerField(default=10),
        ),
    ]
