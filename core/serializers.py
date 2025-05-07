from rest_framework import serializers
from core.models import User, SearchHistory, MediaItem
from django.contrib.auth.hashers import make_password
import re


# ------------------------- User Serializer -------------------------


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_name", "user_password", "user_email", "user_role"]

    def create(self, attrs):
        attrs["user_password"] = make_password(attrs["user_password"])
        return super().create(attrs)

    def validate_user_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError(
                "Password should have at least 8 characters."
            )
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError("Include at least one uppercase letter.")
        if not re.search(r"\d", password):
            raise serializers.ValidationError("Include at least one number.")
        return password


# ---------------------- Search History Serializer ----------------------


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["id", "user", "query", "media_type", "searched_at"]
        read_only_fields = ["id", "searched_at"]

    def validate_media_type(self, media_type):
        valid_choices = {"image", "audio", "video"}
        if media_type not in valid_choices:
            raise serializers.ValidationError(
                "Media type must be image, audio, or video."
            )
        return media_type


# ------------------------- Media Item Serializer -------------------------


class MediaResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItem
        fields = [
            "id",
            "user",
            "query",
            "media_type",
            "url",
            "title",
            "thumbnail",
            "fetched_at",
        ]
        read_only_fields = ["id", "fetched_at"]

    def validate_media_type(self, media_type):
        if not media_type:
            raise serializers.ValidationError("Media type is required.")
        return media_type

    def validate_url(self, url):
        if not url.startswith(("http://", "https://")):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return url
