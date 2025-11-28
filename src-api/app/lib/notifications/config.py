import re
from datetime import date, datetime, time
from pydantic import field_validator, model_validator
from typing import Optional, Union, Any
from zoneinfo import ZoneInfo
from app.lib.enums import (
    TaskEnum, DayOfWeekEnum,
    NotificationCategoryEnum, TwilioNotificationTypeEnum, NotificationServiceEnum
)
from app.lib.notifications.events import ALL_EVENTS
from app.models.base import BaseModel

UTC_TZ = ZoneInfo('UTC')


class NotificationCriteria(BaseModel):
    """Represents notification criteria configuration associated with a notification configuration."""

    category: Optional[Union[set[NotificationCategoryEnum], NotificationCategoryEnum]] = None
    """A notification category string or list of strings that the notification configuration should be used for."""

    task: Optional[Union[set[TaskEnum], TaskEnum]] = None
    """A task name string or list of strings that the notification configuration should be used for."""

    meta: Optional[dict[str, Any]] = None
    """A dictionary of key/value pairs that should be used to as additional matching criteria to determine a
    notification configuration's relevant to a particular event."""

    def applicable(self, event: ALL_EVENTS) -> bool:
        """Determines if this object is applicable for use based on the given criteria."""

        if isinstance(self.category, NotificationCategoryEnum) and event.category != self.category:
            return False

        if isinstance(self.category, set) and self.category:
            if event.category is None:
                return False
            if event.category not in self.category:
                return False

        if isinstance(self.task, TaskEnum) and event.task_name != self.task:
            return False

        if isinstance(self.task, set) and self.task:
            if event.task_name is None:
                return False
            if TaskEnum(event.task_name) not in self.task:
                return False

        # TODO: Check meta

        return True


class RecipientScheduleDates(BaseModel):
    """Represents a date/time restriction criteria of a recipient schedule configuration."""

    start: Optional[Union[date, datetime]] = None
    """The earliest date/time the recipient schedule should be restricted to."""

    end: Optional[Union[date, datetime]] = None
    """The latest date/time the recipient schedule should be restricted to."""

    def applicable(self, timestamp: Optional[datetime] = None) -> bool:
        """Determines if this object is applicable for use based on the given timestamp."""

        # Default timestamp to now with a UTC timezone if none provided
        if not isinstance(timestamp, datetime):
            timestamp = datetime.now(tz=UTC_TZ)

        # Check the start datetime
        if isinstance(self.start, datetime):
            if timestamp < self.start:
                return False

        # Check the start date
        elif isinstance(self.start, date):
            if timestamp.date() < self.start:
                return False

        # Check the end datetime
        if isinstance(self.end, datetime):
            if timestamp > self.end:
                return False

        # Check the end date
        elif isinstance(self.end, date):
            if timestamp.date() > self.end:
                return False

        return True

    @field_validator('start', 'end', mode='before')
    @classmethod
    def parse_custom_datetime(cls, v: str) -> Union[date, datetime, str, None]:
        if not v:
            return v

        # Regex to check if the input matches the date-only format
        date_only_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

        if date_only_pattern.match(v):
            # If it's just a date, parse it as a date object
            return datetime.strptime(v, '%Y-%m-%d').date()
        else:
            # If it includes time, attempt to parse the custom datetime format
            # We must handle optional minutes/seconds via multiple attempts as strptime is strict
            try:
                # Try parsing the full format: YYYY-MM-DD H:MM:SS am/pm (e.g., 2023-11-15 3:05:00 pm)
                return datetime.strptime(v, '%Y-%m-%d %I:%M:%S %p')
            except ValueError:
                try:
                    # Try parsing without seconds: YYYY-MM-DD H:MM am/pm (e.g., 2023-11-15 3:05 pm)
                    return datetime.strptime(v, '%Y-%m-%d %I:%M %p')
                except ValueError:
                    try:
                        # Try parsing without minutes/seconds: YYYY-MM-DD H am/pm (e.g., 2023-11-15 3 pm)
                        return datetime.strptime(v, '%Y-%m-%d %I %p')
                    except ValueError:
                        # If all attempts fail, return the original string. Pydantic's core validation
                        # for `Union[date, datetime]` will raise the appropriate ValidationError.
                        return v


