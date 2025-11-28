import importlib, asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from app import initialize, init_loop, init_db_loop
from app.lib.prometheus import metric_setup
from app.routers import install_routers

# Initialize the app with logging, environment settings, and file-based configuration
config = initialize()

STARTUP_TASKS = [init_loop, init_db_loop]
RUNNING_TASKS = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize all tasks defined in STARTUP_TASKS list
    for task in STARTUP_TASKS:
        RUNNING_TASKS.append(asyncio.create_task(task()))

    yield

    # Cancel all tasks defined in the RUNNING_TASKS list
    for task in RUNNING_TASKS:
        task.cancel()


base_docs_url = config.server.proxy_root
if not base_docs_url.endswith('/'):
    base_docs_url += '/'

# Instantiate the FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title=config.app.name.title(),
    description=config.app.metadata.description,
    summary=config.app.summary,
    version=config.app.version,
    contact=config.app.author.model_dump(),
    openapi_tags=[t.model_dump() for t in config.api.metadata.tags],
    root_path=config.server.proxy_root,
    # FIXME: Update the following to load dynamically from environment configuration
    servers=[
        {'url': 'https://local.powerdnsadmin.org/api/', 'description': 'Local Development Environment'},
        {'url': 'https://dev.powerdnsadmin.org/api/', 'description': 'Shared Development Environment'},
        {'url': 'https://prod.powerdnsadmin.org/api/', 'description': 'Production Environment'},
    ],
)

# Set up Prometheus metrics for the app
metrics = Instrumentator()
metric_setup(metrics)
# TODO: Re-enable once schema created
# metrics.instrument(app).expose(app)

# FastAPI Middleware Configuration
if config.server.middleware:
    for middleware in config.server.middleware:
        logger.debug(f'Loading FastAPI middleware: {middleware.name}')
        mw_parts = middleware.name.split('.')
        mw_mod = importlib.import_module('.'.join(mw_parts[:-1]))
        mw = getattr(mw_mod, mw_parts[-1])
        app.add_middleware(mw, **middleware.config if middleware.config else {})

# Set up FastAPI routers
install_routers(app)
