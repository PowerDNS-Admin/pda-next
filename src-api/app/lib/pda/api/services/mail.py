import uuid
from pydantic import Field
from typing import Optional, Union
from app.lib.mail import EmailSendRecipientResponse
from app.models.base import BaseModel


class MailServiceSendRequest(BaseModel):
    """Represents an API request for sending an email via the mail service router."""
    from_address: Optional[str] = Field(
        title='Email Sender Address',
        description='The email address to use in the mail "From" field. If left empty then the server default will be used.',
        examples=['Your Name <your.name@domain.com>', 'admin@domain.com', 'Server <server@localhost>'],
        default=None,
    )
    to_addresses: Union[list[str], str] = Field(
        ...,
        title='Email Recipients',
        description='One or more email addresses to deliver the mail to. May be expressed as an array of strings containing one email each or a single string with a single recipient.',
        examples=[['Your Name <your.name@domain.com>', 'somebody@domain.com'], 'Your Name <your.name@domain.com',
                  'somebody@domain.com'],
    )
    cc_addresses: Optional[Union[list[str], str]] = Field(
        title='Email CC Recipients',
        description='One or more email addresses to deliver the mail to as carbon copies. May be expressed as an array of strings containing one email each or a single string with a single recipient.',
        examples=[['Your Name <your.name@domain.com>', 'somebody@domain.com'], 'Your Name <your.name@domain.com',
                  'somebody@domain.com'],
        default=None,
    )
    subject: Optional[str] = Field(
        title='Email Subject',
        description='The subject line of the email.',
        examples=['Account Notification'],
        default=None,
    )
    body_html: Optional[str] = Field(
        title='Email HTML Body',
        description='The HTML body of the email.',
        examples=['<h1>Submission Received!</h1><p>We want to notify you that we received your submission.</p>'],
        default=None,
    )
    body_plain: Optional[str] = Field(
        title='Email Plain Text Body',
        description='The plain text body of the email.',
        examples=['Submission Received!\n\nWe want to notify you that we received your submission.'],
        default=None,
    )


class MailServiceSendResponse(BaseModel):
    """Represents an API response for sending an email via the mail service router."""

    id: Optional[uuid.UUID] = Field(
        title='Mail Request ID',
        description='The UUID associated with the mail request task.',
        examples=[str(uuid.uuid4())],
        default=None,
    )

    status: str = Field(
        title='Mail Request Status',
        description='The status of the mail request.',
        examples=['queued', 'sending', 'sent', 'retry', 'failed', 'not-found'],
        default='queued',
    )

    message: str = Field(
        title='Mail Request Response Message',
        description='Message related to the mail request response.',
        examples=['The mail request could not be queued for sending.'],
        default=None,
    )

    responses: list[EmailSendRecipientResponse] = Field(
        title='Mail Request Response Objects',
        description='A list of response objects of send action for each recipient.',
        examples=[
            EmailSendRecipientResponse(recipient='Recipient #1 <recipient1@domain.com>', success=True, code=250),
            EmailSendRecipientResponse(recipient='Recipient #2 <recipient2@domain.com>', success=False, code=450,
                                       message='This mailbox is unavailable.'),
            EmailSendRecipientResponse(recipient='recipient3@domain.com', success=True, code=250),
        ],
        default=None,
    )
