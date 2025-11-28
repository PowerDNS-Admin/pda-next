from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from pydantic import ConfigDict, Field, computed_field
from typing import Optional, Union
from app.models.base import BaseModel

MESSAGE_TYPES = Union[EmailMessage, MIMEApplication, MIMEAudio, MIMEImage, MIMEMessage, MIMEMultipart, MIMEText]


class MIMEMultipartSubTypeEnum(str, Enum):
    """Defines the available subtypes for MIMEMultipart messages."""
    mixed = 'mixed'
    alternative = 'alternative'
    related = 'related'
    digest = 'digest'
    signed = 'signed'
    encrypted = 'encrypted'
    form_data = 'form-data'
    parallel = 'parallel'
    byteranges = 'byteranges'


class MIMETextSubTypeEnum(str, Enum):
    """Defines the available subtypes for MIMEText messages."""
    html = "html"
    plain = "plain"


class Message(BaseModel):
    """Provides a representation of an email message."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Allow arbitrary types so that the model can have attributes typed as EmailMessage."""

    sender: Optional[str] = Field(
        description="The sender of the email message",
        default=None,
    )
    """The email address of the sender."""

    recipients: list[str] = Field(
        description="The recipients of the email message",
        default_factory=list,
        min_length=1,
    )
    """The recipients of the email message."""

    cc: Optional[list[str]] = Field(
        description="The carbon copy recipients of the email message",
        default=None,
    )
    """The carbon copy recipients of the email message."""

    bcc: Optional[list[str]] = Field(
        description="The below carbon copy recipients of the email message",
        default=None,
    )
    """The below carbon copy recipients of the email message."""

    subject: Optional[str] = Field(
        description="The subject of the email message",
        default=None,
    )
    """The subject of the email message."""

    attachments: Optional[list[MESSAGE_TYPES]] = Field(
        description="The attachments of the email message which includes text bodies and files",
        default=None,
    )
    """The attachments of the email message which includes text bodies and files."""

    multipart_subtype: MIMEMultipartSubTypeEnum = Field(
        description="The subtype of MIMEMultipart messages",
        default=MIMEMultipartSubTypeEnum.alternative,
    )
    """The subtype of MIMEMultipart messages."""

    individual_recipients: bool = Field(
        description="Whether to send separate emails for each recipient or as one single email",
        default=True,
    )
    """Whether to send separate emails for each recipient or as one single email."""

    def add_attachment(self, attachment: MESSAGE_TYPES):
        """Adds an attachment to the email message."""
        if not isinstance(self.attachments, list):
            self.attachments = [attachment]
        else:
            self.attachments.append(attachment)

    def add_application_attachment(self, path: str, mime_type: str = 'octet-stream', content_id: Optional[str] = None):
        """Adds an application attachment to the email message."""
        import os
        from pathlib import Path

        if not isinstance(path, str):
            raise TypeError("Attachment path must be a string")

        if not len(path.strip()):
            raise ValueError("Attachment path must not be empty")

        file_path = Path(path)

        if not file_path.exists():
            raise ValueError("Attachment path does not exist")

        if not file_path.is_file():
            raise ValueError("Attachment path is not a file")

        message = MIMEApplication(file_path.read_bytes(), mime_type)

        # Set the filename
        message.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))

        if isinstance(content_id, str) and len(content_id.strip()):
            message.add_header('Content-ID', f'<{content_id}>')

        self.add_attachment(message)

    def add_text_attachment(self, text: str, subtype: MIMETextSubTypeEnum = MIMETextSubTypeEnum.plain):
        """Adds a text attachment to the email message."""
        from email.mime.text import MIMEText

        if not isinstance(text, str):
            raise TypeError("Email text attachment must be a string")

        if not len(text.strip()):
            raise ValueError("Email text attachment must not be empty")

        self.add_attachment(MIMEText(text, subtype.value))

    def create_messages(self) -> Union[list[MESSAGE_TYPES], MESSAGE_TYPES]:
        """
        Creates the appropriate MIMEBase subclass objects for this email message depending on how many attachments
        are present.

        Returns the MIME message directly if there will be only one email generated or a list of MIME message objects
        if there will be multiple recipients with the "individual_recipients" option set to True.
        """
        import copy

        if not self.attachments:
            message = EmailMessage()

        elif isinstance(self.attachments, list) and len(self.attachments) == 1:
            message = self.attachments[0]

        else:
            message = MIMEMultipart(self.multipart_subtype.value)
            for attachment in self.attachments:
                message.attach(attachment)

        if isinstance(self.sender, str) and len(self.sender.strip()):
            message['From'] = self.sender

        if isinstance(self.subject, str) and len(self.subject.strip()):
            message['Subject'] = self.subject

        if isinstance(self.cc, list) and self.cc:
            message['Cc'] = ', '.join(self.cc)

        if isinstance(self.bcc, list) and self.bcc:
            message['Bcc'] = ', '.join(self.bcc)

        if not self.recipients:
            return message

        if isinstance(self.recipients, list):
            if self.individual_recipients:
                messages = []
                for recipient in self.recipients:
                    msg = copy.deepcopy(message)
                    msg['To'] = recipient
                    messages.append(msg)
                if len(messages) == 1:
                    return messages[0]
                return messages
            else:
                for recipient in self.recipients:
                    message['To'] = recipient
                return message

        return message


class EmailDeliveryRecipientResponse(BaseModel):
    """Provides a representation of email delivery responses for an email delivery attempt of a specific recipient."""

    recipient: str = Field(description="The recipient of the email message")
    """The recipient of the email message."""

    code: int = Field(
        description="The response code of the delivery attempt",
        default=250,
    )
    """The response code of the delivery attempt."""

    message: Optional[str] = Field(description="The response message of the delivery attempt")
    """The response message of the delivery attempt."""

    @computed_field
    @property
    def success(self) -> bool:
        """Whether the delivery attempt was successful for the recipient."""
        return 200 <= self.code <= 300


class EmailDeliveryResult(BaseModel):
    """Provides a representation of email delivery result for an email delivery attempt."""

    responses: list[EmailDeliveryRecipientResponse] = Field(
        description="The response objects representing each recipient of the delivery attempt",
        default_factory=list,
        min_length=1,
    )
    """The response objects representing each recipient of the delivery attempt."""

    @computed_field
    @property
    def success(self) -> bool:
        """Whether the delivery attempt was successful for all recipients."""

        for response in self.responses:
            if not response.success:
                return False

        return True
