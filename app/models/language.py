import uuid

from sqlalchemy import (
    String,
    Integer,
    Boolean,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    docker_image: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    compile_command: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    run_command: Mapped[str] = mapped_column(
        String(500),
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

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )