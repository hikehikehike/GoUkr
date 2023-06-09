# Generated by Django 4.2 on 2023-04-18 21:15

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_photo",
            field=models.ImageField(
                blank=True, null=True, upload_to=user.models.user_image_file_path
            ),
        ),
    ]
