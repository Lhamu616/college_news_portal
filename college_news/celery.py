import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE','college_news.settings')

app= Celery('college_news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()