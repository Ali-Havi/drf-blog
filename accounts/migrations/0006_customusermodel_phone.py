# Generated by Django 5.2 on 2025-07-26 09:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_customusermodel_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customusermodel",
            name="phone",
            field=models.CharField(
                default="2",
                max_length=14,
                validators=[
                    django.core.validators.RegexValidator(regex="^\\+989\\d{9}$")
                ],
            ),
        ),
    ]
