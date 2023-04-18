from rest_framework import serializers, fields

from app.models import City, CityImage, Comment


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


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name')
    profile_photo = fields.ImageField(source='user.profile_photo', read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "header",
            "text",
            "rating",
            "profile_photo",
        )


class CitySerializer(CityListSerializer):
    image = ImageSerializer(many=True, read_only=True)
    comment = CommentSerializer(many=True)

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "song_line",
            "description",
            "drive_url",
            "image",
            "comment",
        )
