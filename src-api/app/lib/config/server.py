from typing import Union
from app.models.base import BaseConfig


class ServerConfig(BaseConfig):
    """A model that represents a configuration hierarchy for the HTTP server."""

    class MiddlewareConfig(BaseConfig):
        name: str
        config: Union[dict, None] = None

    proxy_root: str = '/'
    middleware: list[MiddlewareConfig] = []
