from django.db import models as django_models
from helpers import models as helper_models


class Post(helper_models.TimeModel):
    """Represents a post of content rating system.

    Attributes:
        title (str): The title of the post(This is a short title for post).
        content (str): The content of the post that include more explanarion about post.
    """

    title = django_models.CharField(max_length=100)
    content = django_models.TextField()

    def __str__(self) -> str:
        return self.title

    @property
    def total_ratings(self) -> int:
        """Returns the total number of users who have rated this post."""
        return self.ratings.count()

    @property
    def average_rating(self) -> float:
        """Returns the average rating for the post. If no ratings exist, return 0."""
        return (
            self.ratings.aggregate(avg_score=django_models.Avg("score"))["avg_score"]
            or 0.0
        )
