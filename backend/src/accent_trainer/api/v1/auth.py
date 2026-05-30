"""Auth routes: register, login, logout, JWT verification."""

from __future__ import annotations

from fastapi import APIRouter

from accent_trainer.api.v1.schemas.user import UserCreate, UserRead
from accent_trainer.infrastructure.auth.backend import auth_backend
from accent_trainer.infrastructure.auth.users import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)