from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from accent_trainer.api.errors import register_exception_handlers
from accent_trainer.api.v1.router import router as v1_router
from accent_trainer.config import Settings, get_settings
from accent_trainer.core.logging import configure_logging


@asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown hooks placeholder."""
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = settings or get_settings()
    configure_logging(settings.app.log_level)

    app = FastAPI(
        title=settings.app.name,
        debug=settings.app.debug,
        lifespan=_lifespan,
    )

    if settings.api.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.api.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    register_exception_handlers(app)
    app.include_router(v1_router, prefix=settings.api.v1_prefix)

    return app


app = create_app()
