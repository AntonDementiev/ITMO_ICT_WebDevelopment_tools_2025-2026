import os

import asyncpg
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/team_finder_db"
)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS parsed_page (
                    id         SERIAL PRIMARY KEY,
                    url        TEXT NOT NULL,
                    title      TEXT,
                    approach   TEXT,
                    parsed_at  TIMESTAMP DEFAULT now()
                );
                """
            )
        conn.commit()
    finally:
        conn.close()


def save_page(url: str, title: str, approach: str) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO parsed_page (url, title, approach) VALUES (%s, %s, %s);",
                (url, title, approach),
            )
        conn.commit()
    finally:
        conn.close()


def clear_pages() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE parsed_page RESTART IDENTITY;")
        conn.commit()
    finally:
        conn.close()


def count_pages() -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM parsed_page;")
            return cur.fetchone()[0]
    finally:
        conn.close()


async def create_async_pool() -> "asyncpg.Pool":
    return await asyncpg.create_pool(dsn=DATABASE_URL, min_size=1, max_size=10)


async def save_page_async(pool: "asyncpg.Pool", url: str, title: str, approach: str) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO parsed_page (url, title, approach) VALUES ($1, $2, $3);",
            url, title, approach,
        )
