from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_api_backend.settings')

app = Celery('stock_api_backend')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule={
    'populate-market-data-daily':{
        'task':'stocks_api.tasks.async_market_population',
        'schedule':crontab(hour=14,minute=39),
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
