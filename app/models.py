import os
import uuid
from PIL import Image

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width > 1400 or img.height > 800:
            output_size = (1400, 800)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    RATING = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="comment"
    )
    city = models.ForeignKey("City", on_delete=models.CASCADE, related_name="comment")
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=5, choices=RATING)

    def __str__(self):
        return f"Comment {self.user.first_name} for {self.city}. Rating {self.rating}"


class Pages(models.Model):
    text = models.TextField()
