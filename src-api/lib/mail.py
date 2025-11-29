from smtplib import SMTP
from typing import Optional, Union
from lib.config.mail import MailConfig
from lib.services.email import MESSAGE_TYPES
from models.base import BaseModel


class SmtpClientException(Exception):
    """Provides a custom exception class for the SmtpClient class."""
    pass


class SmtpClient:
    """Provides a simple interface for instantiating SMTP client objects."""

    _connection: Optional[SMTP] = None
    """The SMTP connection object."""

    _servers: list[MailConfig.MailServer]
    """A list of SMTP MailServer configuration objects."""

    _server: Optional[MailConfig.MailServer] = None
    """The currently selected SMTP MailServer configuration object."""

    _server_index: Optional[int] = None
    """The currently selected SMTP MailServer configuration object index."""

    def __enter__(self, servers: Optional[list[MailConfig.MailServer]] = None) -> 'SmtpClient':
        """Opens a new SMTP connection and attempts to authenticate."""
        if not isinstance(servers, list):
            from app import config
            servers = config.mail.servers if isinstance(config.mail.servers, list) else []

        if not servers:
            raise SmtpClientException('SmtpClient requires at least one SMTP server configuration!')

        self._servers = servers

        self._find_server()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the open SMTP connection."""
        self._disconnect()

    def _connect(self) -> bool:
        from socket import timeout
        from loguru import logger
        from smtplib import SMTP_SSL, SMTPException

        logger.trace(f'SmtpClient connecting to server "{self._server.alias}".')

        try:
            if self._server.ssl:
                self._connection = SMTP_SSL(host=self._server.host, port=self._server.port,
                                            local_hostname=self._server.local_hostname,
                                            keyfile=self._server.keyfile,
                                            certfile=self._server.certfile, timeout=self._server.timeout,
                                            source_address=self._server.source_address)

            else:
                self._connection = SMTP(host=self._server.host, port=self._server.port,
                                        local_hostname=self._server.local_hostname, timeout=self._server.timeout,
                                        source_address=self._server.source_address)

        except (SMTPException, timeout) as e:
            logger.error(f'Failed to connect to SMTP server "{self._server.alias}": {e}')
            return False

        if self._server.ssl and self._server.tls:
            raise SmtpClientException(f'The mail server "{self._server.alias}" has both SSL and TLS enabled and the '
                                      + 'two are mutually exclusive.')

        if self._server.tls:
            self._connection.starttls()

        logger.trace(f'SmtpClient authenticating to server "{self._server.alias}".')

        try:
            self._connection.login(self._server.username, self._server.password)
        except SMTPException as e:
            logger.error(f'Failed to login to SMTP server "{self._server.alias}": {e}')
            return False

        return True

    def _disconnect(self):
        from loguru import logger
        from smtplib import SMTPServerDisconnected

        if self._connection is not None:
            try:
                self._connection.quit()
            except SMTPServerDisconnected:
                logger.trace(f'SmtpClient server already disconnected: {self._server.alias}.')
                pass

    def _next_server(self):
        from loguru import logger

        self._disconnect()

        try:
            self._server_index = self._servers.index(self._server) + 1
        except ValueError:
            self._server_index = 0

        try:
            self._server = self._servers[self._server_index]
        except IndexError:
            raise SmtpClientException('SmtpClient has no additional server configurations to attempt delivery with!')

        logger.trace(f'SmtpClient selecting server "{self._server.alias}".')

    def _find_server(self):
        self._next_server()
        while not self._connect():
            self._next_server()

    def send_message(self, message: MESSAGE_TYPES, from_address=None, to_addresses=None,
                     mail_options=(), rcpt_options=()) -> dict:
        from loguru import logger
        from smtplib import SMTPException
        from lib.decorators import redis_throttle, ThrottleException

        while True:
            try:

                if not message['From'] or message['From'] is None:
                    del message['From']

                    if isinstance(self._server.from_address, str):
                        message['From'] = self._server.from_address

                    elif isinstance(self._server.username, str):
                        message['From'] = self._server.username

                    else:
                        raise SmtpClientException(f'Invalid from address: {message["From"]}')

                throttle_key = self._server.throttle.key

                if not isinstance(throttle_key, str):
                    throttle_key = 'SmtpClient'

                throttle_key += f'-server-{self._server_index}'

                throttler = redis_throttle(
                    calls=self._server.throttle.threshold,
                    period=self._server.throttle.period,
                    mode=self._server.throttle.mode,
                    key=throttle_key,
                    backoff_strategy=self._server.throttle.backoff_strategy,
                    backoff_base=self._server.throttle.backoff_base,
                    backoff_cap=self._server.throttle.backoff_cap,
                    jitter=self._server.throttle.jitter,
                )(lambda: self._connection.send_message(message, from_address, to_addresses, mail_options,
                                                        rcpt_options))

                return throttler()
            except SMTPException as e:
                logger.error(f'Failed to send message via SMTP server "{self._server.alias}": {e}')
                self._find_server()
            except ThrottleException as e:
                logger.warning(f'Failed to send message via SMTP server "{self._server.alias}" due to throttle limit: '
                               + f'{e}')
                self._find_server()


class EmailSendRecipientResponse(BaseModel):
    """Provides a result object for email send operations to track the result of each recipient."""
    recipient: str
    success: bool
    code: int
    message: Optional[str] = None


class EmailSendResult(BaseModel):
    """Provides a result object for email send operations to track the result of each recipient."""
    responses: list[EmailSendRecipientResponse] = []


class Email(BaseModel):
    """Provides a data model that represents an email message."""

    template_path: Union[str, None] = None
    subject: Union[str, None] = None
    body_html: Union[str, None] = None
    body_text: Union[str, None] = None
    data: Union[dict, None] = None
    mail_from: Union[str, None] = None
    mail_to: Union[str, list[str], None] = None
    mail_cc: Union[str, list[str], None] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Validate that at least one mail to address was provided
        if not self.mail_to:
            raise ValueError('Failed to initialize because mail_to is empty!')

        if self.template_path is not None:
            self.render()

    def render(self):
        """Renders the configured templates into the appropriate email properties."""
        from loguru import logger
        from pathlib import Path
        from app import config, j2

        if self.template_path is None:
            raise ValueError('Failed to render email templates because template_path is None!')

        tpl_path = Path(f'{config.paths.templates}/{self.template_path}')

        if not tpl_path.exists():
            raise RuntimeError('Failed to render email templates because the template path '
                               + f'"{self.template_path}" does not exist!')

        if not isinstance(self.data, dict):
            self.data = {}

        # Attempt to locate and render subject template if subject not already set
        if self.subject is None:
            subject_path = tpl_path / 'subject.jinja2'
            if not subject_path.exists():
                logger.debug(f'Email subject template not found: {subject_path}')
            else:
                self.subject = j2.get_template(f'{self.template_path}/subject.jinja2').render(**self.data)

        # Attempt to locate and render HTML body template if HTML body not already set
        if self.body_html is None:
            html_body_path = tpl_path / 'body_html.jinja2'
            if not html_body_path.exists():
                logger.debug(f'Email HTML body template not found: {html_body_path}')
            else:
                self.body_html = j2.get_template(f'{self.template_path}/body_html.jinja2').render(**self.data)

        # Attempt to locate and render text body template if text body not already defined
        if self.body_text is None:
            text_body_path = tpl_path / 'body_text.jinja2'
            if not text_body_path.exists():
                logger.debug(f'Email TEXT body template not found: {text_body_path}')
            else:
                self.body_text = j2.get_template(f'{self.template_path}/body_text.jinja2').render(**self.data)

    def send(self) -> EmailSendResult:
        """Sends the email to the configured recipient(s) and returns a boolean representing whether the email was
        sent."""
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from loguru import logger

        recipients = self.mail_to if isinstance(self.mail_to, list) else [self.mail_to]
        messages = []
        subject = self.subject

        if isinstance(subject, str):
            subject = subject.replace('\n', '').strip()

        for recipient in recipients:
            message = MIMEMultipart('alternative')
            message['To'] = recipient
            message['Subject'] = subject

            if isinstance(self.mail_cc, list):
                for cc_recipient in self.mail_cc:
                    message['Cc'] = cc_recipient
            elif isinstance(self.mail_cc, str):
                message['Cc'] = self.mail_cc

            if isinstance(self.mail_from, str):
                message['From'] = self.mail_from

            if isinstance(self.body_html, str) and len(self.body_html.strip()):
                message.attach(MIMEText(self.body_html, 'html'))

            if isinstance(self.body_text, str) and len(self.body_text.strip()):
                message.attach(MIMEText(self.body_text, 'plain'))

            messages.append(message)

        send_result = EmailSendResult()

        with SmtpClient() as client:
            for message in messages:
                result: dict[str, tuple[int, Optional[str]]] = client.send_message(message)

                if not result:
                    result = {message['To']: (250, None)}

                for recipient, response in result.items():
                    logger.trace(f'Email Send Response: Recipient: {recipient}, Code: {response[0]}, '
                                 + f'Message: {response[1]}')

                    send_result.responses.append(EmailSendRecipientResponse(
                        recipient=recipient,
                        success=response[0] < 300,
                        code = response[0],
                        message = response[1],
                    ))

        return send_result

    @staticmethod
    def build_rendered_conf(**kwargs) -> dict:
        mail = Email(**kwargs)
        return {
            'subject': mail.subject,
            'body_html': mail.body_html,
            'body_text': mail.body_text,
            'mail_from': mail.mail_from,
            'mail_to': mail.mail_to,
        }
