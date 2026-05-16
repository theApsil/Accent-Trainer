# Архитектура

## Полная файловая структура
```bash
├── README.md
├── backend
│   ├── Dockerfile
│   ├── README.md
│   ├── alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   ├── alembic.ini
│   ├── data
│   │   ├── arpabet_to_ipa.json
│   │   ├── exercises_seed.json
│   │   ├── hillenbrand_vowels.csv
│   │   └── piper_voices
│   ├── pyproject.toml
│   ├── src
│   │   ├── __init__.py
│   │   └── accent_trainer
│   │       ├── __init__.py
│   │       ├── api
│   │       │   ├── __init__.py
│   │       │   ├── deps.py
│   │       │   ├── errors.py
│   │       │   └── v1
│   │       │       ├── __init__.py
│   │       │       ├── attempts.py
│   │       │       ├── auth.py
│   │       │       ├── courses.py
│   │       │       ├── exercises.py
│   │       │       ├── modules.py
│   │       │       ├── progress.py
│   │       │       ├── reference.py
│   │       │       ├── router.py
│   │       │       ├── schemas
│   │       │       │   ├── __init__.py
│   │       │       │   ├── analysis.py
│   │       │       │   ├── attempt.py
│   │       │       │   ├── auth.py
│   │       │       │   ├── exercise.py
│   │       │       │   ├── progress.py
│   │       │       │   └── user.py
│   │       │       └── users.py
│   │       ├── application
│   │       │   ├── __init__.py
│   │       │   ├── dto
│   │       │   │   ├── __init__.py
│   │       │   │   ├── analysis_dto.py
│   │       │   │   ├── exercise_dto.py
│   │       │   │   └── progress_dto.py
│   │       │   ├── interfaces
│   │       │   │   ├── __init__.py
│   │       │   │   ├── asr_service.py
│   │       │   │   ├── audio_analyzer.py
│   │       │   │   ├── object_storage.py
│   │       │   │   ├── repositories.py
│   │       │   │   └── tts_service.py
│   │       │   └── use_cases
│   │       │       ├── __init__.py
│   │       │       ├── analyze_pronunciation.py
│   │       │       ├── final_check.py
│   │       │       ├── get_progress.py
│   │       │       ├── get_reference_audio.py
│   │       │       ├── start_session.py
│   │       │       └── submit_attempt.py
│   │       ├── config.py
│   │       ├── core
│   │       │   ├── __init__.py
│   │       │   ├── exceptions.py
│   │       │   ├── logging.py
│   │       │   └── security.py
│   │       ├── domain
│   │       │   ├── __init__.py
│   │       │   ├── entities
│   │       │   │   ├── __init__.py
│   │       │   │   ├── attempt.py
│   │       │   │   ├── course.py
│   │       │   │   ├── exercise.py
│   │       │   │   ├── module.py
│   │       │   │   ├── phoneme_report.py
│   │       │   │   ├── progress.py
│   │       │   │   ├── task.py
│   │       │   │   └── user.py
│   │       │   └── value_objects
│   │       │       ├── __init__.py
│   │       │       ├── formants.py
│   │       │       ├── mfcc.py
│   │       │       ├── phoneme.py
│   │       │       └── tongue_position.py
│   │       ├── infrastructure
│   │       │   ├── __init__.py
│   │       │   ├── asr
│   │       │   │   ├── __init__.py
│   │       │   │   ├── aligner.py
│   │       │   │   ├── g2p.py
│   │       │   │   └── whisper_service.py
│   │       │   ├── audio
│   │       │   │   ├── __init__.py
│   │       │   │   ├── advice_generator.py
│   │       │   │   ├── formant_extractor.py
│   │       │   │   ├── mfcc_extractor.py
│   │       │   │   ├── reference_db.py
│   │       │   │   └── spectrogram.py
│   │       │   ├── db
│   │       │   │   ├── __init__.py
│   │       │   │   ├── base.py
│   │       │   │   ├── models
│   │       │   │   │   ├── __init__.py
│   │       │   │   │   ├── attempt.py
│   │       │   │   │   ├── course.py
│   │       │   │   │   ├── exercise.py
│   │       │   │   │   ├── module.py
│   │       │   │   │   ├── progress.py
│   │       │   │   │   ├── task.py
│   │       │   │   │   └── user.py
│   │       │   │   ├── repositories
│   │       │   │   │   ├── __init__.py
│   │       │   │   │   ├── attempt_repo.py
│   │       │   │   │   ├── exercise_repo.py
│   │       │   │   │   ├── progress_repo.py
│   │       │   │   │   └── user_repo.py
│   │       │   │   └── session.py
│   │       │   ├── storage
│   │       │   │   ├── __init__.py
│   │       │   │   ├── file_storage.py
│   │       │   │   └── minio_client.py
│   │       │   ├── tasks
│   │       │   │   ├── __init__.py
│   │       │   │   ├── jobs.py
│   │       │   │   └── worker.py
│   │       │   └── tts
│   │       │       ├── __init__.py
│   │       │       ├── piper_service.py
│   │       │       └── reference_cache.py
│   │       └── main.py
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       ├── integration
│       │   └── __init__.py
│       └── unit
│           └── __init__.py
├── docker-compose.dev.yml
├── docker-compose.yml
├── docs
│   ├── api.md
│   ├── architecture.md
│   ├── phoneme_pipeline.md
│   └── setup.md
└── frontend
    ├── Dockerfile
    ├── README.md
    ├── index.html
    ├── package.json
    ├── postcss.config.js
    ├── public
    ├── src
    │   ├── App.tsx
    │   ├── api
    │   │   ├── client.ts
    │   │   └── endpoints
    │   │       ├── attempts.ts
    │   │       ├── auth.ts
    │   │       ├── exercises.ts
    │   │       ├── progress.ts
    │   │       └── reference.ts
    │   ├── assets
    │   ├── features
    │   │   ├── auth
    │   │   │   ├── components
    │   │   │   ├── hooks
    │   │   │   │   └── useAuth.ts
    │   │   │   └── pages
    │   │   │       ├── LoginPage.tsx
    │   │   │       └── RegisterPage.tsx
    │   │   ├── course
    │   │   │   ├── components
    │   │   │   ├── hooks
    │   │   │   └── pages
    │   │   │       ├── CourseDetailPage.tsx
    │   │   │       └── CoursesListPage.tsx
    │   │   ├── exercise
    │   │   │   ├── components
    │   │   │   │   ├── AdviceList.tsx
    │   │   │   │   ├── FormantChart.tsx
    │   │   │   │   ├── MfccHeatmap.tsx
    │   │   │   │   ├── Recorder.tsx
    │   │   │   │   ├── ReferencePlayer.tsx
    │   │   │   │   ├── SpectrogramView.tsx
    │   │   │   │   └── TongueDiagram.tsx
    │   │   │   ├── hooks
    │   │   │   │   ├── useAnalysis.ts
    │   │   │   │   └── useRecorder.ts
    │   │   │   └── pages
    │   │   │       └── ExercisePage.tsx
    │   │   ├── final-test
    │   │   │   ├── components
    │   │   │   ├── hooks
    │   │   │   └── pages
    │   │   │       └── FinalTestPage.tsx
    │   │   ├── module
    │   │   │   ├── components
    │   │   │   │   └── ModuleProgress.tsx
    │   │   │   ├── hooks
    │   │   │   └── pages
    │   │   │       └── ModuleDetailPage.tsx
    │   │   └── progress
    │   │       ├── components
    │   │       │   └── ProgressBar.tsx
    │   │       ├── hooks
    │   │       └── pages
    │   │           └── DashboardPage.tsx
    │   ├── main.tsx
    │   ├── routes
    │   │   ├── ProtectedRoute.tsx
    │   │   └── index.tsx
    │   ├── shared
    │   │   ├── config
    │   │   │   └── env.ts
    │   │   ├── hooks
    │   │   ├── lib
    │   │   ├── types
    │   │   │   └── api.ts
    │   │   └── ui
    │   ├── store
    │   │   ├── authStore.ts
    │   │   └── sessionStore.ts
    │   ├── styles
    │   │   ├── globals.css
    │   │   └── tailwind.css
    │   └── vite-env.d.ts
    ├── tailwind.config.js
    ├── tsconfig.json
    ├── tsconfig.node.json
    └── vite.config.ts
```


