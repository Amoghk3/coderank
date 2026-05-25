import uuid
from datetime import datetime, UTC

from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class Leaderboard(Base):
    __tablename__ = "leaderboards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
    )

    accepted_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    total_submissions: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    total_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    best_runtime_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )