# Generated by Django 4.2 on 2023-04-12 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_city_drive_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="city",
            name="drive_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]