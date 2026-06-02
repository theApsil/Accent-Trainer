from __future__ import annotations

from functools import lru_cache

from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.application.interfaces.tts_service import TTSService
from accent_trainer.config import Settings, get_settings
from accent_trainer.infrastructure.storage.minio_storage import MinIOStorage
from accent_trainer.infrastructure.tts.piper_service import PiperTTSService
from accent_trainer.application.interfaces.aligner import Aligner
from accent_trainer.application.interfaces.asr_service import ASRService
from accent_trainer.application.interfaces.g2p_service import G2PService
from accent_trainer.application.interfaces.object_storage import ObjectStorage
from accent_trainer.application.interfaces.tts_service import TTSService
from accent_trainer.config import Settings, get_settings
from accent_trainer.infrastructure.asr.faster_whisper_asr import FasterWhisperASR
from accent_trainer.infrastructure.asr.g2p_en_service import G2PEnService
from accent_trainer.infrastructure.asr.proxy_aligner import ProxyAligner
from accent_trainer.application.interfaces.formant_extractor import (
    FormantExtractor,
)
from accent_trainer.infrastructure.audio.converter import AudioConverter
from accent_trainer.infrastructure.audio.formant_extractor import (
    LPCFormantExtractor,
)


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


@lru_cache(maxsize=1)
def _asr_singleton() -> ASRService:
    return FasterWhisperASR(settings=get_settings())


def get_asr_service() -> ASRService:
    return _asr_singleton()


@lru_cache(maxsize=1)
def _g2p_singleton() -> G2PService:
    return G2PEnService()


def get_g2p_service() -> G2PService:
    return _g2p_singleton()


@lru_cache(maxsize=1)
def _aligner_singleton() -> Aligner:
    return ProxyAligner()


def get_aligner() -> Aligner:
    return _aligner_singleton()


@lru_cache(maxsize=1)
def _formant_singleton() -> FormantExtractor:
    return LPCFormantExtractor(settings=get_settings())


def get_formant_extractor() -> FormantExtractor:
    return _formant_singleton()


@lru_cache(maxsize=1)
def _converter_singleton() -> AudioConverter:
    return AudioConverter(settings=get_settings())


def get_audio_converter() -> AudioConverter:
    return _converter_singleton()