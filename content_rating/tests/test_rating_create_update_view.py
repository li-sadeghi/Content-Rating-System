from rest_framework import test, status
from helpers.tests import factory
from content_rating import models as content_rating_models
from django import urls


class RatingCreateUpdateViewTest(test.APITestCase):
    """Test for the RatingCreateUpdateView."""

    def setUp(self):
        """Setup test data."""
        self.user = factory.create_dummy_user(
            username="testusername", password="testpassword"
        )
        self.post = factory.create_dummy_post(title="Test Post", content="Test content")
        self.api_url = urls.reverse("create-update-rating", kwargs={"pk": self.post.pk})

    def test_create_rating_authenticated(self):
        """Test creating a new rating when authenticated."""
        self.client.login(username="testusername", password="testpassword")
        response = self.client.post(self.api_url, {"score": 4})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rating = content_rating_models.Rating.objects.get(
            user=self.user, post=self.post
        )
        self.assertEqual(rating.score, 4)

    def test_update_rating_authenticated(self):
        """Test updating the rating when authenticated."""
        self.client.login(username="testusername", password="testpassword")
        factory.create_dummy_rating(user=self.user, post=self.post, score=3)
        response = self.client.post(self.api_url, {"score": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rating = content_rating_models.Rating.objects.get(
            user=self.user, post=self.post
        )
        self.assertEqual(rating.score, 5)

    def test_unauthenticated_user(self):
        """Test that unauthenticated users cannot create or update a rating."""
        response = self.client.post(self.api_url, {"score": 4})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_score(self):
        """Test that invalid score values return a 400 error."""
        self.client.login(username="testusername", password="testpassword")

        response = self.client.post(self.api_url, {"score": 10})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("score", response.data)

    def test_no_score(self):
        """Test that missing score returns a 400 error."""
        self.client.login(username="testusername", password="testpassword")

        response = self.client.post(self.api_url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("score", response.data)

    def test_user_rate_throttling(self):
        self.client.login(username="testusername", password="testpassword")
        response = self.client.post(self.api_url, {"score": 5})

        # Throttle must allow the first request
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.post(self.api_url, {"score": 5})
        self.client.post(self.api_url, {"score": 5})
        self.client.post(self.api_url, {"score": 5})
        self.client.post(self.api_url, {"score": 5})
        response = self.client.post(self.api_url, {"score": 5})

        # Throttle must not allow the fifth request
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
