import heapq
from billiard.einfo import ExceptionInfo
from celery import Celery
from celery.app.task import Context, Task
from celery.beat import Scheduler
from celery.worker.request import Request
from collections import namedtuple
from kombu.transport.virtual.base import Message
from typing import Any, Optional, Union
from models.db.tasks import TaskJob

event_t = namedtuple('event_t', ('time', 'priority', 'entry'))


class DynamicScheduler(Scheduler):
    """Provides a custom scheduler for Celery Beat that loads the latest schedule configuration periodically."""

    sync_every = 300

    max_interval = 30

    _last_sync = 0

    _store = None

    _startup_tasks_executed = False

    def setup_schedule(self):
        self._store = {'entries': {}}
        self.merge_inplace(self.app.conf.beat_schedule)
        self.install_default_entries(self.schedule)

    def tick(self, event_t=event_t, min=min, heappop=heapq.heappop,
             heappush=heapq.heappush):
        import time
        from loguru import logger

        now = time.time()

        diff = abs(now - self._last_sync)

        stale = diff > self.sync_every or 'entries' not in self._store

        if stale:
            logger.trace('Schedule data stale, reloading...')
            self.schedule.clear()
            self.update_from_dict(self.build_beat_schedule())
            self._last_sync = now

        return super().tick()

    def build_beat_schedule(self) -> dict:
        from celery import current_app
        from loguru import logger
        from lib import load_config, load_schedules
        from lib.util.dt import TimeUtil

        config = load_config()
        schedule_data = load_schedules()

        self.sync_every = config.tasks.scheduler.max_schedule_lifetime
        self.max_interval = config.tasks.scheduler.tick_interval

        schedules = {}

        if not config.tasks.enabled or not schedule_data:
            return schedules

        for schedule in schedule_data:
            # Validate schedule configuration
            if not schedule.name or not schedule.task:
                logger.error(f'Skipping invalid schedule configuration: {schedule}')
                continue

            # Check that the schedule is enabled
            if not schedule.enabled:
                logger.trace(f'Skipping disabled schedule configuration: {schedule.name}')
                continue

            # Parse scheduling information
            at = TimeUtil.convert_times_to_crontab(schedule.at)

            if not at and not self._startup_tasks_executed:
                logger.trace(f'Scheduling task for immediate execution: {schedule.name}')
                current_app.send_task(schedule.task, args=schedule.args, kwargs=schedule.kwargs)
                continue

            # Build the Celery Beat schedule configuration
            index = 1
            for time in at:
                logger.trace(f'Creating Schedule: {schedule.name} @ {time}')

                bs = {
                    'task': schedule.task,
                    'schedule': time,
                }

                if schedule.args:
                    args = schedule.args
                    if isinstance(args, str):
                        args = [args]
                    bs['args'] = args

                if schedule.kwargs and isinstance(schedule.kwargs, dict):
                    bs['kwargs'] = schedule.kwargs

                if schedule.options and isinstance(schedule.options, dict):
                    bs['options'] = schedule.options

                schedules[f'{schedule.key}{index}'] = bs

                index += 1

        self._startup_tasks_executed = True

        return schedules


