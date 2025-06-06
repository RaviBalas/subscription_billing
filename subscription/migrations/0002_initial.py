# Generated by Django 5.2 on 2025-05-25 11:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("subscription", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="my_subscriptions",
                related_query_name="subscription",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
