"""
PDA Task Database Models

This file defines the database models associated with task functionality.
"""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, DECIMAL, Integer, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from models.db import BaseSqlModel
from models.enums import TaskJobStatusEnum


class TaskJob(BaseSqlModel):
    """Represents a PDA task job."""

    __tablename__ = 'pda_task_jobs'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    """The unique identifier of the record."""

    root_id: Mapped[str] = mapped_column(Uuid)
    """The unique identifier of the Celery root task associated with this task."""

    parent_id: Mapped[Optional[str]] = mapped_column(Uuid)
    """The unique identifier of the Celery parent task associated with this task."""

    task_id: Mapped[Optional[str]] = mapped_column(Uuid)
    """The unique identifier of the Celery task associated with this task."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    """The name of the Celery task."""

    args: Mapped[Optional[str]] = mapped_column(TEXT)
    """The JSON-encoded arguments of the Celery task."""

    kwargs: Mapped[Optional[str]] = mapped_column(TEXT)
    """The JSON-encoded keyword arguments of the Celery task."""

    options: Mapped[Optional[str]] = mapped_column(TEXT)
    """The JSON-encoded options of the Celery task."""

    retries: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, default=0)
    """The total number of execution retries performed."""

    runtime: Mapped[Optional[float]] = mapped_column(DECIMAL(14, 6))
    """The total runtime of the task job in seconds."""

    output: Mapped[Optional[str]] = mapped_column(TEXT)
    """The captured STDOUT and STDERR of the task job."""

    errors: Mapped[Optional[str]] = mapped_column(TEXT)
    """The captured exception stacktraces of the task job."""

    status: Mapped[TaskJobStatusEnum] = mapped_column(String(20), nullable=False)
    """The current status of the task job."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    started_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    """The timestamp representing when the task job was started."""

    ended_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    """The timestamp representing when the task job was completed."""

    activities = relationship('TaskJobActivity', back_populates='task_job')
    """A list of activities associated with the task job."""


class TaskJobActivity(BaseSqlModel):
    """Represents a PDA task job activity update."""

    __tablename__ = 'pda_task_job_activities'
    """Defines the database table name."""

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the record."""

    task_job_id: Mapped[str] = mapped_column(Uuid, ForeignKey('pda_task_jobs.id'), nullable=False)
    """The unique identifier of the task job associated with this activity update."""

    error: Mapped[Optional[str]] = mapped_column(TEXT)
    """The captured exception stacktrace of a failed task job execution."""

    status: Mapped[TaskJobStatusEnum] = mapped_column(String(20), nullable=False)
    """The status of the task job for the activity update."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    task_job = relationship('TaskJob', back_populates='activities')
    """The task job associated with the activity update."""
