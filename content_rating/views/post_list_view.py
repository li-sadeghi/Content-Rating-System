from rest_framework import generics, permissions
from content_rating import models as content_rating_models
from content_rating import serializers


class PostListView(generics.ListAPIView):
    """API view to retrieve a list of posts.

    This view returns a list of all posts along with their total ratings,
    average rating, and the rating given by the authenticated user (if any).
    """

    queryset = content_rating_models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        """Passes the request context to the serializer to access the authenticated user."""
        return {"request": self.request}
