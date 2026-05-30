from __future__ import annotations

import uuid
import logging
from collections.abc import AsyncIterator

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from accent_trainer.config import get_settings
from accent_trainer.infrastructure.auth.user_db import get_user_db
from accent_trainer.infrastructure.db.models.user import UserModel

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[UserModel, uuid.UUID]):
    @property
    def reset_password_token_secret(self) -> str:
        return get_settings().auth.secret

    @property
    def verification_token_secret(self) -> str:
        return get_settings().auth.secret

    async def on_after_register(
        self,
        user: UserModel,
        request: Request | None = None,
    ) -> None:
        logger.info("User registered: %s", user.email)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[UserModel, uuid.UUID] = Depends(get_user_db),
) -> AsyncIterator[UserManager]:
    yield UserManager(user_db)