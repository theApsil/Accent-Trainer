"""User ORM model — integrated with fastapi-users."""

from __future__ import annotations

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from accent_trainer.infrastructure.db.base import Base, TimestampMixin


class UserModel(SQLAlchemyBaseUserTableUUID, Base, TimestampMixin):
    __tablename__ = "users"

    native_language: Mapped[str | None] = mapped_column(String(16), nullable=True)