## Принципы

Проект придерживается Clean Architecture (Robert C. Martin) с
четырьмя слоями. Зависимости направлены строго внутрь: внешние
слои знают о внутренних, обратное запрещено.
```bash
┌─────────────────────────────────────────────────────────┐
│                       api (FastAPI)                     │
│   контроллеры, Pydantic-схемы, зависимости (DI)         │
└───────────────────────────┬─────────────────────────────┘
                            │ вызывает
┌───────────────────────────▼─────────────────────────────┐
│                    application                          │
│   use-cases, DTO, интерфейсы (порты)                    │
└───────────────────────────┬─────────────────────────────┘
                            │ оперирует
┌───────────────────────────▼─────────────────────────────┐
│                       domain                            │
│   сущности, value objects (без сторонних зависимостей)  │
└─────────────────────────────────────────────────────────┘
                            ▲
                            │ реализует порты
┌───────────────────────────┴─────────────────────────────┐
│                  infrastructure                         │
│  SQLAlchemy, MinIO, Whisper, Praat, Piper, arq          │
└─────────────────────────────────────────────────────────┘
```
### Слои

| Слой | Содержимое | Зависимости |
|---|---|---|
| domain | Entities, Value Objects, доменные правила | — |
| application | Use-cases, DTO, абстрактные интерфейсы (`asr_service.py`, tts_service.py, repositories.py, …) | domain |
| infrastructure | Реализации портов: SQLAlchemy-репозитории, MinIO-клиент, Whisper-сервис, Praat-извлекатель формант, Piper TTS, arq-воркер | domain, application |
| api | FastAPI-роутеры, Pydantic-схемы, DI через Depends | application, infrastructure (только в `deps.py`) |

