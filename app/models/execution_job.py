import uuid
from datetime import datetime, UTC

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base

from app.models.enums import (
    ExecutionJobStatus,
)


class ExecutionJob(Base):
    __tablename__ = "execution_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "submissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    celery_task_id: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[ExecutionJobStatus] = mapped_column(
        Enum(ExecutionJobStatus),
        default=ExecutionJobStatus.QUEUED,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )