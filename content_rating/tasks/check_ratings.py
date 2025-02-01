import celery
from django.utils import timezone
from datetime import timedelta
from content_rating import models as content_rating_models
from django.db import models as db_models

INCREASE_RATINGS_TOTAL_CONTROLLER_COEFFICIENT = 5
UNUSUAL_RATINGS_CONTROLLER_COEFFICIENT = 1

@celery.shared_task
def check_for_unusual_ratings():
    """Check hourly for unusual spikes in ratings."""
    current_time = timezone.now()
    one_hour_ago = current_time - timedelta(hours=1)
    last_week = one_hour_ago - timedelta(days=7)

    for post in content_rating_models.Post.objects.all():
        last_hour_ratings = content_rating_models.Rating.objects.filter(
            post=post, modified__gte=one_hour_ago, modified__lte=current_time
        ).count()

        last_week_avg_hour_ratings = content_rating_models.Rating.objects.filter(
            post=post, modified__lte=one_hour_ago, modified__gte=last_week
        ).count() / (24 * 7)
    
        # Check for are there some unusual ratings for this post?
        if last_week_avg_hour_ratings * INCREASE_RATINGS_TOTAL_CONTROLLER_COEFFICIENT < last_hour_ratings:
            last_hour_ratings_total = content_rating_models.Rating.objects.filter(
                post=post, modified__gte=one_hour_ago, modified__lte=current_time
            ).aggregate(score_sum=db_models.Sum('score'))['score_sum']

            total_ratings_of_post = post.total_ratings
            avg_rating_of_post = post.average_rating

            last_rating_sum = avg_rating_of_post * total_ratings_of_post
            new_rating_of_post = (last_rating_sum + last_hour_ratings_total * UNUSUAL_RATINGS_CONTROLLER_COEFFICIENT) / total_ratings_of_post
            post.average_rating = new_rating_of_post
            post.save(update_fields=["average_rating"])
