from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_base.settings")
app = Celery("_base")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Beat schedule of tasks in whole project
app.conf.beat_schedule = {
    "create unusual ratings for posts": {
        "task": "content_rating.tasks.check_ratings.check_for_unusual_ratings",
        "schedule": crontab(minute='*', hour='*'),
    },
}
