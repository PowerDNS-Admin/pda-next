from billiard.einfo import ExceptionInfo
from celery.app.task import Task, Context
from celery.worker.request import Request
from datetime import datetime
from kombu.transport.virtual.base import Message
from pydantic import PrivateAttr, ConfigDict, model_validator
from typing import Any, Optional, Union
from zoneinfo import ZoneInfo
from app.lib.enums import NotificationCategoryEnum
from app.models.base import BaseModel

UTC_TZ = ZoneInfo('UTC')
BLOCK_STYLES = ("font-family: monospace, Consolas, 'Courier New', sans-serif; background-color: #f4f4f4; "
                + "padding: 15px; border: 1px solid #dddddd; font-size: 13px; line-height: 1.4; "
                + "white-space: pre-wrap; word-wrap: break-word;")


class TaskInfoMixin:
    """Provides a mixin for notification events that contain task information."""

    @property
    def task_info_plain(self) -> Optional[str]:
        """Defines the formatted task information in plain format of the notification event (if applicable)."""
        import json

        message = ''
        info = None

        if hasattr(self, 'request') and isinstance(self.request, Request):
            info = self.request

        elif hasattr(self, 'context') and isinstance(self.context, Context):
            info = self.context

        if info is None:
            return None

        if info.id is not None:
            message += f'Task ID: {info.id}\n'

        if info.root_id is not None:
            message += f'Root ID: {info.root_id}\n'

        if info.parent_id is not None:
            message += f'Parent ID: {info.parent_id}\n'

        if isinstance(info.args, str) and len(info.args.strip()):
            message += f'\nArguments:\n{json.dumps(json.loads(info.args), indent=4)}\n'

        if isinstance(info.kwargs, str) and len(info.kwargs.strip()):
            message += f'\nKeyword Arguments:\n{json.dumps(json.loads(info.kwargs), indent=4)}\n'

        return message.rstrip() or None

    @property
    def task_info_html(self) -> Optional[str]:
        """Defines the task information in HTML format of the notification event (if applicable)."""
        import html, json

        message = ''
        info = None

        if hasattr(self, 'request') and isinstance(self.request, Request):
            info = self.request

        elif hasattr(self, 'context') and isinstance(self.context, Context):
            info = self.context

        if info is None:
            return None

        if info.id is not None:
            message += f'<p style="margin-bottom: 10px;"><strong>Task ID:</strong> {info.id}</p>\n'

        if info.root_id is not None:
            message += f'<p style="margin-bottom: 10px;"><strong>Root ID:</strong> {info.root_id}</p>\n'

        if info.parent_id is not None:
            message += f'<p style="margin-bottom: 10px;"><strong>Parent ID:</strong> {info.parent_id}</p>\n'

        if isinstance(info.args, str) and len(info.args.strip()):
            message += f'<p style="margin-bottom: 10px;"><strong>Arguments:</strong></p>\n'
            message += (f'<div style="margin-bottom: 10px; {BLOCK_STYLES}"><pre>'
                        + f'{html.escape(json.dumps(json.loads(info.args), indent=4))}</pre></div>\n')

        if isinstance(info.kwargs, str) and len(info.kwargs.strip()):
            message += f'<p style="margin-bottom: 10px;"><strong>Keyword Arguments:</strong></p>\n'
            message += (f'<div style="margin-bottom: 10px; {BLOCK_STYLES}"><pre>'
                        + f'{html.escape(json.dumps(json.loads(info.kwargs), indent=4))}</pre></div>\n')

        return message.rstrip() or None


class ExceptionEventMixin:
    """Provides a mixin for notification events that contain exception information."""

    @property
    def exception_traceback(self) -> Optional[str]:
        """Defines the formatted traceback of the associated exception information (if applicable)."""
        import traceback

        if hasattr(self, 'exception') and isinstance(self.exception, Exception):
            return ''.join(traceback.format_exception(
                type(self.exception),
                self.exception,
                self.exception.__traceback__,
            ))

        if hasattr(self, 'einfo') and isinstance(self.einfo, ExceptionInfo):
            return self.einfo.traceback

        return None

    @property
    def exception_info_plain(self) -> Optional[str]:
        """Defines the message exception in plain format of the notification event (if applicable)."""

        if isinstance(formatted_exception := self.exception_traceback, str):
            return f'\nException Info:\n{formatted_exception}'

        return None

    @property
    def exception_info_html(self) -> Optional[str]:
        """Defines the message exception in HTML format of the notification event (if applicable)."""
        import html

        if isinstance(formatted_exception := self.exception_traceback, str):
            return (f'<p style="margin-bottom: 10px;"><strong>Exception Info:</strong></p>\n'
                    + f'<div style="margin-bottom: 10px; {BLOCK_STYLES}"><pre>'
                    + f'{html.escape(formatted_exception)}</pre></div>')

        return None


