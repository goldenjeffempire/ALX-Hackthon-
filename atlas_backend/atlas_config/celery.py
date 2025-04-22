from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atlas_config.settings")

app = Celery("atlas_config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
