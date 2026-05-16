# Setup

## Пререквизиты

| Инструмент | Версия | Установка (macOS, brew) |
|---|---|---|
| Python | 3.11+ | brew install python@3.11 |
| uv | latest | brew install uv или curl -LsSf https://astral.sh/uv/install.sh \| sh |
| Node.js | 20+ | brew install node@20 |
| Docker | latest | [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| ffmpeg | latest | brew install ffmpeg |
| git | latest | brew install git |

> ⚠️ Apple Silicon (M4): Docker Desktop должен быть в режиме
> Use Rosetta for x86/amd64 emulation — для совместимости с некоторыми
> образами. Для нативных контейнеров используется arm64.

---

## Клонирование и переменные окружения
```bash
git clone <repo-url> accent-trainer
cd accent-trainer
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
Отредактируй значения под себя (пароли, порты).
 ```
---

## Запуск инфраструктуры (Postgres + Redis + MinIO)

> Будет добавлено в следующем этапе (`feature/infra-compose`).

Превью команды:
`docker compose up -d postgres redis minio`
---

## Установка backend

> Будет добавлено в feature/backend-core.

Превью:
```bash
cd backend
uv sync                       # установит зависимости из pyproject.toml
uv run alembic upgrade head   # применит миграции
uv run uvicorn accent_trainer.main:app --reload
```
---

## Установка frontend

> Будет добавлено в feature/frontend-skeleton.

Превью:
```bash
cd frontend
npm install
npm run dev
```
---

## Проверка

| URL | Что |
|---|---|
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/api/v1/health | Healthcheck |
| http://localhost:5173 | Frontend |
| http://localhost:9001 | MinIO console |

---

## Troubleshooting

### M4 / arm64
- faster-whisper использует CTranslate2. Установится с CPU-поддержкой
  автоматически; для Metal-ускорения проверь, что у PyTorch backend = MPS:
import torch; print(torch.backends.mps.is_available())
- parselmouth имеет нативные arm64-wheels, проблем быть не должно.

### Windows / CUDA (RTX 3080)
- faster-whisper с CUDA 12: uv pip install ctranslate2 --reinstall
  и убедиться, что NVIDIA cuDNN установлен.
- Docker Desktop с WSL2.