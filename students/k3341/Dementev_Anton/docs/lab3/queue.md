# Celery + Redis
Асинхронная очередь: POST /parser/parse-async ставит задачу, worker обрабатывает, GET /parser/result/{id} — статус.
Периодические задачи через Celery Beat.
