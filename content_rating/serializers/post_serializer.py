from rest_framework import serializers
from content_rating import models as content_rating_models


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model.

    This serializer provides details about a post, including the total number
    of ratings, the average rating, and the rating given by the authenticated user.

    Attributes:
        user_rating (SerializerMethodField): Retrieves the rating given by the current user.
    """

    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = content_rating_models.Post
        fields = [
            "id",
            "title",
            "content",
            "total_ratings",
            "average_rating",
            "user_rating",
        ]
        read_only_fields = ["id", "total_ratings", "average_rating"]

    def get_user_rating(self, post_obj: content_rating_models.Post):
        """Returns the rating given by the authenticated user for this post."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            rating = post_obj.ratings.filter(user=request.user).first()
            return rating.score if rating else None
        return None
