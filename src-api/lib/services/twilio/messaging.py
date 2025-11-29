from pydantic import Field
from typing import Optional
from models.base import BaseModel


class SMSMessage(BaseModel):
    """Provides a representation of a Twilio SMS message."""

    from_: Optional[str] = Field(
        description="The sender's phone number (in E.164 format).",
        alias="from",
        default=None,
    )
    """The sender's phone number (in E.164 format)."""

    to_: str = Field(
        description="The recipient's phone number J(in E.164 format) or channel address (e.g. whatsapp:+15552229999).",
        alias="to",
    )
    """The recipient's phone number J(in E.164 format) or channel address (e.g. whatsapp:+15552229999)."""

    body: str = Field(
        description="The text content of the message.",
    )
    """The text content of the message."""


class MMSMessage(SMSMessage):
    """Provides a representation of a Twilio MMS message."""

    media_url: Optional[list[str]] = Field(
        description="The URL of media to include in the Message content. jpeg, jpg, gif, and png file types are fully supported by Twilio and content is formatted for delivery on destination devices.",
        alias="mediaUrl",
    )
