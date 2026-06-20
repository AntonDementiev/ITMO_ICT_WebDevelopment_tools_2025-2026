# Подключение к БД и миграции

## Подключение

Используется SQLModel (обёртка над SQLAlchemy) с драйвером `psycopg2-binary`. Строка подключения читается из переменной окружения `DATABASE_URL`.

```python
from sqlmodel import Session, SQLModel, create_engine
from app.core.config import settings

engine = create_engine(settings.database_url, echo=settings.db_echo)

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
```

## Миграции (Alembic)

Инициализация:

```bash
alembic upgrade head
```

Создание новой миграции:

```bash
alembic revision --autogenerate -m "описание изменений"
```

## Конфигурация

Настройки хранятся в `.env` (не коммитится) и читаются через `pydantic-settings`:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/team_finder_db
SECRET_KEY=super-secret-change-me-please
```
