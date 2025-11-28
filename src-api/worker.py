import os
from loguru import logger
from celery import Celery
from app import initialize
from app.lib.celery import SignalHandler

# Initialize the app with logging, environment settings, and file-based configuration
config = initialize()

# Initialize the Celery signal handler
signal_handler = SignalHandler()

# Instantiate the Celery application
app = signal_handler.app = Celery(
    config.app.name,
    broker=config.celery.broker.url,
    backend=config.celery.backend.url,
)

# Set this app instance to be the default for all threads
app.set_default()

app.conf.beat_scheduler = 'src.app.lib.celery.DynamicScheduler'
app.conf.timezone = 'UTC'
app.conf.event_serializer = 'pickle'
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.result_extended = True
app.conf.accept_content = ['json', 'application/json', 'application/x-python-serialize']

# Set up task auto-discovery
root_task_path = f'src/app/tasks'
task_packages = []

for dirpath, _, filenames in os.walk(root_task_path):
    for filename in filenames:
        if filename.endswith('.py') and filename != '__init__.py':
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_task_path)
            module = rel_path.replace(os.path.sep, '.').rsplit('.py', 1)[0]
            task_packages.append(f'app.tasks.{module}')

logger.debug(f'Registering task packages for auto-discovery: {task_packages}')

app.autodiscover_tasks(task_packages)
