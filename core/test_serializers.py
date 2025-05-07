from django.test import TestCase
# from rest_framework.exceptions import ValidationError
from core.models import User, SearchHistory, MediaItem
from core.serializers import (
    RegisterUserSerializer,
    UserSearchSerializer,
    MediaResultSerializer,
)

# from django.contrib.auth.hashers import check_password


class UserSerializerTest(TestCase):
    def test_invalid_password_too_short(self):
        data = {
            "user_name": "testuser",
            "user_password": "short",  # Too short password
            "user_email": "test@example.com",
            "user_role": "admin"
        }
        serializer = RegisterUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user_password", serializer.errors)

    def test_invalid_password_no_uppercase(self):
        data = {
            "user_name": "testuser",
            "user_password": "test1234",  # No uppercase
            "user_email": "test@example.com",
            "user_role": "admin"
        }
        serializer = RegisterUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user_password", serializer.errors)

    def test_invalid_password_no_digit(self):
        data = {
            "user_name": "testuser",
            "user_password": "TestTest",  # No digit
            "user_email": "test@example.com",
            "user_role": "admin"
        }
        serializer = RegisterUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user_password", serializer.errors)


class SearchHistorySerializerTest(TestCase):
    def test_valid_media_type(self):
        data = {
            "user": 1,
            "query": "test query",
            "media_type": "image",
            "searched_at": "2025-04-21T00:00:00Z",
        }
        serializer = UserSearchSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        search_history = serializer.save()

        self.assertEqual(search_history.media_type, "image")

    def test_valid_media_type(self):
        user = User.objects.create(
            user_name="testuser",
            user_password="Test1234",
            user_email="test@example.com",
            user_role="admin",
        )
        data = {
            "user": user.id,
            "query": "test query",
            "media_type": "image",  # Valid media type
            "searched_at": "2025-04-21T00:00:00Z",
        }
        serializer = UserSearchSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        search_history = serializer.save()
        self.assertEqual(search_history.media_type, "image")


class MediaItemSerializerTest(TestCase):
    def test_valid_media_item(self):
        user = User.objects.create(user_name="testuser", user_password="Test1234", user_email="test@example.com", user_role="admin")  # Create a user
        data = {
            "user": user.id,  # Use the user ID
            "query": "test query",
            "media_type": "image",
            "url": "http://example.com/image.jpg",
            "title": "Test Image",
            "thumbnail": "http://example.com/thumbnail.jpg",
            "fetched_at": "2025-04-21T00:00:00Z",
        }
        serializer = MediaResultSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        media_item = serializer.save()
        self.assertEqual(media_item.title, "Test Image")
        self.assertEqual(media_item.url, "http://example.com/image.jpg")

    def test_invalid_media_type_empty(self):
        data = {
            "user": 1,
            "query": "test query",
            "media_type": "",  # Empty media type
            "url": "http://example.com/image.jpg",
            "title": "Test Image",
            "thumbnail": "http://example.com/thumbnail.jpg",
            "fetched_at": "2025-04-21T00:00:00Z",
        }
        serializer = MediaResultSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors["media_type"]), 1)

    def test_invalid_url_format(self):
        data = {
            "user": 1,
            "query": "test query",
            "media_type": "image",
            "url": "ftp://example.com/image.jpg",  # Invalid URL format
            "title": "Test Image",
            "thumbnail": "http://example.com/thumbnail.jpg",
            "fetched_at": "2025-04-21T00:00:00Z",
        }
        serializer = MediaResultSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors["url"]), 1)

    def test_valid_url_format(self):
        user = User.objects.create(user_name="testuser", user_password="Test1234", user_email="test@example.com", user_role="admin")
        data = {
            "user": user.id,
            "query": "test query",
            "media_type": "image",
            "url": "http://example.com/image.jpg",  # Valid URL
            "title": "Test Image",
            "thumbnail": "http://example.com/thumbnail.jpg",
            "fetched_at": "2025-04-21T00:00:00Z",
        }
        serializer = MediaResultSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        media_item = serializer.save()
        self.assertEqual(media_item.url, "http://example.com/image.jpg")
