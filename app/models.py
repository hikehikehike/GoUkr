import os
import uuid

from django.db import models
from django.utils.text import slugify

URL_GOOGLE_MAPS = "https://www.google.com/maps/dir/current+location/"


def city_drive_url(name):
    return f"{URL_GOOGLE_MAPS}{name}"


def city_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.city.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/city/", filename)


class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    song_line = models.TextField()
    description = models.TextField()
    drive_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.drive_url = city_drive_url(self.name)
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"City: {self.name}"


class CityImage(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(null=True, upload_to=city_image_file_path)

    def __str__(self):
        return f"Image: {self.city}"
