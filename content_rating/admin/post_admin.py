from django.contrib import admin
from content_rating import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Post model."""

    model = models.Post
    list_display = (
        "title",
        "content",
        "total_ratings",
        "average_rating",
    )
    readonly_fields = ("total_ratings", "average_rating")
