import uuid

from sqlalchemy import (
    Text,
    Boolean,
    Integer,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    problem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("problems.id"),
        nullable=False,
    )

    input_data: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    points: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )