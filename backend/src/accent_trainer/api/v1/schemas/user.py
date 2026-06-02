from __future__ import annotations

import uuid

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    """What we return to clients."""

    native_language: str | None = None


class UserCreate(schemas.BaseUserCreate):
    """What clients send to /auth/register.

    Note: is_active / is_superuser / is_verified are intentionally
    not exposed — fastapi-users ignores them on registration anyway.
    """

    native_language: str | None = Field(default=None, max_length=16)


class UserUpdate(schemas.BaseUserUpdate):
    """What users can update on themselves via PATCH /users/me.

    Superusers can additionally toggle is_active / is_superuser / is_verified
    via PATCH /users/{id} — those fields are kept in the base class.
    """

    native_language: str | None = Field(default=None, max_length=16)