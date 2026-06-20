# Docker и вызов парсера по HTTP

## Dockerfile (web)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
EXPOSE 8000
CMD ["sh", "entrypoint.sh"]
```

`entrypoint.sh` сначала применяет миграции, затем запускает uvicorn.

## Dockerfile (parser)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## Docker Compose

Все сервисы объединены в `docker-compose.yml`. БД PostgreSQL использует healthcheck, web и parser зависят от неё.

## Вызов парсера по HTTP

Эндпоинт `POST /parser/parse?url=...` в основном приложении отправляет запрос сервису-парсеру (http://parser:8001) и возвращает результат клиенту.

```python
@router.post("/parse")
def parse_via_service(url: str = Query(...)):
    response = requests.post(f"{PARSER_SERVICE_URL}/parse", params={"url": url})
    return response.json()
```

## Запуск

```bash
cd Lr_3
docker compose up --build
```
