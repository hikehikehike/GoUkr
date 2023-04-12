import os
import uuid

from django.db import models
from django.utils.text import slugify


def city_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/city/", filename)


class City(models.Model):
    name = models.CharField(max_length=255)
    song_line = models.TextField()
    description = models.TextField()
    gallery_image = models.ImageField(null=True, upload_to=city_image_file_path)
    drive_url = models.URLField()

