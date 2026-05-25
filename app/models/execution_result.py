import uuid
from datetime import datetime, UTC

from sqlalchemy import (
    Text,
    ForeignKey,
    DateTime,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class ExecutionResult(Base):
    __tablename__ = "execution_results"

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
    )

    stdout: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    stderr: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )