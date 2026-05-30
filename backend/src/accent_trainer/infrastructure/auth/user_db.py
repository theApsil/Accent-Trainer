from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from accent_trainer.infrastructure.db.models.user import UserModel
from accent_trainer.infrastructure.db.session import get_session


async def get_user_db(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[SQLAlchemyUserDatabase[UserModel, ...]]:  # type: ignore[type-arg]
    yield SQLAlchemyUserDatabase(session, UserModel)