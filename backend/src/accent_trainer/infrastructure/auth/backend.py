from __future__ import annotations

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from accent_trainer.config import get_settings


def _token_url() -> str:
    # Absolute path relative to the API root, so Swagger UI resolves it correctly.
    return f"{get_settings().api.v1_prefix}/auth/jwt/login"


bearer_transport = BearerTransport(tokenUrl=_token_url())


def get_jwt_strategy() -> JWTStrategy:
    settings = get_settings()
    return JWTStrategy(
        secret=settings.auth.secret,
        lifetime_seconds=settings.auth.jwt_lifetime_seconds,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)