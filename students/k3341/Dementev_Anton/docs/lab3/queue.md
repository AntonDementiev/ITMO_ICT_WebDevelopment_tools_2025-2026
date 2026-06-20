# Очередь Celery (Redis)

## Архитектура

```
Клиент → FastAPI (web) → Redis → Celery Worker → БД
```

1. Клиент отправляет `POST /parser/parse-async?url=...`
2. FastAPI ставит задачу `parse_url_task` в очередь Redis через Celery
3. Celery worker забирает задачу, парсит страницу, сохраняет в БД
4. Клиент проверяет статус через `GET /parser/result/{task_id}`

## Конфигурация Celery

```python
celery_app = Celery("lab3", broker=BROKER_URL, backend=RESULT_BACKEND)

@celery_app.task(name="parse_url")
def parse_url_task(url: str) -> dict:
    # загрузить страницу, извлечь title, сохранить в БД
    ...
```

## Асинхронный вызов

```python
@router.post("/parse-async")
def parse_async(url: str = Query(...)):
    task = parse_url_task.delay(url)
    return {"task_id": task.id, "status": "queued"}
```

## Проверка результата

```python
@router.get("/result/{task_id}")
def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": result.status, "result": result.result}
```

## Периодические задачи (Celery Beat)

Каждые 2 минуты автоматически парсится `https://example.com`:

```python
celery_app.conf.beat_schedule = {
    "parse-example-every-2-minutes": {
        "task": "parse_url",
        "schedule": 120.0,
        "args": ("https://example.com",),
    }
}
```

## Запуск

```bash
docker compose up --build
```

Все сервисы (web, parser, redis, worker, beat) запускаются автоматически.
