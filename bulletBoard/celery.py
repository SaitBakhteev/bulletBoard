import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletBoard.settings')

app = Celery('bulletBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # настройка для автопоиска тасок в проекте
app.conf.beat_schedule = {}
app.conf.timezone = 'Europe/Moscow'
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {'send_weekly_messages':
                          {'task':
                           'ads.tasks.weekly_mailing',
                           'schedule': crontab(day_of_week='sunday', hour='19', minute='16')}}
