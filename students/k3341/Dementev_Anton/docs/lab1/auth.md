# Аутентификация (JWT)

## Механизм

1. Пользователь регистрируется через `POST /auth/register` — пароль хешируется bcrypt.
2. Для входа `POST /auth/token` принимает `username`/`password` (OAuth2 form), проверяет хеш и возвращает JWT access-токен.
3. Защищённые эндпоинты используют зависимость `get_current_user`, которая извлекает токен из заголовка `Authorization: Bearer <token>`, декодирует его и возвращает пользователя из БД.

## Генерация токена

```python
def create_access_token(subject: str | int, expires_delta=None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=60))
    return jwt.encode({"sub": str(subject), "exp": expire}, SECRET_KEY, algorithm="HS256")
```

## Хеширование паролей

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

## Swagger UI

FastAPI автоматически генерирует кнопку «Authorize» в Swagger UI. После ввода логина и пароля все последующие запросы отправляются с токеном.
