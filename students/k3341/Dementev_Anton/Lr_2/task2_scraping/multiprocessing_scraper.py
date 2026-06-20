import argparse
import time
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

from db import count_pages, init_db, save_page
from urls import URLS

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Lab2Scraper/1.0)"}
APPROACH = "multiprocessing"


def parse_and_save(url: str) -> str | None:
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "(без заголовка)"
        )
        save_page(url, title, APPROACH)
        print(f"[{APPROACH}] {url} -> {title}")
        return title
    except Exception as exc:
        print(f"[{APPROACH}] ОШИБКА {url}: {exc}")
        return None


def run(urls: list[str], workers: int) -> float:
    start_time = time.perf_counter()
    with Pool(processes=workers) as pool:
        pool.map(parse_and_save, urls)
    return time.perf_counter() - start_time


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    init_db()
    elapsed = run(URLS, args.workers)
    print(f"\n[multiprocessing] страниц={len(URLS)}, процессов={args.workers}, время={elapsed:.3f} с")
    print(f"строк в parsed_page: {count_pages()}")
