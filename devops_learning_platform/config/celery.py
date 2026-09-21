"""
Celery Configuration.

WHAT IS CELERY?
---------------
Celery is a distributed task queue. It lets Django offload slow or
periodic tasks to background workers so the web server stays fast.

WHY DO WE NEED IT?
------------------
Without Celery, every HTTP request is synchronous. If you trigger an AI
analysis that takes 30 seconds, the user's browser hangs. With Celery:
  1. Django puts the task on a Redis queue (near-instant)
  2. Returns a 202 Accepted to the browser immediately
  3. A Celery worker picks up the task and runs it in the background
  4. The result is stored and the user is notified

ARCHITECTURE:
-------------
Django Web → Redis (Message Broker) → Celery Worker → Result Backend (Redis)

HOW IT WORKS:
-------------
1. @shared_task decorator marks a function as a Celery task
2. Calling task.delay() sends it to the queue asynchronously
3. Worker processes the task and stores the result
"""
import os
from celery import Celery

# Tell Celery where to find Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('devops_platform')

# Load Celery config from Django settings (keys prefixed with CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all INSTALLED_APPS
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task — prints request info. Test with: debug_task.delay()"""
    print(f'Request: {self.request!r}')
