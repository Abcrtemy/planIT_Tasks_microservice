import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_service.settings')

app = Celery('your_service')

# Указываем RabbitMQ как брокер
app.conf.broker_url = 'amqp://admin:admin@rabbitmq:5672//'

# Если используешь django-celery-results
app.conf.result_backend = 'django-db'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()