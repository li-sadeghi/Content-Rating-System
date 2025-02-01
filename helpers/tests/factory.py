from content_rating import models as content_rating_models
from django.contrib.auth import models as auth_models
import random
import string


def create_dummy_post(
    title: str = "Test title", content: str = "Content of the test title"
) -> content_rating_models.Post:
    """Creates and returns a dummy post."""
    return content_rating_models.Post.objects.create(title=title, content=content)


def create_dummy_rating(
    user: auth_models.User, post: content_rating_models.Post, score: int
) -> content_rating_models.Rating:
    """Creates and returns a dummy rating for a post by a user."""
    return content_rating_models.Rating.objects.create(
        user=user, post=post, score=score
    )


def create_dummy_user(**kwargs) -> auth_models.User:
    """Create and return a dummy user with random values for its username and password."""
    kwargs.setdefault(
        "username",
        "test_user" + "".join(random.choice(string.ascii_letters) for i in range(8)),
    )
    kwargs.setdefault("password", "F4kePaSs0d")
    kwargs.setdefault("email", "test_user@example.com")
    user = auth_models.User.objects.create_user(**kwargs)
    user.raw_password = kwargs["password"]
    return user
