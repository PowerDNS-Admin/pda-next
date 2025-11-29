import uuid
from datetime import datetime
from pydantic import ConfigDict
from typing import Optional
from models.base import BaseModel


class UserSchema(BaseModel):
    """Represents an authentication user for API interactions."""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[uuid.UUID] = None
    tenant_id: Optional[uuid.UUID] = None
    username: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    authenticated_at: Optional[datetime] = None


class ClientSchema(BaseModel):
    """Represents an authentication client for API interactions."""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[uuid.UUID] = None
    tenant_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    name: str
    redirect_uri: str
    scopes: list[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
