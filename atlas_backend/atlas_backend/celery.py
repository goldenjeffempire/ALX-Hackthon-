# atlas_backend/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atlas_backend.settings')

app = Celery('atlas_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
