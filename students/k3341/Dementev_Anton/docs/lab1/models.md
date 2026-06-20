# Модели и сущности

## ER-диаграмма

```
User 1──* Skill
User 1──* Project
Project 1──* Team
Team 1──* TeamMember *──1 User
```

## User

| Поле | Тип | Описание |
|------|-----|----------|
| id | int (PK) | Идентификатор |
| username | str (unique) | Логин |
| email | str (unique) | Email |
| full_name | str? | Полное имя |
| bio | text? | О себе |
| experience_years | int? | Опыт (лет) |
| hashed_password | str | Хеш пароля (bcrypt) |
| is_active | bool | Активен ли |
| created_at | datetime | Дата регистрации |

## Skill

| Поле | Тип | Описание |
|------|-----|----------|
| id | int (PK) | Идентификатор |
| name | str | Название навыка |
| level | str | Уровень (beginner/intermediate/advanced) |
| user_id | int (FK → User) | Владелец |

## Project

| Поле | Тип | Описание |
|------|-----|----------|
| id | int (PK) | Идентификатор |
| title | str | Название проекта |
| description | text? | Описание |
| status | str | Статус (open/in_progress/closed) |
| deadline | datetime? | Дедлайн |
| owner_id | int (FK → User) | Создатель |
| created_at | datetime | Дата создания |

## Team

| Поле | Тип | Описание |
|------|-----|----------|
| id | int (PK) | Идентификатор |
| name | str | Название команды |
| description | text? | Описание |
| project_id | int (FK → Project) | Проект |
| created_at | datetime | Дата создания |

## TeamMember

| Поле | Тип | Описание |
|------|-----|----------|
| id | int (PK) | Идентификатор |
| team_id | int (FK → Team) | Команда |
| user_id | int (FK → User) | Участник |
| role | str | Роль (member/lead) |
| joined_at | datetime | Дата присоединения |
