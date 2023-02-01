import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'when_creating_post': {
        'task': 'news.tasks.notify_about_new_post',
        'schedule': 30,
        'args': ("some_arg"),
    },
}

app.conf.beat_schedule = {
    'when_week': {
        'task': 'news.tasks.mailing_weekly',
        'schedule': crontab(hour=11, minute=15, day_of_week='monday'),
    },
}