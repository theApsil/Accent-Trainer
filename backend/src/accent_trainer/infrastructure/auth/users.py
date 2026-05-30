from __future__ import annotations

import uuid

from fastapi_users import FastAPIUsers

from accent_trainer.infrastructure.auth.backend import auth_backend
from accent_trainer.infrastructure.auth.user_manager import get_user_manager
from accent_trainer.infrastructure.db.models.user import UserModel

fastapi_users = FastAPIUsers[UserModel, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)