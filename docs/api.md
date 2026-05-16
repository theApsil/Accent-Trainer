# API Reference

> Документ заполняется по мере разработки эндпоинтов.
> Источник правды — автогенерируемая Swagger UI: http://localhost:8000/docs.

---

## Базовый URL
http://localhost:8000/api/v1
## Аутентификация

JWT Bearer. Получить токен:
POST /auth/login
Использовать в заголовке:
Authorization: Bearer <token>
---

## Планируемые группы эндпоинтов

| Группа | Префикс | Назначение |
|---|---|---|
| Auth | /auth | Регистрация, логин, refresh |
| Users | /users | Профиль текущего пользователя |
| Courses | /courses | Список курсов и детали |
| Modules | /modules | Модули внутри курса |
| Exercises | /exercises | Упражнения и задания |
| Attempts | /attempts | Создание попытки, получение анализа |
| Progress | /progress | Прогресс по курсам/модулям |
| Reference | /reference | Эталонное аудио (pre-signed URL) |

Детальные схемы запросов/ответов будут заполняться по мере реализации
соответствующих ветвей roadmap.