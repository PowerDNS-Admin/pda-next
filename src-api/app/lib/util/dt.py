import re
from celery.schedules import crontab
from typing import Union

TIME_STRING_REGEX = re.compile(
    r'(?:(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{1,2}))(?:\s(?P<meridiem>AM|PM))?(?:\s(?P<tz>[A-Z/]{3,}))?',
    re.IGNORECASE,
)

CRONTAB_STRING_REGEX = re.compile(
    r'^(?P<minute>[\d*/,-]+)\s+(?P<hour>[\d*/,-]+)\s+(?P<dom>[\d*/,-]+)\s+(?P<moy>[\d*/,-]+)\s+(?P<dow>[\d*/,-]+)(?:\s(?P<tz>[A-Z/]{3,}))?$',
    re.IGNORECASE,
)

CRONTAB_INTERVAL_REGEX = re.compile(r'^\*\/(?P<hour>[0-9]{1,2})$')

CRONTAB_RANGE_REGEX = re.compile(r'^(?P<start>[0-9]{1,2})\-(?P<end>[0-9]{1,2})$')


class TimeUtil:

    @staticmethod
    def convert_times_to_crontab(times: Union[list[str], str]) -> list[crontab]:
        """Converts a list of times to their Celery crontab representation."""
        from datetime import datetime, timedelta
        from zoneinfo import ZoneInfo

        result = []

        # If not time selectors are present, default to 1 minute in the future
        if not times:
            return result

        # Convert single time strings into a list of strings
        if isinstance(times, str):
            times = [times]

        for time in times:
            hour = 0
            minute = 0
            day_of_month = '*'
            month_of_year = '*'
            day_of_week = '*'
            tz = 'UTC'

            now = datetime.now()

            if match := CRONTAB_STRING_REGEX.match(time):
                mg = match.groupdict()

                if 'tz' in mg and mg['tz'] is not None:
                    tz = mg['tz']

                if 'hour' in mg:
                    hour = mg['hour']

                    if tz != 'UTC':
                        interval = False

                        if match := CRONTAB_INTERVAL_REGEX.match(hour):
                            interval = True
                            hmg = match.groupdict()
                            hours = [hmg['hour']]
                            pass
                        elif match := CRONTAB_RANGE_REGEX.match(hour):
                            hmg = match.groupdict()
                            hours = [hmg['start'], hmg['end']]
                            pass
                        elif ',' in hour:
                            hours = hour.split(',')
                        else:
                            hours = [hour]

                        for i in range(len(hours)):
                            if hours[i] == '*':
                                continue
                            schedule_dt = (datetime.now().astimezone(ZoneInfo(tz)).replace(hour=int(hours[i]), minute=0)
                                           .astimezone(ZoneInfo('UTC')))

                            hours[i] = schedule_dt.hour

                        if len(hours) == 1 and interval:
                            hour = f'*/{hours[0]}'
                        elif len(hours) == 1:
                            hour = f'{hours[0]}'
                        elif len(hours) == 2:
                            hour = f'{hours[0]}-{hours[1]}'
                        elif len(hours) > 2:
                            hour = ','.join(hours)

                if 'minute' in mg:
                    minute = mg['minute']

                if 'dom' in mg:
                    day_of_month = mg['dom']

                if 'moy' in mg:
                    month_of_year = mg['moy']

                if 'dow' in mg:
                    day_of_week = mg['dow']

            elif match := TIME_STRING_REGEX.match(time):
                mg = match.groupdict()

                if 'hour' in mg:
                    hour = int(mg['hour'])

                if 'minute' in mg:
                    minute = int(mg['minute'])

                if 'meridiem' in mg and mg['meridiem'] is not None:
                    if mg['meridiem'].upper() == 'PM' and hour != 12:
                        hour += 12
                    elif mg['meridiem'].upper() == 'AM' and hour == 12:
                        hour = 0

                if 'tz' in mg and mg['tz'] is not None:
                    tz = mg['tz']

                # Create a date/time object representing the schedule time, localized if not UTC
                schedule_dt = (datetime(now.year, now.month, now.day, int(hour), int(minute))
                               .replace(tzinfo=ZoneInfo(tz)))

                # Convert the schedule time to UTC if not already
                if tz != 'UTC':
                    schedule_dt = schedule_dt.astimezone(ZoneInfo('UTC'))

                hour = schedule_dt.hour
                minute = schedule_dt.minute

            else:
                continue

            result.append(crontab(
                hour=str(hour), minute=str(minute),
                day_of_month=day_of_month, month_of_year=month_of_year, day_of_week=day_of_week
            ))

        return result

    @staticmethod
    def extract_time_components(time: str) -> tuple[int, int, int]:
        # Return a time of 00:00:00 when an invalid input string is given
        if not time or not isinstance(time, str) or ':' not in time:
            return 0, 0, 0

        parts = time.split(':')
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        second = int(parts[2]) if len(parts) > 2 else 0

        return hour, minute, second


class DateUtil:

    @staticmethod
    def add_one_month(dt):
        # Calculate the next month and year
        month = dt.month
        year = dt.year
        day = dt.day

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        # Handle day overflow (e.g. 31st → adjust)
        # Find the last valid day in the target month
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        day = min(day, last_day)

        return dt.replace(year=year, month=month, day=day)
