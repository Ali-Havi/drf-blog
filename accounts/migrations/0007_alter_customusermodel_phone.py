# Generated by Django 5.2 on 2025-07-26 09:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_customusermodel_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customusermodel",
            name="phone",
            field=models.CharField(
                max_length=14,
                validators=[
                    django.core.validators.RegexValidator(regex="^\\+989\\d{9}$")
                ],
            ),
        ),
    ]
