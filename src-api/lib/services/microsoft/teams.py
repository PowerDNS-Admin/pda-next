from enum import Enum
from pydantic import Field
from typing import Optional, Union
from lib.services.microsoft.adaptivecards import ElementTypes, ContainerStyleEnum
from models.base import BaseModel


class MessageActionType(str, Enum):
    """Represents an Adaptive Card Message Action type."""
    OpenUrl = "Action.OpenUrl"


class MessageAction(BaseModel):
    """Represents a Microsoft Teams Message action."""

    type: MessageActionType = Field(description="The type of the action")
    """The type of the action."""


class MessageActionOpenUrl(MessageAction):
    """Represents a Microsoft Teams Message URL open action."""

    type: MessageActionType = Field(
        description="The type of the action",
        default=MessageActionType.OpenUrl,
    )
    """The type of the action."""

    title: str = Field(
        description="The title of the action",
        default="View in Browser",
    )
    """The title of the action."""

    url: str = Field(description="The URL of the action")
    """The URL of the action."""


ActionTypes = Union[MessageAction, MessageActionOpenUrl]


class MessageAttachment(BaseModel):
    """Represents a Microsoft Teams message attachment."""

    content_type: str = Field(
        description="The content type of the message attachment",
        alias="contentType",
    )
    """The content type of the message attachment."""


class AdaptiveCardMessageAttachment(MessageAttachment):
    """Represents a Microsoft Teams Adaptive Card message attachment."""

    class Content(BaseModel):
        """Represents a Microsoft Teams Adaptive Card message attachment content object."""

        schema_: str = Field(
            description="The schema of the content object.",
            alias="$schema",
            default="http://adaptivecards.io/schemas/adaptive-card.json",
        )
        """The schema of the content object."""

        type: str = Field(
            description="The type of the content object.",
            default="AdaptiveCard",
        )
        """The type of the content object."""

        version: str = Field(
            description="The version of the content object.",
            default="1.2",
        )
        """The version of the content object."""

        body: list[ElementTypes] = Field(
            description="The body of the content object.",
            default_factory=list,
            min_length=1,
        )
        """The body of the content object."""

        actions: list[ActionTypes] = Field(
            description="The actions attached to the content object.",
            default_factory=list,
        )

    content_type: str = Field(
        description="The content type of the message attachment",
        alias="contentType",
        default="application/vnd.microsoft.card.adaptive",
    )
    """The content type of the message attachment."""

    content: Content = Field(
        description="The content object of the message attachment",
        default_factory=Content,
    )
    """The content object of the message attachment."""


class Message(BaseModel):
    """Represents a Microsoft Teams message."""

    type: str = Field(
        description="The type of the message",
        default="message",
    )
    """The type of the message."""

    attachments: list[AdaptiveCardMessageAttachment] = Field(
        description="A list of attachments attached to the message",
        default_factory=list,
        min_length=1,
    )
    """The list of attachments attached to the message."""


class MessageFactory:
    """Represents a Microsoft Teams Message factory."""

    @staticmethod
    def create_simple_message(
            segments: list[str], title: Optional[str] = None, style: Optional[ContainerStyleEnum] = None,
            action_url: Optional[str] = None, action_title: Optional[str] = None,
    ) -> Message:
        """This method is used to create a simple Microsoft Teams message."""
        from lib.services.microsoft.adaptivecards import (
            Container, TextBlock, FontSizeEnum, FontWeightEnum
        )

        attachment = AdaptiveCardMessageAttachment()

        if isinstance(title, str) and len(stripped_title := title.strip()):
            container = Container()

            if isinstance(style, ContainerStyleEnum):
                container.style = style

            container.items.append(TextBlock(
                text=stripped_title,
                size=FontSizeEnum.medium,
                weight=FontWeightEnum.bolder,
                wrap=True,
            ))

            attachment.content.body.append(container)

        for segment in segments:
            attachment.content.body.append(TextBlock(
                text=segment,
                wrap=True,
                size=FontSizeEnum.medium,
            ))

        if isinstance(action_url, str) and len(stripped_action_url := action_url.strip()):
            action = MessageActionOpenUrl(url=stripped_action_url)
            if isinstance(action_title, str) and len(stripped_action_title := action_title.strip()):
                action.title = stripped_action_title

            attachment.content.actions.append(action)

        return Message(attachments=[attachment])
