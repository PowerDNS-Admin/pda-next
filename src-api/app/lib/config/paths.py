from typing import Union
from app.models.base import BaseConfig


class PathsConfig(BaseConfig):
    """A model that represents a configuration hierarchy for file system paths."""
    templates: Union[str, list[str]] = 'src/templates'
