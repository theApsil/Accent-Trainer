from fastapi import APIRouter

from accent_trainer.api.v1.auth import router as auth_router
from accent_trainer.api.v1.users import router as users_router

router = APIRouter()


@router.get("/health", tags=["system"], summary="Healthcheck")
async def health() -> dict[str, str]:
    return {"status": "ok"}


router.include_router(auth_router, prefix="/auth")
router.include_router(users_router, prefix="/users")