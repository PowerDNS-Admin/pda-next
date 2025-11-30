from fastapi import FastAPI
from lib.config import Config


def load_middleware(app:FastAPI, config: Config):
    import importlib
    from loguru import logger
    from lib.security import SESSION_AGE
    from middleware import SessionMiddleware

    # Set up session middleware
    # app.add_middleware(
    #     SessionMiddleware,
    #     secret_key=config.app.secret_key,
    #     https_only=True,
    #     same_site='strict',
    #     max_age=COOKIE_AGE,
    # )

    # Load middleware defined in server configuration
    if config.server.middleware:
        for middleware in config.server.middleware:
            logger.debug(f'Loading FastAPI middleware: {middleware.name}')
            mw_parts = middleware.name.split('.')
            mw_mod = importlib.import_module('.'.join(mw_parts[:-1]))
            mw = getattr(mw_mod, mw_parts[-1])
            app.add_middleware(mw, **middleware.config if middleware.config else {})
