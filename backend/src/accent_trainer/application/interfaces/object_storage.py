from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from datetime import timedelta
from typing import IO


class ObjectStorage(ABC):
    """Storage abstraction independent of backend (MinIO/S3/local fs)."""

    @abstractmethod
    async def put_object(
        self,
        bucket: str,
        key: str,
        data: IO[bytes] | bytes,
        content_type: str,
        length: int | None = None,
    ) -> None:
        """Upload an object."""

    @abstractmethod
    async def get_object(self, bucket: str, key: str) -> bytes:
        """Download an object fully into memory."""

    @abstractmethod
    async def stream_object(
        self,
        bucket: str,
        key: str,
        chunk_size: int = 64 * 1024,
    ) -> AsyncIterator[bytes]:
        """Stream object content."""

    @abstractmethod
    async def delete_object(self, bucket: str, key: str) -> None:
        """Delete object (idempotent)."""

    @abstractmethod
    async def object_exists(self, bucket: str, key: str) -> bool:
        """Check whether object exists."""

    @abstractmethod
    async def presigned_get_url(
        self,
        bucket: str,
        key: str,
        expires: timedelta = timedelta(hours=1),
    ) -> str:
        """Return a temporary URL for direct client download."""