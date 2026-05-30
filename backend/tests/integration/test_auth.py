from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_login_me(client: AsyncClient) -> None:
    email = "alice@example.com"
    password = "Sup3rSecret!"

    r = await client.post(
        "/api/v1/auth/jwt/login",
        data={"username": email, "password": password},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    r = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == email
    assert body["is_active"] is True