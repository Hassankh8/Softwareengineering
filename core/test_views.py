from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class MediaViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_search_view(self):
        response = self.client.get(reverse("media_search") + "?q=nature")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
