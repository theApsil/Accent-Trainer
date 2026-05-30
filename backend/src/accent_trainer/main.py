from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from accent_trainer.api.errors import register_exception_handlers
from accent_trainer.api.v1.router import router as v1_router
from accent_trainer.config import get_settings
from accent_trainer.core.logging import setup_logging
from accent_trainer.infrastructure.storage.minio_client import ensure_buckets

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging()
    logger.info("Starting up...")
    try:
        ensure_buckets()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to ensure MinIO buckets; continuing")
    yield
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app.name,
        debug=settings.app.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.cors_origins or ["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    register_exception_handlers(app)
    app.include_router(v1_router, prefix=settings.api.v1_prefix)
    return app


app = create_app()