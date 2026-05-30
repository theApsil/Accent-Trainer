from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["system"], summary="Healthcheck")
async def health() -> dict[str, str]:
    """Return service liveness status."""
    return {"status": "ok"}
