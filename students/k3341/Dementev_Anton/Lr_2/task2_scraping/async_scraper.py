import argparse
import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

from db import count_pages, create_async_pool, init_db, save_page_async
from urls import URLS

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Lab2Scraper/1.0)"}
APPROACH = "async"


async def parse_and_save(session: aiohttp.ClientSession, pool, url: str) -> str | None:
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            resp.raise_for_status()
            html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "(без заголовка)"
        )
        await save_page_async(pool, url, title, APPROACH)
        print(f"[{APPROACH}] {url} -> {title}")
        return title
    except Exception as exc:
        print(f"[{APPROACH}] ОШИБКА {url}: {exc}")
        return None


async def run(urls: list[str]) -> float:
    pool = await create_async_pool()
    start_time = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(parse_and_save(session, pool, url) for url in urls))
    await pool.close()
    return time.perf_counter() - start_time


if __name__ == "__main__":
    init_db()
    elapsed = asyncio.run(run(URLS))
    print(f"\n[async] страниц={len(URLS)}, время={elapsed:.3f} с")
    print(f"строк в parsed_page: {count_pages()}")
