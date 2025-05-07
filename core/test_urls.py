from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):

    def test_signup_url(self):
        url = reverse("signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_update_delete_user_url(self):
    #     url = reverse(
    #         "update_delete_user", args=[1]
    #     )  # Assuming you're passing a user_id
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    def test_main_url(self):
        url = reverse("main")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_url(self):
        url = reverse("user_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_history_url(self):
        url = reverse("search_history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_media_search_url(self):
        url = reverse("media_search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
