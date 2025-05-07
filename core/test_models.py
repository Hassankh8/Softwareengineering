from django.test import TestCase
from core.models import User, MediaItem


class MediaItemModelTest(TestCase):
    def test_media_item_creation(self):
        # Custom user create karo
        user = User.objects.create(
            user_name="testuser",
            user_password="test1234",  # Make sure it's 8 characters max
            user_email="test@example.com",
            user_role="student",
        )

        # Ab media item create karo
        item = MediaItem.objects.create(
            title="Nature Photo",
            url="http://example.com/nature.jpg",
            user=user,  # foreign key assign
        )

        # Assert check
        self.assertEqual(item.title, "Nature Photo")
        self.assertEqual(item.user, user)
