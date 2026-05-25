import uuid

from sqlalchemy import (
    Text,
    Boolean,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class JudgeCaseResult(Base):
    __tablename__ = "judge_case_results"

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

    test_case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "test_cases.id",
            ondelete="CASCADE",
        ),
    )

    expected_output: Mapped[str] = mapped_column(
        Text,
    )

    actual_output: Mapped[str] = mapped_column(
        Text,
    )

    passed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )