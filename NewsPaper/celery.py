import os
from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('news')#Newspaper
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_monday_8am': {
        'task': 'news.tasks.week_task',
        #'schedule': crontab(),
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    }
}
app.conf.timezone = 'UTC'
# реальное время (UTC 3) больше на 3часа , чем (UTC)
app.autodiscover_tasks()