class RecipientScheduleTimes(BaseModel):
    """Represents a day/time restriction criteria of a recipient schedule configuration."""

    days: Optional[list[DayOfWeekEnum]] = None
    """The day(s) of the week that the recipient schedule should be restricted to."""

    start: Optional[time] = None
    """The earliest time of a day that the recipient schedule should be restricted to."""

    end: Optional[time] = None
    """The latest time of a day that the recipient schedule should be restricted to."""

    def applicable(self, timestamp: Optional[datetime] = None) -> bool:
        """Determines if this object is applicable for use based on the given timestamp."""

        # Default timestamp to now with a UTC timezone if none provided
        if not isinstance(timestamp, datetime):
            timestamp = datetime.now(tz=UTC_TZ)

        # Check the days
        if isinstance(self.days, list) and self.days:
            check = False
            ts_day = timestamp.strftime('%A').lower()

            for day in self.days:
                if day.value.lower() == ts_day:
                    check = True
                    break

            if not check:
                return False

        # Check the start time
        if isinstance(self.start, time) and timestamp.time() < self.start:
            return False

        # Check the end time
        if isinstance(self.end, time) and timestamp.time() > self.end:
            return False

        return True

    @field_validator('start', 'end', mode='before')
    @classmethod
    def parse_custom_time(cls, v: str) -> Union[time, str, None]:
        if not v:
            return v

        # We must handle optional minutes/seconds for custom am/pm format via multiple attempts
        try:
            # Try parsing the full format: H:MM:SS am/pm (e.g., 3:05:00 pm)
            dt_object = datetime.strptime(v, '%I:%M:%S %p')
            return dt_object.time()
        except ValueError:
            try:
                # Try parsing without seconds: H:MM am/pm (e.g., 3:05 pm)
                dt_object = datetime.strptime(v, '%I:%M %p')
                return dt_object.time()
            except ValueError:
                try:
                    # Try parsing without minutes/seconds: H am/pm (e.g., 3 pm)
                    dt_object = datetime.strptime(v, '%I %p')
                    return dt_object.time()
                except ValueError:
                    # If all attempts fail, return the original string. Pydantic's core validation
                    # for `time` will then raise the appropriate ValidationError.
                    return v


