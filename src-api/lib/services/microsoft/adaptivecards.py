from enum import Enum
from pydantic import Field
from typing import Optional, Union
from models.base import BaseModel


class ItemTypeEnum(str, Enum):
    """Represents an Adaptive Card Item type."""
    Container = "Container"
    TextBlock = "TextBlock"


class ContainerStyleEnum(str, Enum):
    """Represents an Adaptive Card ContainerStyleEnum type."""
    default = "default"
    attention = "attention"
    good = "good"
    emphasis = "emphasis"


class TextBlockStyleEnum(str, Enum):
    """Represents an Adaptive Card TextBlockStyleEnum type."""
    default = "default"
    heading = "heading"


class ColorsEnum(str, Enum):
    """Represents an Adaptive Card Colors type."""
    default = "default"
    dark = "dark"
    light = "light"
    accent = "accent"
    good = "good"
    warning = "warning"
    attention = "attention"


class FontTypeEnum(str, Enum):
    """Represents an Adaptive Card FontType type."""
    default = "default"
    monospace = "monospace"


class HorizontalAlignmentEnum(str, Enum):
    """Represents an Adaptive Card HorizontalAlignment type."""
    left = "left"
    center = "center"
    right = "right"


class VerticalContentAlignmentEnum(str, Enum):
    """Represents an Adaptive Card VerticalContentAlignment type."""
    top = "top"
    center = "center"
    bottom = "bottom"


class FontSizeEnum(str, Enum):
    """Represents an Adaptive Card FontSize type."""
    default = "default"
    small = "small"
    medium = "medium"
    large = "large"
    extra_large = "extraLarge"


class FontWeightEnum(str, Enum):
    """Represents an Adaptive Card FontWeight type."""
    default = "default"
    lighter = "lighter"
    bolder = "bolder"


class Element(BaseModel):
    """Represents an Adaptive Card item."""

    type: ItemTypeEnum = Field(description="The Adaptive Card item type")
    """The Adaptive Card item type."""


class TextBlock(Element):
    """Represents an Adaptive Card text block."""

    type: ItemTypeEnum = Field(default=ItemTypeEnum.TextBlock, description="The Adaptive Card item type")
    """The Adaptive Card item type."""

    text: str = Field(description="The Adaptive Card TextBlock text")
    """The Adaptive Card TextBlock text."""

    color: ColorsEnum = Field(
        description="The Adaptive Card TextBlock color attribute",
        default=ColorsEnum.default,
    )
    """The Adaptive Card TextBlock color attribute."""

    font_type: FontTypeEnum = Field(
        description="The Adaptive Card TextBlock fontType attribute",
        default=FontTypeEnum.default,
        alias="fontType",
    )
    """The Adaptive Card TextBlock fontType attribute."""

    horizontal_alignment: HorizontalAlignmentEnum = Field(
        description="The Adaptive Card TextBlock horizontalAlignment attribute",
        default=HorizontalAlignmentEnum.left,
        alias="horizontalAlignment",
    )
    """The Adaptive Card TextBlock horizontalAlignment attribute."""

    is_subtle: bool = Field(
        description="Whether the Adaptive Card TextBlock text should be slightly toned down",
        default=False,
    )
    """Whether the Adaptive Card TextBlock text should be slightly toned down."""

    maxLines: int = Field(
        description="The Adaptive Card TextBlock maxLines attribute",
        default=None,
        alias="maxLines",
    )
    """The Adaptive Card TextBlock maxLines attribute."""

    size: FontSizeEnum = Field(
        description="The Adaptive Card TextBlock size attribute",
        default=FontSizeEnum.default,
    )
    """The Adaptive Card TextBlock size attribute."""

    weight: FontWeightEnum = Field(
        description="The Adaptive Card TextBlock weight attribute",
        default=FontWeightEnum.default,
    )
    """The Adaptive Card TextBlock weight attribute."""

    wrap: bool = Field(
        default=True,
        description="Whether the Adaptive Card TextBlock text should be wrapped",
    )
    """Whether the Adaptive Card TextBlock text should be wrapped."""

    style: TextBlockStyleEnum = Field(
        description="The Adaptive Card TextBlock style attribute",
        default=TextBlockStyleEnum.default,
    )
    """The Adaptive Card TextBlock style attribute."""


class Container(Element):
    """Represents an Adaptive Card Container item."""

    type: ItemTypeEnum = Field(
        description="The Adaptive Card item type",
        default=ItemTypeEnum.Container,
    )
    """The Adaptive Card item type."""

    items: list['ElementTypes'] = Field(
        description="The Adaptive Card items",
        default_factory=list,
        min_length=1,
    )
    """The Adaptive Card items."""

    style: Optional[ContainerStyleEnum] = Field(
        description="The Adaptive Card Container style attribute",
        default=ContainerStyleEnum.default,
    )
    """The Adaptive Card Container style attribute."""

    vertical_content_alignment: VerticalContentAlignmentEnum = Field(
        description="The Adaptive Card Container verticalContentAlignment attribute",
        default=VerticalContentAlignmentEnum.top,
    )
    """The Adaptive Card Container verticalContentAlignment attribute."""

    bleed: bool = Field(default=True, description="Whether the container has bleed")
    """Whether the container has bleed."""

    min_height: str = Field(
        description="The Adaptive Card Container minimum height in pixels e.g. \"80px\"",
        default=None,
        alias="minHeight",
    )
    """The Adaptive Card Container minimum height in pixels e.g. \"80px\""""

    rtl: bool = Field(
        description="Whether the Adaptive Card Container content should be presented right to left",
        default=False,
    )
    """Whether the Adaptive Card Container content should be presented right to left"""


ElementTypes = Union[TextBlock, Container]
