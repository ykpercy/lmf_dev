from celery import shared_task
from django.core.management import call_command

@shared_task
def update_stock_data():
    call_command('update_stock_data')

# In your Celery beat schedule configuration (e.g., in settings.py):
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update-stock-data-every-day': {
        'task': 'stock_api.tasks.update_stock_data',
        'schedule': crontab(hour=0, minute=0),
    },
}