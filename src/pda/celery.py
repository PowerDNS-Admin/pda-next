import os
from celery import Celery
from app import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pda.settings")

# Configure Celery backend and/or broker depending on configuration
celery_params = {}

if 'celery' in config and 'backend' in config.celery:
    backend = config.celery.backend

    if backend.engine == 'redis':
        celery_params['backend'] = f'redis://{backend.host}:{backend.port}/{backend.db}'

if 'celery' in config and 'broker' in config.celery:
    broker = config.celery.broker

    if broker.engine == 'redis':
        celery_params['broker'] = f'redis://{broker.host}:{broker.port}/{broker.db}'

app = Celery(f'pda-{__name__}', **celery_params)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
