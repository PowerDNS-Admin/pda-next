import os

from celery import Celery
from loguru import logger

from lib import load_config, init_logging
from lib.celery import SignalHandler

# Load app configuration and initialize logging
config = load_config()
init_logging(config)

# Instantiate the Celery application
app = Celery(
    config.app.name,
    broker=config.celery.broker.url,
    backend=config.celery.backend.url,
)

# Instantiate a Celery signal handler
SignalHandler(app=app)

# Set this app instance to be the default for all threads
app.set_default()

# Configure Celery
app.conf.beat_scheduler = 'src.lib.celery.DynamicScheduler'
app.conf.timezone = 'UTC'
app.conf.event_serializer = 'pickle'
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.result_extended = True
app.conf.accept_content = ['json', 'application/json', 'application/x-python-serialize']

# Set up task auto-discovery
root_task_path = f'src/tasks'
task_packages = []

for dirpath, _, filenames in os.walk(root_task_path):
    for filename in filenames:
        if filename.endswith('.py') and filename != '__init__.py':
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_task_path)
            module = rel_path.replace(os.path.sep, '.').rsplit('.py', 1)[0]
            task_packages.append(f'tasks.{module}')

logger.debug(f'Registering task packages for auto-discovery: {task_packages}')

app.autodiscover_tasks(task_packages)
