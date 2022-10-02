from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Innotwitter.settings')

app = Celery("Innotwitter")

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()