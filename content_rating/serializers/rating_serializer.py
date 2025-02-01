from rest_framework import serializers
from content_rating import models as content_rating_models


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for creating or updating a rating for a post."""

    class Meta:
        model = content_rating_models.Rating
        fields = ["score"]

    def create(self, validated_data):
        """Create a new rating or update an existing one."""
        user = self.context["request"].user
        post = validated_data["post"]

        rating, created = content_rating_models.Rating.objects.update_or_create(
            user=user, post=post, defaults={"score": validated_data["score"]}
        )

        return rating
