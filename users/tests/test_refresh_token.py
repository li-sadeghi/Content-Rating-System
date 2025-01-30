from rest_framework import test, status
from django import urls
from django.contrib import auth

User = auth.get_user_model()


class TestRefreshTokenView(test.APITestCase):
    """Test suite for the refresh token endpoint."""

    def setUp(self):
        """Set up the necessary test data and authentication for token refresh tests."""
        user = User.objects.create(username="testusername")
        user.set_password("testtesttest")
        user.save()
        self.login_url = urls.reverse("token_obtain_pair")
        self.refresh_token_url = urls.reverse("token_refresh")

        user_data = {"username": "testusername", "password": "testtesttest"}

        login_response = self.client.post(self.login_url, user_data)
        self.refresh_token = login_response.data.get("refresh")

    def test_refresh_token_valid(self):
        """Test refresh token with valid refresh token"""
        response = self.client.post(
            self.refresh_token_url, {"refresh": self.refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_invalid(self):
        """Test refresh token with invalid refresh token"""
        response = self.client.post(
            self.refresh_token_url, {"refresh": "invalid_token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Token is invalid or expired")
