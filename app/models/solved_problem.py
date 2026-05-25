import uuid
from datetime import (
    datetime,
    UTC,
)

from sqlalchemy import (
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class SolvedProblem(Base):

    __tablename__ = "solved_problems"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "problem_id",
            name=(
                "uq_user_problem_solved"
            ),
        ),
    )

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
    )

    problem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "problems.id",
            ondelete="CASCADE",
        ),
    )

    first_submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "submissions.id",
            ondelete="CASCADE",
        ),
    )

    solved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )