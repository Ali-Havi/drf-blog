# Generated by Django 5.2 on 2025-07-21 13:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customusermodel",
            name="date_joined",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="customusermodel",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="customusermodel",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]
