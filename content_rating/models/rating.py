from django.db import models as django_models
from helpers import models as helper_models
from django.contrib.auth import models as auth_models
from content_rating import models as content_rating_models

SCORE_VALUE_CHOICES = [(i, i) for i in range(6)]


class Rating(helper_models.TimeModel):
    """Represents a user's rating for a post.

    Attributes:
        user (ForeignKey): The user who submitted the rating.
        post (ForeignKey): The post being rated.
        score (IntegerField): The score given by the user, must be one of the predefined choices (0-5).

    Meta:
        constraints: Ensures that each user can only rate a given post once.
    """

    user = django_models.ForeignKey(
        auth_models.User,
        on_delete=django_models.CASCADE,
        help_text="The user who submitted the rating.",
        verbose_name="User",
    )
    post = django_models.ForeignKey(
        content_rating_models.Post,
        on_delete=django_models.CASCADE,
        related_name="ratings",
        help_text="The post being rated.",
        verbose_name="Post",
    )
    score = django_models.IntegerField(
        choices=SCORE_VALUE_CHOICES,
        help_text="The score given by the user, must be one of the predefined choices.",
        verbose_name="Score",
    )

    class Meta:
        """Meta class to define custom constraints for the model."""

        constraints = [
            django_models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post",
                violation_error_message="Each user can rate a post only once.",
            )
        ]

    def __str__(self) -> str:
        """Returns a string representation of the Rating object."""
        return f"{self.user.username} rated {self.post.title} with {self.score} score"
