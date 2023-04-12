from rest_framework import serializers

from app.models import City, CityImage


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "song_line",
            "description",
            "drive_url",
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityImage
        fields = (
            "image",
        )


class CitySerializer(CityListSerializer):
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "song_line",
            "description",
            "drive_url",
            "image",
        )
