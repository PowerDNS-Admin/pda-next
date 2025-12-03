from fastapi import FastAPI
from app import lifespan
from lib import load_config, init_logging
from lib.config.app import EnvironmentEnum
from middleware import load_middleware

config = load_config()
init_logging(config)

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
    docs_url='/api/docs',
    redoc_url='/api/redoc',
    debug=config.app.environment.name in (EnvironmentEnum.local, EnvironmentEnum.dev),
    swagger_ui_parameters={
        'docExpansion': 'none',  # list, full, or none
        'displayRequestDuration': True,
        'filter': True,
        'tryItOutEnabled': True,
        'requestSnippetsEnabled': True,
        'persistAuthorization': True,
    },
)

# Set up FastAPI middleware
load_middleware(app, config)