class RecipientSchedule(BaseModel):
    """Represents a recipient schedule configuration used to determine when notifications should be sent to a
    recipient."""

    enabled: bool = True
    """Whether the recipient schedule should be enabled or disabled."""

    label: str
    """A friendly label for the recipient schedule used in logging."""

    timezone: str = 'Etc/UTC'
    """An IANA timezone used to determine how the recipient schedule dates and times should be interpreted."""

    dates: Optional[list[RecipientScheduleDates]] = None
    """Defines the start and/or end dates and optionally times that the recipient schedule should be restricted to."""

    times: Optional[list[RecipientScheduleTimes]] = None
    """Defines the weekdays and/or start and/or end times that the recipient schedule should be restricted to
    while respecting the dates and optionally time ranges defined by the 'dates' attribute if set."""

    def applicable(self, timestamp: Optional[datetime] = None) -> bool:
        """Determines if this recipient is applicable for use based on the given timestamp."""

        # Default timestamp to now with a UTC timezone if none provided
        if not isinstance(timestamp, datetime):
            timestamp = datetime.now(tz=ZoneInfo(self.timezone))
        elif str(timestamp.tzinfo.tzname).lower() != self.timezone.lower():
            timestamp = timestamp.astimezone(ZoneInfo(self.timezone))

        # If no schedule dates or times are defined then assume applicable
        if ((not isinstance(self.dates, list) or not self.dates)
                and (not isinstance(self.times, list) or not self.times)):
            return True

        # Check that defined dates/times (if any) meet the criteria
        if isinstance(self.dates, list) and self.dates:
            check = False

            for d in self.dates:
                if d.applicable(timestamp=timestamp):
                    check = True
                    break

            if not check:
                return False

        # Check that defined days/times (if any) meets the criteria
        if isinstance(self.times, list) and self.times:
            check = False

            for t in self.times:
                if t.applicable(timestamp=timestamp):
                    check = True
                    break

            if not check:
                return False

        return True

    @model_validator(mode='after')
    def set_timezone_for_dates_and_times(self) -> 'RecipientSchedule':
        """
        After instantiation, apply the 'timezone' attribute to the relevant fields of the dates and times objects.
        """
        from zoneinfo import ZoneInfo

        if self.dates is None and self.times is None:
            return self

        tz = ZoneInfo(self.timezone)

        # Helper function to apply the timezone to a datetime object
        def localize_datetime(dt_value: Optional[Union[date, datetime, time]]):
            if (isinstance(dt_value, datetime) or isinstance(dt_value, time)) and dt_value.tzinfo is None:
                # If it's a naive datetime, localize it to the schedule's timezone
                return dt_value.replace(tzinfo=tz)
            elif (isinstance(dt_value, datetime) or isinstance(dt_value, time)) and dt_value.tzinfo is not None:
                # If it's already timezone-aware, convert it to the schedule's timezone
                return dt_value.astimezone(tz)
            # Dates (not datetime / time) and already localized datetime / time values are returned as is
            return dt_value

        # Apply the helper function to the dates list object's start and end date / datetime objects
        if isinstance(self.dates, list) and len(self.dates):
            for schedule_date in self.dates:
                if isinstance(schedule_date.start, datetime):
                    schedule_date.start = localize_datetime(schedule_date.start)
                if isinstance(schedule_date.end, datetime):
                    schedule_date.end = localize_datetime(schedule_date.end)

        # Apply the helper function to the times list object's start and end time objects
        if isinstance(self.times, list) and len(self.times):
            for schedule_time in self.times:
                if isinstance(schedule_time.start, time):
                    schedule_time.start = localize_datetime(schedule_time.start)
                if isinstance(schedule_time.end, time):
                    schedule_time.end = localize_datetime(schedule_time.end)

        return self


class ServiceRecipient(BaseModel):
    """Represents a recipient configuration associated with a notification service configuration."""

    enabled: bool = True
    """Whether the recipient should be enabled or disabled."""

    label: str
    """A friendly label for the recipient configuration used in logging."""

    schedules: Optional[list[RecipientSchedule]] = None
    """Defines schedules to be used to determine when notifications should be sent to a recipient."""

    def applicable(self, timestamp: Optional[datetime] = None) -> bool:
        """Determines if this recipient is applicable for use based on the given timestamp."""

        # Check that the recipient is enabled
        if not self.enabled:
            return False

        # Default timestamp to now with a UTC timezone if none provided
        if not isinstance(timestamp, datetime):
            timestamp = datetime.now(tz=UTC_TZ)

        # If no schedules are defined then assume applicable
        if not isinstance(self.schedules, list) or not self.schedules or all(not s.enabled for s in self.schedules):
            return True

        # Check that at least one recipient schedule applies to the timestamp
        for schedule in self.schedules:
            if not schedule.enabled:
                continue

            if schedule.applicable(timestamp=timestamp):
                return True

        return False


class MailServiceRecipient(ServiceRecipient):
    """Represents a recipient configuration associated with the mail notification service."""

    name: Optional[str] = None
    """Name used to identify the recipient."""

    email: str
    """Email address of the recipient."""


class MsTeamsServiceRecipient(ServiceRecipient):
    """Represents a recipient configuration associated with the Microsoft Teams notification service."""

    webhook: str
    """A webhook URL to receive Microsoft Teams channel messages."""


class TwilioServiceRecipient(ServiceRecipient):
    """Represents a recipient configuration associated with the Twilio notification service."""

    name: Optional[str] = None
    """Name used to identify the recipient."""

    number: str
    """Phone number of the recipient in E164 format."""

    types: list[TwilioNotificationTypeEnum]
    """A list of notification types to be used for the recipient."""


