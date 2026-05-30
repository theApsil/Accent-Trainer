from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_trainer.infrastructure.db.base import Base, TimestampMixin, UUIDMixin


class TaskModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tasks"

    exercise_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    phonemes: Mapped[list[str]] = mapped_column(
        ARRAY(String(8)), default=list, nullable=False
    )
    reference_audio_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    exercise: Mapped["ExerciseModel"] = relationship(back_populates="tasks")  # noqa: F821