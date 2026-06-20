# Задача 2 — I/O-bound: парсинг веб-страниц

## Описание

Параллельный парсинг 12 веб-страниц с сохранением заголовков (`<title>`) в таблицу `parsed_page` базы данных из ЛР1.

## Threading

Список URL делится на части, каждый поток обрабатывает свою часть. Во время ожидания ответа от сервера Python освобождает GIL, поэтому потоки дают реальное ускорение для I/O-bound задач.

## Multiprocessing

Каждый процесс получает свой URL из пула. Работает, но накладные расходы на создание процессов могут быть заметны для небольшого числа страниц.

## Async (aiohttp)

Корутины с `aiohttp` + `asyncpg` — полностью неблокирующий парсинг и сохранение в БД. Наиболее эффективный подход для I/O-bound задач.

```python
async with aiohttp.ClientSession() as session:
    await asyncio.gather(*(parse_and_save(session, pool, url) for url in urls))
```

## Запуск

```bash
cd Lr_2/task2_scraping
python benchmark.py
```
