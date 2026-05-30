from __future__ import annotations

import logging
import uuid
from collections.abc import AsyncIterator
from typing import Any

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, InvalidPasswordException, UUIDIDMixin
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

    async def validate_password(
        self,
        password: str,
        user: UserModel | Any,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password must be at least 8 characters long."
            )
        if user and isinstance(user, UserModel) and password.lower() in user.email.lower():
            raise InvalidPasswordException(
                reason="Password must not contain the email."
            )

    async def on_after_register(
        self,
        user: UserModel,
        request: Request | None = None,
    ) -> None:
        logger.info("User registered: %s (id=%s)", user.email, user.id)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[UserModel, uuid.UUID] = Depends(get_user_db),
) -> AsyncIterator[UserManager]:
    yield UserManager(user_db)