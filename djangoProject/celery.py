from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('djangoProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-30-seconds': {
        'task': 'article.tasks.dict_with_tag',
        'schedule': 300.0,
    },
}
