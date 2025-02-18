from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workIndia.settings")

app = Celery("workIndia")

# Configure Celery using settings from Django settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Update task routing and queues in configuration
app.conf.update(
    task_routes={
        "railways.tasks.celery.process_booking_information": {
            "queue": settings.BOOKING_PROCESSING_QUEUE
        },
    },
    task_queues={
        settings.BOOKING_PROCESSING_QUEUE: {
            "exchange": "bookings",
            "binding_key": "book",
        },
    },
    task_serializer="json",
    accept_content=["json"],
)
