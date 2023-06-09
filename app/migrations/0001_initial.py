# Generated by Django 4.2 on 2023-04-18 18:34

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("song_line", models.TextField()),
                ("description", models.TextField()),
                ("drive_url", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CityImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=app.models.city_image_file_path
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="image",
                        to="app.city",
                    ),
                ),
            ],
        ),
    ]
