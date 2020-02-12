from __future__ import absolute_import
import os
import logging
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base_app.settings')

app = Celery('base_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