### Правила
1. domain не импортирует ничего из других слоёв и внешних библиотек (только stdlib + pydantic для VO).
2. application определяет интерфейсы; конкретные реализации — в infrastructure.
3. Связывание реализаций со слоями происходит в api/deps.py через FastAPI Depends.
4. Use-case не знает про HTTP. Контроллер — это тонкий адаптер.

---

## Высокоуровневая схема развёртывания
```bash
┌──────────────┐   HTTPS    ┌─────────────┐    ┌──────────────┐
│  React SPA   │ ─────────► │   FastAPI   │ ─► │  PostgreSQL  │
│ (Vite build) │            │  (Uvicorn)  │    └──────────────┘
└──────────────┘            └──┬───────┬──┘    ┌──────────────┐
                               │       └─────► │    MinIO     │
                               │               └──────────────┘
                               │ enqueue
                          ┌────▼────┐          ┌──────────────┐
                          │  Redis  │ ◄──poll──┤   arq worker │
                          └─────────┘          │ Whisper+Praat│
                                               └──────────────┘
                                               
```
- MinIO хранит: записи пользователя, эталонные TTS, спектрограммы.
- Redis — брокер очереди для тяжёлых задач ASR/анализа.
- arq worker — отдельный процесс с моделями Whisper и Piper в памяти.

---

## Доменная модель

### Иерархия обучения
```bash
Course ─┬── Module ─┬── Exercise ─┬── Task (отдельное слово/фраза)
        │           │             └── Reference audio (URL в MinIO)
        │           └── FinalCheck (предложение для контрольной точки)
        └── ...
```
### Основные сущности
- User — учётка, родной язык (для подбора курса/советов).
- Course — целевой акцент или подбор «РЯ → English».
- Module — группа фонем (`/æ/ vs /ʌ/`, θ/ð, r-coloring, …).
- Exercise — конкретная задача (слово / минимальная пара).
- Task — атомарная единица записи внутри упражнения.
- Attempt — одна попытка пользователя со всем анализом.
- PhonemeReport — отчёт по конкретной фонеме внутри попытки.
- Progress — агрегированный прогресс по модулю/курсу.


### Value Objects
- Formants — f1: float, f2: float, f3: float, time_ms: int.
- Mfcc — массив коэффициентов.
- Phoneme — символ ARPAbet/IPA + дескрипторы (vowel/consonant, voicing, …).
- TonguePosition — height: float (0..1), frontness: float (0..1),
  вычисляется из формант для отображения на схеме рта.

---

## Обоснование ключевых решений

| Решение | Причина |
|---|---|
| FastAPI | Async, OpenAPI из коробки, отличная DI-модель |
| faster-whisper | Кросс-платформенно (CUDA на RTX 3080 + Metal на M4), быстрее vanilla Whisper в 4-6 раз |
| parselmouth (Praat) | Стандарт де-факто в фонетике для извлечения формант |
| Piper TTS | Оффлайн, быстрый, естественный, ONNX runtime (нативно работает на M-серии) |
| MinIO | S3-совместимый API → код легко портируется в облако |
| arq | Лёгкая альтернатива Celery, чисто async, простая интеграция с FastAPI |
| Clean Architecture | Тестируемость, замена ASR-провайдера без рефакторинга |
| Hillenbrand vowel data | Открытый эталонный датасет F1/F2/F3 для гласных American English |

---

## Тестирование

- unit-тесты — domain и application слои, моки портов
- integration-тесты — api + реальная БД в Docker
- аудио fixtures — короткие WAV-сэмплы в backend/tests/integration/fixtures/