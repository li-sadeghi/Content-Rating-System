from django.db import transaction, models as django_models
from helpers import models as helper_models


class Post(helper_models.TimeModel):
    """Represents a post of content rating system.

    Attributes:
        title (str): The title of the post(This is a short title for post).
        content (str): The content of the post that include more explanarion about post.
    """

    title = django_models.CharField(max_length=100)
    content = django_models.TextField()

    total_ratings = django_models.PositiveIntegerField(default=0)
    average_rating = django_models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.title

    def update_ratings(self):
        """Update total ratings and average rating."""
        with transaction.atomic():
            post = Post.objects.select_for_update().get(id=self.id)
            total_ratings = post.ratings.count()
            if total_ratings > 0:
                avg_rating = post.ratings.aggregate(
                    avg_score=django_models.Avg("score")
                )["avg_score"]
            else:
                avg_rating = 0.0

            post.total_ratings = total_ratings
            post.average_rating = avg_rating
            post.save(update_fields=["total_ratings", "average_rating"])
