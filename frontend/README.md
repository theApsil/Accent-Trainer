# Accent Trainer — Frontend

React SPA для записи речи, визуализации анализа и отслеживания прогресса.

## Стек
- React 18 + TypeScript
- Vite
- Tailwind CSS + shadcn/ui
- Zustand + TanStack Query
- wavesurfer.js, Recharts

## Структура (feature-sliced)
```bash
src/
├── api/         # HTTP-клиент + endpoints
├── features/    # auth, course, module, exercise, progress, final-test
├── shared/      # ui, hooks, lib, types, config
├── store/       # zustand
├── routes/      # роутинг + ProtectedRoute
└── styles/
```
## Локальный запуск

> Будет настроено в feature/frontend-skeleton.
```bash
npm install
npm run dev
```