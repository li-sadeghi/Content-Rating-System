from rest_framework import permissions, generics, status, response, throttling
from content_rating import serializers, models as content_rating_models


class RatingCreateUpdateView(generics.GenericAPIView):
    """API view to create or update a rating for a post."""

    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    throttle_scope = "user"

    def get_object(self):
        """Retrieve the post object using the pk in the URL."""
        post = generics.get_object_or_404(
            content_rating_models.Post, pk=self.kwargs["pk"]
        )
        return post

    def post(self, request, *args, **kwargs):
        """Handle POST request to create or update a rating."""
        post = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
