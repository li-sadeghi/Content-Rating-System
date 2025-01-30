from django.contrib import auth
from rest_framework import test, status
from django import urls

User = auth.get_user_model()


class TestLoginView(test.APITestCase):
    """Test suite for the user login endpoint."""

    def setUp(self):
        """Set up the necessary test data like user object for login tests."""
        self.api_url = urls.reverse("token_obtain_pair")
        self.user = User.objects.create(
            username="testusername", password="testtesttest"
        )
        self.user.set_password("testtesttest")
        self.user.save()

    def test_login_user_successfully(self):
        """Test logging in a user with valid credentials."""
        data = {"username": "testusername", "password": "testtesttest"}
        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_dont_login_user_with_incorrect_username(self):
        """Test logging in with an incorrect username."""
        data = {"username": "test1username", "password": "testtesttest"}
        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dont_login_user_with_incorrect_password(self):
        """Test logging in with an incorrect password."""
        data = {"username": "testusername", "password": "incorrectpass"}
        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
