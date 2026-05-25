import uuid

from sqlalchemy import (
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class ProblemTag(Base):
    __tablename__ = "problem_tags"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    problem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "problems.id",
            ondelete="CASCADE",
        ),
    )

    tag: Mapped[str] = mapped_column(
        String(50),
    )