class NotificationEvent(BaseModel):
    """Defines a generic event used for metadata when generating notifications."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Allow arbitrary types so that the models can have attributes typed as Exceptions."""

    timestamp: Optional[datetime] = None
    """Defines the timestamp of the event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = None
    """Defines the notification category for the event (if applicable)."""

    @model_validator(mode='after')
    def set_timestamp(self) -> 'NotificationEvent':
        """After instantiation, set the event timestamp."""
        if self.timestamp is None:
            self.timestamp = datetime.now(tz=UTC_TZ)
        return self

    @property
    def message_subject(self) -> Optional[str]:
        """Defines the message subject of the event (if applicable)."""
        raise NotImplementedError()

    @property
    def message_title(self) -> Optional[str]:
        """Defines the message title of the event (if applicable)."""
        raise NotImplementedError()

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the event (if applicable)."""
        raise NotImplementedError()

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the event (if applicable)."""
        raise NotImplementedError()


class AlertEvent(ExceptionEventMixin, NotificationEvent):
    """Defines a generic event used for alert notifications."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.ALERT
    """Defines the notification category for the event."""

    subject: Optional[str] = None
    """Defines the subject of the notification event (if applicable)."""

    title: Optional[str] = None
    """Defines the title of the notification event (if applicable)."""

    message: Optional[str] = None
    """Defines the message of the notification event (if applicable)."""

    exception: Optional[Exception] = None
    """Defines the exception associated with the event (if applicable)."""

    @property
    def message_subject(self) -> Optional[str]:
        """Defines the message subject of the notification event (if applicable)."""

        if isinstance(self.subject, str) and len(self.subject.strip()):
            return self.subject

        if isinstance(self.title, str) and len(self.title.strip()):
            return self.title

        return None

    @property
    def message_title(self) -> Optional[str]:
        """Defines the message title of the notification event (if applicable)."""

        if isinstance(self.title, str) and len(self.title.strip()):
            return self.title

        if isinstance(self.subject, str) and len(self.subject.strip()):
            return self.subject

        return None

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the notification event (if applicable)."""
        message = ''

        if isinstance(self.message, str) and len(self.message.strip()):
            message += self.message + '\n\n'

        if isinstance(formatted_exception := self.exception_info_plain, str):
            message += f'{formatted_exception}\n'

        return message.rstrip()

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the notification event (if applicable)."""
        message = ''

        if isinstance(self.message, str) and len(self.message.strip()):
            message += f'<p>{self.message}</p>\n'

        if isinstance(formatted_exception := self.exception_info_html, str):
            message += f'{formatted_exception}\n'

        return message.rstrip()


class TaskEvent(TaskInfoMixin, NotificationEvent):
    """Defines a generic event used for task notifications."""

    label: Optional[str] = 'Task Event'
    """Defines the label of the task event (if applicable)."""

    task: Optional[Task] = None
    """Defines the task instance associated with the event (if applicable)."""

    context: Optional[Context] = None
    """Defines the context associated with the event (if applicable)."""

    request: Optional[Request] = None
    """Defines the task request associated with the event (if applicable)."""

    _task_id: Optional[str] = PrivateAttr(default=None)
    """Defines the task id associated with the event (if applicable)."""

    _task_name: Optional[str] = PrivateAttr(default=None)
    """Defines the task name associated with the event (if applicable)."""

    @property
    def task_id(self) -> Optional[str]:
        """Retrieves the task request id associated with the event."""

        if isinstance(self._task_id, str):
            return self._task_id

        if (isinstance(self.request, Request) and hasattr(self.request, 'id')
                and isinstance(self.request.id, str) and len(self.request.id.strip())):
            return self.request.id

        return None

    @task_id.setter
    def task_id(self, value: Optional[str]):
        """Sets the task request id associated with the event."""
        self._task_id = value

    @property
    def task_name(self) -> Optional[str]:
        """Retrieves the task name associated with the event."""

        if isinstance(self._task_name, str):
            return self._task_name

        if (isinstance(self.task, Task) and hasattr(self.task, 'name')
                and isinstance(self.task.name, str) and len(self.task.name.strip())):
            return self.task.name

        if (isinstance(self.request, Request) and hasattr(self.request, 'name')
                and isinstance(self.request.name, str) and len(self.request.name.strip())):
            return self.request.name

        return None

    @task_name.setter
    def task_name(self, value: Optional[str]):
        """Sets the task name associated with the event."""
        self._task_name = value

    @property
    def task_label(self) -> Optional[str]:
        """Defines the friendly label of the task associated with the event (if available)."""

        if (isinstance(self.task, Task) and hasattr(self.task, 'label') and isinstance(self.task.label, str)
                and len(self.task.label.strip())):
            return self.task.label

        if isinstance(task_name := self.task_name, str) and len(self.task_name.strip()):
            from worker import app as celery_app
            if (task_name in celery_app.tasks and hasattr(celery_app.tasks[task_name], 'label')
                    and isinstance(celery_app.tasks[task_name].label, str)
                    and len(celery_app.tasks[task_name].label.strip())):
                return celery_app.tasks[task_name].label

        return None

    @property
    def message_subject(self) -> Optional[str]:
        """Defines the message subject of the notification event (if applicable)."""

        if isinstance(task_label := self.task_label, str):
            return f'{task_label} {self.label}'

        return self.label

    @property
    def message_title(self) -> Optional[str]:
        """Defines the message title of the notification event (if applicable)."""
        return self.message_subject

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the notification event (if applicable)."""
        return self.task_info_plain

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the notification event (if applicable)."""
        return self.task_info_html


class TaskExceptionEvent(ExceptionEventMixin, TaskEvent):
    """Defines a generic event used for Celery signal notifications when some type of exception occurred."""

    label: Optional[str] = 'Task Exception'
    """Defines the label of the task event (if applicable)."""

    exception: Optional[Exception] = None
    """Defines the exception associated with the event (if applicable)."""

    einfo: Optional[ExceptionInfo] = None
    """Defines the exception info associated with the event (if applicable)."""

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_plain, str):
            message += f'{task_info}\n'

        if isinstance(exception_info := self.exception_info_plain, str):
            message += f'{exception_info}\n'

        return message.rstrip() or None

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_html, str):
            message += f'{task_info}\n'

        if isinstance(exception_info := self.exception_info_html, str):
            message += f'{exception_info}\n'

        return message.rstrip() or None


class TaskReceivedEvent(TaskEvent):
    """Defines an event used for Celery signal notifications when a task is received."""

    label: Optional[str] = 'Task Received'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_RECEIVED
    """Defines the notification category for the event."""


class TaskRevokedEvent(TaskEvent):
    """Defines an event used for Celery signal notifications when a task is revoked."""

    label: Optional[str] = 'Task Revoked'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_REVOKED
    """Defines the notification category for the event."""

    terminated: Optional[bool] = None
    """Defines if the task is terminated or not."""

    expired: Optional[bool] = None
    """Defines if the task is expired or not."""

    signum: Optional[int] = None
    """Defines the signal number for the event."""

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_plain, str):
            message += f'{task_info}\n'

        if isinstance(self.terminated, bool):
            message += f'Terminated: {self.terminated}\n'

        if isinstance(self.expired, bool):
            message += f'Expired: {self.expired}\n'

        if isinstance(self.signum, int):
            message += f'Signal Number: {self.signum}\n'

        return message.rstrip() or None

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_html, str):
            message += f'{task_info}\n'

        if isinstance(self.terminated, bool):
            message += f'<p style="margin-bottom: 10px;"><strong>Terminated:</strong> {self.terminated}</p>\n'

        if isinstance(self.expired, bool):
            message += f'<p style="margin-bottom: 10px;"><strong>Expired:</strong> {self.expired}</p>\n'

        if isinstance(self.signum, int):
            message += f'<p style="margin-bottom: 10px;"><strong>Signal Number:</strong> {self.signum}</p>\n'

        return message.rstrip() or None


class TaskRejectedEvent(TaskExceptionEvent):
    """Defines an event used for Celery signal notifications when a task is rejected."""

    label: Optional[str] = 'Task Rejected'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_REJECTED
    """Defines the notification category for the event."""

    message: Optional[str] = None
    """Defines the message for the event."""

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_plain, str):
            message += f'{task_info}\n'

        if isinstance(self.message, str):
            message += f'Message: {self.message}\n'

        if isinstance(exception_info := self.exception_info_plain, str):
            message += f'{exception_info}\n'

        return message.rstrip() or None

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_html, str):
            message += f'{task_info}\n'

        if isinstance(self.message, str):
            message += f'<p style="margin-bottom: 10px;"><strong>Message:</strong> {self.message}</p>\n'

        if isinstance(exception_info := self.exception_info_html, str):
            message += f'{exception_info}\n'

        return message.rstrip() or None


class TaskPreRunEvent(TaskEvent):
    """Defines an event used for Celery signal notifications before a task is started."""

    label: Optional[str] = 'Task Pre Run'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_PRE_RUN
    """Defines the notification category for the event."""


class TaskPostRunEvent(TaskEvent):
    """Defines an event used for Celery signal notifications after a task is finished."""

    label: Optional[str] = 'Task Post Run'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_POST_RUN
    """Defines the notification category for the event."""


class TaskSuccessEvent(TaskEvent):
    """Defines an event used for Celery signal notifications when a task is completed."""

    label: Optional[str] = 'Task Succeeded'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_SUCCESS
    """Defines the notification category for the event."""

    result: Optional[Any] = None
    """Defines the result of the task."""

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_plain, str):
            message += f'{task_info}\n'

        if self.result is not None:
            try:
                message += f'Result: {self.result}\n'
            except Exception:
                pass

        return message.rstrip() or None

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_html, str):
            message += f'{task_info}\n'

        if self.result is not None:
            try:
                message += f'<p style="margin-bottom: 10px;"><strong>Result:</strong> {self.result}</p>\n'
            except Exception:
                pass

        return message.rstrip() or None


class TaskRetryEvent(TaskExceptionEvent):
    """Defines an event used for Celery signal notifications when a task is retried."""

    label: Optional[str] = 'Task Retrying'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_RETRY
    """Defines the notification category for the event."""

    reason: Optional[str] = None
    """Defines the reason associated with the event (if applicable)."""

    @property
    def message_body_plain(self) -> Optional[str]:
        """Defines the message body in plain format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_plain, str):
            message += f'{task_info}\n'

        if isinstance(self.reason, str):
            message += f'Reason: {self.reason}\n'

        if isinstance(exception_info := self.exception_info_plain, str):
            message += f'{exception_info}\n'

        return message.rstrip() or None

    @property
    def message_body_html(self) -> Optional[str]:
        """Defines the message body in HTML format of the notification event (if applicable)."""
        message = ''

        if isinstance(task_info := super().message_body_html, str):
            message += f'{task_info}\n'

        if isinstance(self.reason, str):
            message += f'<p style="margin-bottom: 10px;"><strong>Reason:</strong> {self.reason}</p>\n'

        if isinstance(exception_info := self.exception_info_html, str):
            message += f'{exception_info}\n'

        return message.rstrip() or None


class TaskFailedEvent(TaskExceptionEvent):
    """Defines an event used for Celery signal notifications when a task has failed."""

    label: Optional[str] = 'Task Failed'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_FAILED
    """Defines the notification category for the event."""


class TaskInternalErrorEvent(TaskExceptionEvent):
    """Defines an event used for Celery signal notifications when a task encounters an internal error."""

    label: Optional[str] = 'Task Internal Error'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_INTERNAL_ERROR
    """Defines the notification category for the event."""


class TaskUnknownEvent(TaskExceptionEvent):
    """Defines an event used for Celery signal notifications when an unknown task exception occurred."""

    label: Optional[str] = 'Task Unknown'
    """Defines the label of the task event (if applicable)."""

    category: Optional[NotificationCategoryEnum] = NotificationCategoryEnum.TASK_UNKNOWN
    """Defines the notification category for the event."""

    message: Optional[Message] = None
    """Defines the message for the event."""


ALL_EVENTS = Union[
    NotificationEvent, AlertEvent, TaskEvent, TaskExceptionEvent, TaskReceivedEvent, TaskRevokedEvent,
    TaskRejectedEvent, TaskPreRunEvent, TaskPostRunEvent, TaskSuccessEvent, TaskRetryEvent, TaskFailedEvent,
    TaskInternalErrorEvent, TaskUnknownEvent
]

ALL_EVENTS_TYPE = type[ALL_EVENTS]
