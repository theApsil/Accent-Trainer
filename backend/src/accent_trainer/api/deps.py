from __future__ import annotations

from functools import lru_cache

from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.infrastructure.storage.minio_storage import MinIOStorage


@lru_cache(maxsize=1)
def _storage_singleton() -> ObjectStorage:
    return MinIOStorage()


def get_object_storage() -> ObjectStorage:
    return _storage_singleton()