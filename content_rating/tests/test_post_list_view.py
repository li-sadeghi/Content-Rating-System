from rest_framework import test
from rest_framework import status
from content_rating import models as content_rating_models
from django import urls
from helpers.tests import factory


class PostListViewTest(test.APITestCase):
    """Test for the PostListView API"""

    def setUp(self):
        """Setup data for testing"""
        self.user = factory.create_dummy_user(
            username="testusername", password="testpassword"
        )

        # Create some posts
        self.post1 = content_rating_models.Post.objects.create(
            title="First Post", content="Content of first post"
        )
        self.post2 = content_rating_models.Post.objects.create(
            title="Second Post", content="Content of second post"
        )

        self.api_url = urls.reverse("post-list")

    def test_get_posts_authenticated(self):
        """Test retrieving posts when authenticated"""
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get(self.api_url)

        expected_fields = [
            "id",
            "title",
            "content",
            "total_ratings",
            "average_rating",
            "user_rating",
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        for field in expected_fields:
            self.assertIn(
                field, response.data[0], f"Field '{field}' not found in the response"
            )

        self.assertIsNone(response.data[0]["user_rating"])
        self.assertIsNone(response.data[1]["user_rating"])

    def test_get_posts_unauthenticated(self):
        """Test retrieving posts when not authenticated"""
        response = self.client.get(self.api_url)

        expected_fields = [
            "id",
            "title",
            "content",
            "total_ratings",
            "average_rating",
            "user_rating",
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        for field in expected_fields:
            self.assertIn(
                field, response.data[0], f"Field '{field}' not found in the response"
            )

        self.assertIsNone(response.data[0]["user_rating"])
        self.assertIsNone(response.data[1]["user_rating"])

    def test_user_rating_in_response(self):
        """Test that the user’s rating appears in the response."""
        self.client.login(username="testusername", password="testpassword")
        content_rating_models.Post.objects.first().ratings.create(
            user=self.user, score=4
        )

        response = self.client.get(self.api_url)
        self.assertEqual(response.data[0]["user_rating"], 4)
        self.assertIsNone(response.data[1]["user_rating"])
