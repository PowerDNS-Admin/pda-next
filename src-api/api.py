import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app import initialize, init_loop, init_db_loop
from lib.config.app import EnvironmentEnum
from middleware import load_middleware
from routers import install_routers

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


# Set up FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title=config.app.name.title(),
    description=config.app.metadata.description,
    summary=config.app.summary,
    version=config.app.version,
    contact=config.app.author.model_dump(),
    openapi_tags=[t.model_dump() for t in config.api.metadata.tags],
    root_path=config.server.proxy_root,
    servers=[{'url': f'{config.app.environment.urls.api}/api/', 'description': 'PDA Environment API'}],
    debug=config.app.environment.name in (EnvironmentEnum.local, EnvironmentEnum.dev),
    swagger_ui_parameters={
        'docExpansion': 'none', # list, full, or none
        'displayRequestDuration': True,
        'filter': True,
        'tryItOutEnabled': True,
        'requestSnippetsEnabled': True,
        'persistAuthorization': True,
    },
)

# Set up FastAPI middleware
load_middleware(app, config)

# Set up FastAPI Prometheus metrics
metrics = Instrumentator()
metrics.instrument(app).expose(app)

# Set up FastAPI routers
install_routers(app)
