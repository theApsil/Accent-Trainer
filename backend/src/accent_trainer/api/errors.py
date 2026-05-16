from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from accent_trainer.core.exceptions import (
    AppError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach exception handlers to the FastAPI app."""

    @app.exception_handler(NotFoundError)
    async def _not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def _validation(_: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedError)
    async def _unauthorized(_: Request, exc: UnauthorizedError) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(AppError)
    async def _generic(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": str(exc)})