import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "equipment_rental_site.settings")
app = Celery("equipment_rental_site")
app.config_from_object("django.conf:settings", namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def test_task():
    time.sleep(20)
    print('hello from test task!!!')
