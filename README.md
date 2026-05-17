# Accent Trainer — Тренажёр коррекции акцентуализированной речи

Веб-сервис для коррекции акцента в английской речи для носителей
других языковых групп. Анализирует произношение пользователя
с помощью ASR и фонетических признаков (MFCC, форманты F1/F2/F3),
визуализирует положение языка и даёт целенаправленные советы.

> Выпускная квалификационная работа магистра.

---

## Ключевые возможности

- Запись речи прямо в браузере (MediaRecorder API)
- ASR + forced alignment (Whisper / WhisperX) для фонемной разметки
- Анализ произношения: MFCC, форманты, спектрограмма
- Эталонное произношение — всегда доступно для прослушивания
  (Piper TTS + кэш в MinIO + сэмплы CMU ARCTIC)
- Визуализация позиции языка на схеме речевого аппарата
  (по F1 / F2)
- Иерархия обучения: Курс → Модуль → Упражнение → Задание
- Контрольные точки — финальное предложение при 100% прогресса модуля
- Прогресс пользователя с дашбордом
- Аутентификация (JWT)

---

## Технологический стек

### Backend
- Python 3.11+, пакетный менеджер uv
- FastAPI + Uvicorn
- SQLAlchemy 2.0 + Alembic (PostgreSQL 16)
- fastapi-users (JWT auth)
- faster-whisper (ASR, поддержка CUDA / Apple MPS)
- praat-parselmouth (форманты)
- librosa, numpy, scipy (MFCC, спектрограмма)
- Piper TTS (генерация эталонного произношения)
- MinIO (S3-совместимое хранилище аудио)
- arq + Redis (фоновые задачи)

### Frontend
- React 18 + TypeScript, сборка через Vite
- Tailwind CSS + shadcn/ui
- Zustand (state) + TanStack Query (HTTP-кэш)
- wavesurfer.js (визуализация записи)
- Recharts / D3 (форманты, спектрограмма)

### Инфраструктура
- Docker + docker-compose
- GitHub Actions (CI: ruff, mypy, pytest, frontend build)

---

## 📁 Структура репозитория
```bash
accent-trainer/
├── backend/        # FastAPI backend, clean architecture
├── frontend/       # React SPA
├── docs/           # Архитектура, пайплайн анализа, setup
├── docker-compose.yml
└── README.md
```
Подробнее: [`docs/architecture.md`](docs/architecture.md)


---

## 🚀 Быстрый старт

См. [`docs/setup.md`](docs/setup.md) для пошаговой инструкции.

Кратко:
cp .env.example .env
docker compose up -d postgres redis minio
# далее — установка backend и frontend (см. docs/setup.md)
---

## 🗺️ Roadmap

| Этап | Ветка | Статус |
|---|---|---|
| 1. Скелет репозитория | feature/project-skeleton | 🟢 сделано |
| 2. Docker Compose инфра | feature/infra-compose | 🟢 сделано |
| 3. Backend core (FastAPI) | feature/backend-core | 🟢 сделано |
| 4. БД и миграции | feature/db-models | 🟡 в работе  |
| 5. Аутентификация | feature/auth | ⏳ |
| 6. Аудио-пайплайн (MFCC, форманты) | feature/audio-pipeline | ⏳ |
| 7. ASR (Whisper) | feature/asr-whisper | ⏳ |
| 8. TTS эталонов (Piper + MinIO) | feature/tts-reference | ⏳ |
| 9. Use-case анализа | feature/analyze-usecase | ⏳ |
| 10. API упражнений и прогресса | feature/exercises-api | ⏳ |
| 11. Финальная проверка | feature/final-check | ⏳ |
| 12. Frontend скелет | feature/frontend-skeleton | ⏳ |
| 13. Frontend auth | feature/frontend-auth | ⏳ |
| 14. Recorder + загрузка | feature/frontend-recorder | ⏳ |
| 15. Визуализации | feature/frontend-visualization | ⏳ |
| 16. Прогресс / дашборд | feature/frontend-progress | ⏳ |
| 17. CI | chore/ci | ⏳ |

---

## 📚 Документация

- [Архитектура](docs/architecture.md) — слои, диаграммы, обоснование выбора
- [Пайплайн анализа речи](docs/phoneme_pipeline.md) — от записи до советов
- [Setup](docs/setup.md) — установка и запуск
- [API](docs/api.md) — спецификация REST-эндпоинтов *(заполняется по мере разработки)*

| Документ | О чём |
|---|---|
| [docs/architecture.md](docs/architecture.md) | Архитектура: слои, диаграммы, обоснование выбора стека |
| [docs/phoneme_pipeline.md](docs/phoneme_pipeline.md) | Пайплайн анализа речи — от записи до советов |
| [docs/setup.md](docs/setup.md) | Установка пререквизитов, запуск проекта |
| [docs/api.md](docs/api.md) | Спецификация REST-эндпоинтов *(заполняется по мере разработки)* |
| [backend/README.md](backend/README.md) | Per-package: backend |
| [frontend/README.md](frontend/README.md) | Per-package: frontend |
---

## 📝 Лицензия

MIT