ALL_SERVICE_RECIPIENTS = [ServiceRecipient, MailServiceRecipient, MsTeamsServiceRecipient, TwilioServiceRecipient]
ALL_SERVICE_RECIPIENTS_TYPE = type[ALL_SERVICE_RECIPIENTS]


class NotificationService(BaseModel):
    """Represents notification service configuration associated with a notification configuration."""

    enabled: bool = True
    """Whether the service should be enabled or disabled."""

    label: str
    """A friendly label for the service configuration used in logging."""

    name: NotificationServiceEnum
    """A name used to identify the service."""

    recipients: list[ServiceRecipient]
    """Defines recipients to be used for delivering notifications for a particular service."""

    def applicable(self, timestamp: Optional[datetime] = None) -> bool:
        """Determines if this service is applicable for use based on the given timestamp."""

        # Check that the service is enabled
        if not self.enabled:
            return False

        # Default timestamp to now with a UTC timezone if none provided
        if not isinstance(timestamp, datetime):
            timestamp = datetime.now(tz=UTC_TZ)

        # Check that at least one recipient applies to the timestamp
        for recipient in self.recipients:
            if not recipient.enabled:
                continue

            if recipient.applicable(timestamp=timestamp):
                return True

        return False


class MailNotificationService(NotificationService):
    """Represents a notification service configuration for the mail notification service."""

    label: str = 'Mail Notification Service'
    """A friendly label for the service configuration used in logging."""

    name: NotificationServiceEnum = NotificationServiceEnum.MAIL
    """A name used to identify the service."""

    recipients: list[MailServiceRecipient]
    """Defines recipients to be used for delivering notifications for a particular service."""


class MsTeamsNotificationService(NotificationService):
    """Represents a notification service configuration for the mail notification service."""

    label: str = 'Microsoft Teams Notification Service'
    """A friendly label for the service configuration used in logging."""

    name: NotificationServiceEnum = NotificationServiceEnum.MSTEAMS
    """A name used to identify the service."""

    recipients: list[MsTeamsServiceRecipient]
    """Defines recipients to be used for delivering notifications for a particular service."""


class TwilioNotificationService(NotificationService):
    """Represents a notification service configuration for the mail notification service."""

    label: str = 'Twilio Notification Service'
    """A friendly label for the service configuration used in logging."""

    name: NotificationServiceEnum = NotificationServiceEnum.TWILIO
    """A name used to identify the service."""

    recipients: list[TwilioServiceRecipient]
    """Defines recipients to be used for delivering notifications for a particular service."""


ALL_NOTIFICATION_SERVICES = [
    NotificationService, MailNotificationService, MsTeamsNotificationService, TwilioNotificationService
]
ALL_NOTIFICATION_SERVICES_TYPE = type[ALL_NOTIFICATION_SERVICES]


class NotificationConfig(BaseModel):
    """Represents a notification configuration document."""

    enabled: bool = True
    """Whether the notification configuration should be enabled or disabled."""

    label: str
    """A friendly label for the notification configuration used in logging."""

    criteria: NotificationCriteria = None
    """Defines criteria used to determine if a notification configuration is relevant to a particular event."""

    services: list[Union[MailNotificationService, MsTeamsNotificationService, TwilioNotificationService]]
    """Defines services to be used for delivering notifications related to a particular event."""

    def applicable(self, event: ALL_EVENTS, timestamp: Optional[datetime] = None) -> bool:
        """Determines if this configuration is applicable for use based on the given timestamp."""

        # Check that the configuration is enabled
        if not self.enabled:
            return False

        # Default timestamp to now with a UTC timezone if none provided
        if not isinstance(timestamp, datetime):
            timestamp = datetime.now(tz=UTC_TZ)

        # Check the notification criteria if any
        if isinstance(self.criteria, NotificationCriteria) and not self.criteria.applicable(event=event):
            return False

        # Check that at least one service schedule applies to the timestamp
        for service in self.services:
            if not service.enabled:
                continue

            if service.applicable(timestamp=timestamp):
                return True

        return False
