"""Verify async DB connection works."""

import pytest
from sqlalchemy import text

from accent_trainer.infrastructure.db.session import get_engine


@pytest.mark.asyncio
async def test_db_connect_and_select_one() -> None:
    engine = get_engine()
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
    await engine.dispose()
