"""Celery application configuration for online_shop project."""

import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings.development')

app = Celery('online_shop')

# Load configuration from Django settings with CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to verify Celery is working."""
    print(f'Request: {self.request!r}')


# Task routing configuration
app.conf.task_routes = {
    'accounts.tasks.*': {'queue': 'critical'},
    'orders.tasks.*': {'queue': 'critical'},
}
