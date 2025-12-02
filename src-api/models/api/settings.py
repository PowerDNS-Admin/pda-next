from datetime import datetime, date, time
from typing import Optional

from pydantic import Field, computed_field

from models.api import BaseApiModel
from models.enums import SettingTypeEnum


class Setting(BaseApiModel):
    """Provides an interface for defining a system setting and applying it accordingly."""

    title: str = Field(
        title='Setting Title',
        description='The title of this setting.',
    )
    """The title of this setting."""

    description: str = Field(
        title='Setting Description',
        description='The description of this setting.',
    )
    """The description this setting."""

    tenant_id: Optional[str] = Field(
        title='Tenant ID',
        description='The tenant ID that this setting is associated with.',
        default=None,
    )
    """The tenant ID that this setting is associated with."""

    user_id: Optional[str] = Field(
        title='User ID',
        description='The user ID that this setting is associated with.',
        default=None,
    )
    """The user ID that this setting is associated with."""

    key: str = Field(
        title='Setting Key',
        description='The key of this setting.',
    )
    """The key of this setting."""

    data_type: SettingTypeEnum = Field(
        title='Setting Data Type',
        description="The data type of this setting's value.",
    )
    """The data type of this setting's value."""

    raw_value: Optional[str] = Field(
        title='Setting Data Raw Value',
        description="The raw value of this setting.",
        default=None,
    )
    """The raw value of this setting."""

    default_value: str | int | float | bool | datetime | date | time | tuple | list | dict = Field(
        title='Setting Default Value',
        description='The default value of this setting.',
    )
    """The default value of this setting."""

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

    @computed_field(
        title='Setting Value',
        description='The value of the setting.',
    )
    @property
    def value(self) -> str | int | float | bool | datetime | date | time | tuple | list | dict | None:
        """The value of the setting."""
        import json

        if self.raw_value is None:
            return None

        match self.data_type:
            case SettingTypeEnum.str:
                return str(self.raw_value)
            case SettingTypeEnum.int:
                return int(self.raw_value)
            case SettingTypeEnum.float:
                return float(self.raw_value)
            case SettingTypeEnum.bool:
                return bool(self.raw_value.lower())
            case SettingTypeEnum.datetime:
                return datetime.fromisoformat(self.raw_value)
            case SettingTypeEnum.date:
                return date.fromisoformat(self.raw_value)
            case SettingTypeEnum.time:
                return time.fromisoformat(self.raw_value)
            case SettingTypeEnum.tuple:
                return tuple(json.loads(self.raw_value))
            case SettingTypeEnum.list:
                return json.loads(self.raw_value)
            case SettingTypeEnum.dict:
                return json.loads(self.raw_value)
            case _:
                raise ValueError(f'Unknown setting type: {self.data_type}')

    @value.setter
    def value(self, value: str | int | float | bool | datetime | date | time | tuple | list | dict | None):
        """Sets the value of the setting."""
        import json

        value_type = type(value)

        if value is None:
            self.raw_value = None
        elif value_type in (str, int, float):
            self.raw_value = str(value)
        elif value_type == bool:
            self.raw_value = str(value).lower()
        elif value_type in (tuple, list, dict):
            self.raw_value = json.dumps(value)
        elif value_type in (datetime, date, time):
            self.raw_value = value.isoformat()
        else:
            raise ValueError(f'Unknown setting type: {value_type}')
