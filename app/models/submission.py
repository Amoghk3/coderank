import uuid
from datetime import datetime, UTC

from sqlalchemy import (
    Boolean,
    Text,
    Integer,
    ForeignKey,
    DateTime,
    Enum,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base
from app.models.enums import SubmissionStatus


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    problem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("problems.id"),
        nullable=False,
    )

    language_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("languages.id"),
        nullable=False,
    )

    source_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    custom_input: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(SubmissionStatus),
        default=SubmissionStatus.PENDING,
    )

    runtime_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    memory_kb: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    is_judge: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    execution_results = relationship(
        "ExecutionResult",
        backref="submission",
    )

    judge_case_results = relationship(
        "JudgeCaseResult",
        backref="submission",
    )