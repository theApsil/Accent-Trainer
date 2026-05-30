from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterable
from uuid import UUID

from accent_trainer.application.use_cases.get_reference_audio import (
    GetReferenceAudio,
)

logger = logging.getLogger(__name__)


async def warmup_references(
    use_case: GetReferenceAudio,
    items: Iterable[tuple[UUID, str]],
    voice: str | None = None,
    concurrency: int = 4,
) -> None:
    sem = asyncio.Semaphore(concurrency)

    async def _one(task_id: UUID, text: str) -> None:
        async with sem:
            try:
                res = await use_case.execute(task_id=task_id, text=text, voice=voice)
                logger.info(
                    "warmup task=%s cached=%s key=%s", task_id, res.cached, res.key
                )
            except Exception:  # noqa: BLE001
                logger.exception("warmup failed for task=%s", task_id)

    await asyncio.gather(*(_one(tid, text) for tid, text in items))