class SignalHandler:
    app: Optional[Celery]
    """The Celery app instance reference."""

    _stdout = None

    _stderr = None

    _stdout_original = None

    _stderr_original = None

    _ignored_tasks: list[str] = [
        'pda.mail',
        'pda.mail.send',
    ]

    class TeeStream:
        def __init__(self, *streams):
            self.streams = streams

        def write(self, data):
            for s in self.streams:
                s.write(data)
                s.flush()

        def flush(self):
            for s in self.streams:
                s.flush()

    def __init__(self, app: Optional[Celery] = None):
        from celery.signals import (
            task_received, task_revoked, task_rejected, task_prerun, task_postrun, task_retry, task_internal_error,
            task_success, task_failure, task_unknown, worker_process_init, worker_process_shutdown
        )

        self.app = app
        self._stdout = None
        self._stderr = None
        self._stdout_original = None
        self._stderr_original = None

        # Connect Celery Signals
        worker_process_init.connect(self.worker_process_init_handler, weak=False)
        worker_process_shutdown.connect(self.worker_process_shutdown_handler, weak=False)
        #task_received.connect(self.task_received_handler, weak=False)
        task_revoked.connect(self.task_revoked_handler, weak=False)
        task_rejected.connect(self.task_rejected_handler, weak=False)
        task_prerun.connect(self.task_pre_run_handler, weak=False)
        task_postrun.connect(self.task_post_run_handler, weak=False)
        task_retry.connect(self.task_retry_handler, weak=False)
        task_internal_error.connect(self.task_internal_error_handler, weak=False)
        task_success.connect(self.task_success_handler, weak=False)
        task_failure.connect(self.task_failure_handler, weak=False)
        task_unknown.connect(self.task_unknown_handler, weak=False)

    def start_capture(self) -> Any:
        import io, sys
        self._stderr = io.StringIO()
        self._stderr_original = sys.stderr
        sys.stderr = self.TeeStream(self._stderr_original, self._stderr)
        return self._stderr

    def stop_capture(self) -> Any:
        import sys
        sys.stderr = self._stderr_original
        return self._stderr

    def get_task_job(self, task_id: str, request: Union[Request, Context] = None) -> TaskJob:
        import json
        from uuid import UUID
        from sqlalchemy import select
        from sqlalchemy.exc import InvalidRequestError
        from sqlalchemy.orm.exc import UnmappedInstanceError
        from app import SessionLocal
        from models.enums import TaskJobStatusEnum

        stmt = select(TaskJob).where(TaskJob.id == UUID(task_id))

        with SessionLocal() as session:
            result = session.execute(stmt).fetchall()

            if result:
                tj = result[0][0]
            else:
                tj = TaskJob()

                if hasattr(request, 'id') and request.id:
                    tj.id = UUID(request.id)

                if request.root_id:
                    tj.root_id = UUID(request.root_id)

                if request.parent_id:
                    tj.parent_id = UUID(request.parent_id)

                if hasattr(request, 'name') and request.name:
                    tj.name = request.name
                elif hasattr(request, 'task') and request.task:
                    tj.name = request.task

                if hasattr(request, 'args') and isinstance(request.kwargs, list) and request.args:
                    tj.args = json.dumps(request.args)

                if hasattr(request, 'kwargs') and isinstance(request.kwargs, dict) and request.kwargs:
                    tj.kwargs = json.dumps(request.kwargs)

                tj.status = TaskJobStatusEnum.received

            try:
                session.expunge(tj)
            except (InvalidRequestError, UnmappedInstanceError):
                pass

        return tj

    def save_task_job(self, task_job: TaskJob, create_activity: bool = True):
        import json
        from datetime import datetime
        from sqlalchemy.exc import InvalidRequestError
        from sqlalchemy.orm.exc import UnmappedInstanceError
        from app import SessionLocal
        from models.db.tasks import TaskJobActivity
        from models.enums import TaskJobStatusEnum

        with SessionLocal() as session:
            session.add(task_job)

            if task_job.status == TaskJobStatusEnum.running and task_job.started_at is None:
                task_job.started_at = datetime.now()

            elif (task_job.status in [TaskJobStatusEnum.success, TaskJobStatusEnum.failed, TaskJobStatusEnum.internal_error]
                  and task_job.started_at is not None):
                task_job.ended_at = datetime.now()
                task_job.runtime = abs((task_job.ended_at - task_job.started_at).total_seconds())

            elif task_job.status == TaskJobStatusEnum.revoked and task_job.started_at is not None:
                task_job.ended_at = datetime.now()
                task_job.runtime = abs((task_job.ended_at - task_job.started_at).total_seconds())

            if create_activity:
                tja = TaskJobActivity()
                tja.task_job_id = task_job.id
                tja.status = task_job.status

                try:
                    if task_job.status in [TaskJobStatusEnum.retry, TaskJobStatusEnum.failed]:
                        tja.error = json.loads(task_job.errors)[-1]
                except Exception:
                    pass

                session.add(tja)

            session.commit()
            session.refresh(task_job)

            try:
                session.expunge(task_job)
            except (InvalidRequestError, UnmappedInstanceError):
                pass

    def worker_process_init_handler(self, **kwargs):
        """Initialize global dependencies for each Celery worker process."""
        from app import app_startup
        app_startup(use_sync=True)

    def worker_process_shutdown_handler(self, **kwargs):
        """Clean up global dependencies for each Celery worker process."""
        from app import app_shutdown
        app_shutdown(use_sync=True)

    def task_received_handler(self, request: Request, **kwargs):
        from loguru import logger
        from app import notifications
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskReceivedEvent
        from models.enums import TaskJobStatusEnum

        logger.debug(f'Task Received: Request: {request}')

        if tj := self.get_task_job(request.id, request):
            tj.status = TaskJobStatusEnum.received
            self.save_task_job(tj)

        event = TaskReceivedEvent(
            request=request,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_revoked_handler(self, request: Context, terminated: bool, signum: int, expired: bool, **kwargs):
        from loguru import logger
        from app import notifications, zabbix
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskRevokedEvent
        from lib.services.zabbix import ZabbixMetric
        from models.enums import TaskJobStatusEnum

        logger.debug(
            f'Task Revoked: Request: {request}; Terminated: {terminated}; SigNum: {signum}; Expired: {expired}')

        if tj := self.get_task_job(request.id, request):
            tj.status = TaskJobStatusEnum.revoked
            self.save_task_job(tj)

        zabbix.report([ZabbixMetric(f'task.{tj.name}.status', -2)])

        event = TaskRevokedEvent(
            context=request,
            terminated=terminated,
            expired=expired,
            signum=signum,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_rejected_handler(self, message: str, exc: Exception, **kwargs):
        from loguru import logger
        from app import notifications
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskRejectedEvent

        logger.debug(f'Task Rejected: {message}; Exception: {exc}')

        event = TaskRejectedEvent(
            message=message,
            exception=exc,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_pre_run_handler(self, task_id: str, task: Task, **kwargs):
        from loguru import logger
        from app import notifications, zabbix
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskPreRunEvent
        from lib.services.zabbix import ZabbixMetric
        from models.enums import TaskJobStatusEnum

        self.start_capture()

        logger.debug(f'Task Pre-Run: Task ID: {task_id}; Task Name: {task.name}')

        if tj := self.get_task_job(task_id, task.request):
            tj.status = TaskJobStatusEnum.running
            self.save_task_job(tj)

        zabbix.report([ZabbixMetric(f'task.{tj.name}.status', 2)])

        event = TaskPreRunEvent(
            task=task,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_post_run_handler(self, task_id: str, task: Task, **kwargs):
        import json
        from loguru import logger
        from app import notifications
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskPostRunEvent

        logger.debug(f'Task Post-Run: Task ID: {task_id}; Task Name: {task.name}')

        stderr = self.stop_capture()

        if tj := self.get_task_job(task_id, task.request):

            output = None

            if tj.output:
                try:
                    output = json.loads(tj.output)
                except json.decoder.JSONDecodeError:
                    pass

            if not isinstance(output, list):
                output = []

            output.append(stderr.getvalue())
            tj.output = json.dumps(output)

            self.save_task_job(tj, False)

        event = TaskPostRunEvent(
            task=task,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_retry_handler(self, request: Context, reason: str, einfo: ExceptionInfo, **kwargs):
        import json
        from loguru import logger
        from app import notifications, zabbix
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskRetryEvent
        from lib.services.zabbix import ZabbixMetric
        from models.enums import TaskJobStatusEnum

        logger.debug(f'Task Retry: Context: {request}; Reason: {reason};\n\nTraceback:\n\n{einfo.traceback}')

        if tj := self.get_task_job(request.id, request):
            tj.status = TaskJobStatusEnum.retry
            tj.retries = request.retries

            errors = None
            if tj.output:
                try:
                    errors = json.loads(tj.errors)
                except json.decoder.JSONDecodeError:
                    pass
            if not isinstance(errors, list):
                errors = []
            errors.append(str(einfo))
            if errors:
                tj.errors = json.dumps(errors)

            self.save_task_job(tj)

        zabbix.report([ZabbixMetric(f'task.{tj.name}.status', 3)])

        event = TaskRetryEvent(
            context=request,
            reason=reason,
            einfo=einfo,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_internal_error_handler(self, task_id: str, args, kwargs, request: Request, exception, traceback, einfo: ExceptionInfo, **kw):
        from loguru import logger
        from app import notifications, zabbix
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskInternalErrorEvent
        from lib.services.zabbix import ZabbixMetric
        from models.enums import TaskJobStatusEnum

        logger.debug(f'Task Internal Error: Task ID: {task_id}; Request: {request};\n\nTraceback:\n\n{einfo.traceback}')

        if tj := self.get_task_job(task_id, request):
            tj.status = TaskJobStatusEnum.internal_error
            self.save_task_job(tj)

        zabbix.report([ZabbixMetric(f'task.{tj.name}.status', -1)])

        event = TaskInternalErrorEvent(
            request=request,
            exception=exception,
            einfo=einfo,
        )
        event.task_id = task_id

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_success_handler(self, sender, result: Any, **kwargs):
        from loguru import logger
        from app import notifications, zabbix
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskSuccessEvent
        from lib.services.zabbix import ZabbixMetric
        from models.enums import TaskJobStatusEnum

        logger.debug(f'Task Success: {sender.name}; Result: {result}')

        if tj := self.get_task_job(sender.request.id, sender.request):
            tj.status = TaskJobStatusEnum.success
            tj.retries = sender.request.retries
            self.save_task_job(tj)

        zabbix.report([ZabbixMetric(f'task.{tj.name}.status', 4)])

        event = TaskSuccessEvent(
            task=sender,
            result=result,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)

    def task_failure_handler(self, sender, task_id: str, exception: Exception, args, kwargs, traceback, einfo: ExceptionInfo, **kw):
        import json
        from loguru import logger
        from app import notifications, zabbix
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskFailedEvent
        from lib.services.zabbix import ZabbixMetric
        from models.enums import TaskJobStatusEnum

        logger.debug(f'Task Failure: {sender.name}; Task ID: {task_id};\n\nTraceback:\n\n{einfo.traceback};')

        if tj := self.get_task_job(task_id, sender.request):
            tj.status = TaskJobStatusEnum.failed
            tj.retries = sender.request.retries

            errors = None
            if tj.output:
                try:
                    errors = json.loads(tj.errors)
                except json.decoder.JSONDecodeError:
                    pass
            if not isinstance(errors, list):
                errors = []
            errors.append(str(einfo))
            if errors:
                tj.errors = json.dumps(errors)

            self.save_task_job(tj)

        zabbix.report([ZabbixMetric(f'task.{tj.name}.status', -1)])

        event = TaskFailedEvent(
            task=sender,
            context=sender.request,
            exception=exception,
            einfo=einfo,
        )

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        try:
            NotificationManager(configs=notifications).handle_event(event)
        except Exception as e:
            import traceback
            logger.warning(e)
            logger.warning(traceback.format_exception(type(e), e, e.__traceback__))

    def task_unknown_handler(self, name: str, id: str, message: Message, exc: Exception, **kw):
        from loguru import logger
        from app import notifications
        from lib.enums import TaskEnum
        from lib.notifications import NotificationManager
        from lib.notifications.events import TaskUnknownEvent

        logger.debug(f'Task Unknown: Task Name: {name}; Task ID: {id}; Message: {message}; Exception: {exc}')

        msg = f'The task "{name}" is unknown and could not be executed.\n\nTask ID: {id}; Message: {message}; Exception: {exc}'

        if name not in self._ignored_tasks:
            self.app.send_task(TaskEnum.PDA_ALERT.value, kwargs={'msg': msg, 'info': f'{message}\n\n{exc}'})

        event = TaskUnknownEvent(
            message=message,
            exception=exc,
        )
        event.task_id = id
        event.task_name = name

        # TODO: Implement a way to handle mailing tasks to prevent infinite recursion
        NotificationManager(configs=notifications).handle_event(event)
