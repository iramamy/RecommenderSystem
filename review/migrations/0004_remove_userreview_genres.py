# Generated by Django 5.0.6 on 2024-07-01 09:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("review", "0003_userreview_genres"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userreview",
            name="genres",
        ),
    ]
