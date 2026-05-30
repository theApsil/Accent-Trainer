from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_trainer.infrastructure.db.base import Base, TimestampMixin, UUIDMixin


class ExerciseModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "exercises"

    module_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("modules.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    module: Mapped["ModuleModel"] = relationship(back_populates="exercises")  # noqa: F821
    tasks: Mapped[list["TaskModel"]] = relationship(  # noqa: F821
        back_populates="exercise",
        cascade="all, delete-orphan",
        lazy="selectin",
    )