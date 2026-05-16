# Accent Trainer — Backend

FastAPI-сервис: REST API, аутентификация, анализ произношения.

## Стек
- Python 3.11+, uv
- FastAPI + Uvicorn
- SQLAlchemy 2.0 + Alembic + PostgreSQL 16
- faster-whisper, parselmouth, librosa, Piper TTS
- MinIO (S3), Redis, arq

## Структура
```bash
src/accent_trainer/
├── core/             # инфраструктурные мелочи (logging, security)
├── domain/           # entities + value objects (без зависимостей)
├── application/      # use-cases, интерфейсы, DTO
├── infrastructure/   # реализации портов (DB, ASR, TTS, storage)
├── api/              # FastAPI роутеры + схемы
├── main.py           # app factory
└── config.py         # Pydantic Settings
```
См. [../docs/architecture.md](../docs/architecture.md).

## Локальный запуск

> Будет настроено в этапах feature/backend-core и далее.
```bash
uv sync
uv run uvicorn accent_trainer.main:app --reload --port 8000
```
## Тесты
`uv run pytest`