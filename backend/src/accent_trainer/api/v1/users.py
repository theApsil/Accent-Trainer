from __future__ import annotations

from fastapi import APIRouter

from accent_trainer.api.v1.schemas.user import UserRead, UserUpdate
from accent_trainer.infrastructure.auth.users import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["users"],
)