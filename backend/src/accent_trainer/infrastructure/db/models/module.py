from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Float

from accent_trainer.infrastructure.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from accent_trainer.infrastructure.db.models.course import CourseModel
    from accent_trainer.infrastructure.db.models.exercise import ExerciseModel


class ModuleModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "modules"

    course_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    target_phonemes: Mapped[list[str]] = mapped_column(
        ARRAY(String(8)), default=list, nullable=False
    )
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    passing_threshold: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    final_check_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)

    course: Mapped["CourseModel"] = relationship(back_populates="modules")
    exercises: Mapped[list["ExerciseModel"]] = relationship(
        back_populates="module",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
