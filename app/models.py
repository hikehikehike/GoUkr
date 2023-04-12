import os
import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from multifilefield.forms import MultiFileField

URL_GOOGLE_MAPS = "https://www.google.com/maps/dir/current+location/"


def city_drive_url(name):
    return f"{URL_GOOGLE_MAPS}{name}"


def city_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/city/", filename)


class City(models.Model):
    name = models.CharField(max_length=255)
    song_line = models.TextField()
    description = models.TextField()
    gallery_image = MultiFileField(null=True, upload_to=city_image_file_path)
    drive_url = models.URLField()

    def save(self, *args, **kwargs):
        self.drive_url = reverse("city_drive_url", args=[self.name])
        super().save(*args, **kwargs)
