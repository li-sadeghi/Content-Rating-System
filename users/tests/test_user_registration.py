from django import urls
from django.contrib import auth
from rest_framework import test, status
from django.core import exceptions

User = auth.get_user_model()


class TestUserRegistration(test.APITestCase):
    """Test suite for user registration endpoints."""

    def setUp(self):
        """Set up the necessary test data and URLs."""
        self.api_url = urls.reverse("auth_register")

    def test_register_user_successfully(self):
        """Test case for registering a user with valid data successfully."""
        data = {
            "first_name": "test",
            "last_name": "testian",
            "username": "testusername",
            "email": "test@test.com",
            "password": "testtesttest",
        }
        response = self.client.post(self.api_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, "testusername")

    def test_register_existing_user_must_not_be_successful(self):
        """Test case for trying to register with an existing username."""
        User.objects.create(username="testusername")
        data = {
            "username": "testusername",
        }
        response = self.client.post(self.api_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_incomplete_information_must_not_be_successful(self):
        """Test case for registering with incomplete data."""
        data = {
            "last_name": "testian",
            "username": "testusername",
            "email": "test@test.com",
            "password": "testtesttest",
        }
        with self.assertRaises(exceptions.ValidationError):
            self.client.post(self.api_url, data)
