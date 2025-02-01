from django.urls import path
from content_rating.views import post_list_view, rating_create_update_view

urlpatterns = [
    path("posts/", post_list_view.PostListView.as_view(), name="post-list"),
    path(
        "rating/<int:pk>/",
        rating_create_update_view.RatingCreateUpdateView.as_view(),
        name="create-update-rating",
    ),
]
