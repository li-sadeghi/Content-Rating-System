from django.contrib import admin
from content_rating import models


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Rating model."""

    model = models.Rating
    list_display = (
        "user",
        "post",
        "score",
    )
