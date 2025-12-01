from typing import Any, Literal

from pydantic import Field

from models.api import BaseApiModel


class BaseSetting(BaseApiModel):
    """Provides an interface for defining a system setting and applying it accordingly."""

    type: Literal['any'] = Any
    """The value type of the setting."""

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

    key: str = Field(
        title='Setting Key',
        description='The key of this setting.',
    )
    """The key of this setting."""

    value: Any = Field(
        title='Default Setting Value',
        description='The default value of this setting.',
    )
    """The default value of this setting."""

    overridable: bool = Field(
        title='Setting Overridable',
        description='Whether the setting can be overridden in lower contexts.',
        default=False,
    )
    """Whether the setting can be overridden in lower contexts."""

    readonly: bool = Field(
        title='Setting Read-Only',
        description='Whether the setting can be modified in non-system contexts.',
        default=False,
    )
    """Whether the setting can be modified in non-system contexts."""


class StringSetting(BaseSetting):
    """Provides an interface for defining a string-type system setting and applying it accordingly."""

    type: Literal['str']
    """The value type of the setting."""

    value: str
    """The default value of this setting."""


class IntSetting(BaseSetting):
    """Provides an interface for defining a int-type system setting and applying it accordingly."""

    type: Literal['int']
    """The value type of the setting."""

    value: int
    """The default value of this setting."""


class FloatSetting(BaseSetting):
    """Provides an interface for defining a float-type system setting and applying it accordingly."""

    type: Literal['float']
    """The value type of the setting."""

    value: float
    """The default value of this setting."""


class BoolSetting(BaseSetting):
    """Provides an interface for defining a bool-type system setting and applying it accordingly."""

    type: Literal['bool']
    """The value type of the setting."""

    value: bool
    """The default value of this setting."""


# TODO: Implement a JSON type for automatic conversion

Setting = StringSetting | IntSetting | FloatSetting | BoolSetting
"""Mash all the types together to make a delicious potato. ( ͡ᵔ ͜ʖ ͡ᵔ )"""
