from __future__ import annotations

from functools import lru_cache

from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.application.interfaces.tts_service import TTSService
from accent_trainer.config import Settings, get_settings
from accent_trainer.infrastructure.storage.minio_storage import MinIOStorage
from accent_trainer.infrastructure.tts.piper_service import PiperTTSService


@lru_cache(maxsize=1)
def _storage_singleton() -> ObjectStorage:
    return MinIOStorage()


def get_object_storage() -> ObjectStorage:
    return _storage_singleton()


@lru_cache(maxsize=1)
def _tts_singleton() -> TTSService:
    return PiperTTSService(settings=get_settings())


def get_tts_service() -> TTSService:
    return _tts_singleton()