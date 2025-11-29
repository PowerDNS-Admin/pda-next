from typing import Optional
from models.base import BaseModel


class NotFoundResponse(BaseModel):
    """A response to a request for a resource that does not exist."""
    success: bool = False
    message: Optional[str] = 'The requested resource could not be found.'

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'success': False,
                    'message': 'The requested resource could not be found.',
                }
            ]
        }
    }


class StatusResponse(BaseModel):
    """A response to a request for the system status."""
    status: str = 'ONLINE'

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'status': 'ONLINE',
                }
            ]
        }
    }


class OperationResponse(BaseModel):
    """A generic response to an operation."""
    success: bool = True
    message: Optional[str] = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'success': True,
                    'message': 'Operation completed successfully',
                }
            ]
        }
    }
