import uuid
from datetime import datetime, UTC

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    statement: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    input_format: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    output_format: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    constraints: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sample_input: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sample_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    time_limit: Mapped[int] = mapped_column(
        Integer,
        default=2,
    )

    memory_limit: Mapped[int] = mapped_column(
        Integer,
        default=256,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )