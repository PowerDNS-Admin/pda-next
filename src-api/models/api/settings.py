from datetime import datetime, date, time
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class SettingIn(BaseApiModel):
    """Provides an API input model for a system setting."""

    key: str = Field(
        title='Setting Key',
        description='The key of this setting.',
    )
    """The key of this setting."""

    value: Optional[str] = Field(
        title='Setting Value',
        description="The value of this setting.",
        default=None,
    )
    """The value of this setting."""

    overridable: bool = Field(
        title='Setting Overridable',
        description='Whether the setting can be overridden in lower contexts.',
        default=False,
    )
    """Whether the setting can be overridden in lower contexts."""

    hidden: bool = Field(
        title='Setting Hidden',
        description='Whether the setting is hidden in lower contexts.',
        default=False,
    )
    """Whether the setting is hidden in lower contexts."""

    readonly: bool = Field(
        title='Setting Read-Only',
        description='Whether the setting can be modified in non-system contexts.',
        default=False,
    )
    """Whether the setting can be modified in non-system contexts."""


class SettingOut(BaseApiModel):
    """Provides an API response model for a system setting."""

    id: Optional[UUID] = Field(
        title='ID',
        description='The unique identifier of this setting.',
        examples=[uuid4()],
    )
    """The unique identifier of this setting."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The tenant ID that this setting is associated with if any.',
        default=None,
        examples=[uuid4()],
    )
    """The tenant ID that this setting is associated with."""

    user_id: Optional[UUID] = Field(
        title='User ID',
        description='The user ID that this setting is associated with if any.',
        default=None,
        examples=[uuid4()],
    )
    """The user ID that this setting is associated with."""

    key: str = Field(
        title='Setting Key',
        description='The key of this setting.',
    )
    """The key of this setting."""

    value: Optional[str | int | float | bool | datetime | date | time | tuple | list | dict] = Field(
        title='Setting Value',
        description="The value of this setting.",
        default=None,
    )
    """The value of this setting."""

    overridable: bool = Field(
        title='Setting Overridable',
        description='Whether the setting can be overridden in lower contexts.',
        default=False,
    )
    """Whether the setting can be overridden in lower contexts."""

    hidden: bool = Field(
        title='Setting Hidden',
        description='Whether the setting is hidden in lower contexts.',
        default=False,
    )
    """Whether the setting is hidden in lower contexts."""

    readonly: bool = Field(
        title='Setting Read-Only',
        description='Whether the setting can be modified in non-system contexts.',
        default=False,
    )
    """Whether the setting can be modified in non-system contexts."""

    created_at: Optional[datetime] = Field(
        title='Setting Created Timestamp',
        description='The date and time the setting was created.',
        default=None,
    )
    """The date and time the setting was created."""

    updated_at: Optional[datetime] = Field(
        title='Setting Updated Timestamp',
        description='The date and time the setting was updated.',
        default=None,
    )
    """The date and time the setting was updated."""


class SettingsOut(BaseApiModel):
    """Provides an API response model for a list of system settings."""

    settings: list[SettingOut] = Field(
        title='Current Context Settings',
        description='The settings of the current authentication context.',
        default=[],
        examples=[[SettingOut(
            id=uuid4(), tenant_id=uuid4(), user_id=uuid4(), key='auth:session:max_age', value=3600,
        )]],
    )
