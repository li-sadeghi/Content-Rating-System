from django.urls import path
from content_rating.views import post_list_view

urlpatterns = [
    path("posts/", post_list_view.PostListView.as_view(), name="post-list"),
]
