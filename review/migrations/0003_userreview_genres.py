# Generated by Django 5.0.6 on 2024-07-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("review", "0002_userreview_ip"),
    ]

    operations = [
        migrations.AddField(
            model_name="userreview",
            name="genres",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
