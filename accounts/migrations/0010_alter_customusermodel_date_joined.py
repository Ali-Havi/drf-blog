# Generated by Django 5.2 on 2025-07-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_rename_phone_number_customusermodel_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customusermodel",
            name="date_joined",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
