# ЛР2 — Потоки, процессы, асинхронность

## Цель

Понять отличия между потоками (threading), процессами (multiprocessing) и асинхронностью (asyncio) в Python.

## Задачи

1. **CPU-bound задача** — подсчёт суммы чисел от 1 до N тремя подходами.
2. **I/O-bound задача** — параллельный парсинг веб-страниц с сохранением в БД.

## Стек

- Python 3.11+
- threading, multiprocessing, asyncio
- requests / aiohttp
- BeautifulSoup
- PostgreSQL (psycopg2 / asyncpg)
