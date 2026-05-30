from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_trainer.infrastructure.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from accent_trainer.infrastructure.db.models.module import ModuleModel


class CourseModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "courses"

    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    target_language: Mapped[str] = mapped_column(String(16), nullable=False)
    source_language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    modules: Mapped[list["ModuleModel"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        lazy="selectin",
    )