from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

from ..models import User


class IndexViewTest(TestCase):
    def test_index_page_loading(self):
        """A GET request to the index (home) page"""
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")


class LoginViewTest(TestCase):
    def test_login_page_loading(self):
        """A GET request to the login page"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class RegisterViewTest(TestCase):
    def test_register_page_loading(self):
        """A GET request to the register page"""
        response = self.client.get(reverse("blog:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_register_a_user(self):
        """A POST request to the register page"""
        response = self.client.post(
            reverse("blog:register"),
            {
                "username": "bob",
                "password1": "ZXCzxc!@#123",
                "password2": "ZXCzxc!@#123",
            },
        )
        self.assertEqual(response.status_code, 302)


class LogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="bob", password="ZXCzxc!@#123")
        user.save()

    def test_logout_request(self):
        """A POST request from a logged in user to logout"""
        login_result = self.client.login(username="bob", password="ZXCzxc!@#123")
        self.assertTrue(login_result)

        self.client.logout()
        self.assertFalse(get_user(self.client).is_authenticated)
