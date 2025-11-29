from pydantic import ConfigDict
from models import BaseModel


class BaseApiModel(BaseModel):
    """Provides an abstract API schema class."""
    model_config = ConfigDict(from_attributes=True)
