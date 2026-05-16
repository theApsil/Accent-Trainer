# Accent Trainer — Backend

FastAPI-сервис: REST API, аутентификация, анализ произношения.

## Стек
- Python 3.13+, uv
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

## Запуск backend-сервиса
### 1. В корне проекта
```bash
cd backend
cp .env.example .env
uv sync
uv run uvicorn accent_trainer.main:app --reload --host 0.0.0.0 --port 8000
curl http://localhost:8000/api/v1/health
```
#### curl должен вернуть {"status":"ok"}
### *. Проверка тестов и линтеров
```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

### 2. Поднять все сервисы
`docker compose up -d`

### 3. Проверить статусы
`docker compose ps`
#### postgres, redis, minio должны быть (healthy)
#### minio-init должен завершиться со статусом Exited (0)

### 4. Логи (если что-то не так)
```bash
docker compose logs -f postgres
docker compose logs -f minio
docker compose logs minio-init
```
### 5. Проверка подключений
####   Postgres:
`docker exec -it accent-postgres psql -U accent -d accent_trainer -c "SELECT version();"`

###    Redis:
`docker exec -it accent-redis redis-cli ping`
#### → PONG

###    MinIO console:
Открыть http://localhost:9001
#### логин: minioadmin / minioadmin_dev_pw
#### должны быть бакеты: user-recordings, reference-audio, spectrograms

### 6. Остановить (данные сохранятся в volumes)
`docker compose down`