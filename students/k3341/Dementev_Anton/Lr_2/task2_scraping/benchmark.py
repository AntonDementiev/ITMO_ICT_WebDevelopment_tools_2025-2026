import asyncio

from db import clear_pages, init_db

WORKERS = 4


def main():
    init_db()

    print("=== Бенчмарк парсинга ===\n")

    clear_pages()
    from threading_scraper import run as t_run
    from urls import URLS
    time_t = t_run(URLS, WORKERS)
    print(f"\nthreading:       {time_t:.3f} с\n")

    clear_pages()
    from multiprocessing_scraper import run as m_run
    time_m = m_run(URLS, WORKERS)
    print(f"\nmultiprocessing: {time_m:.3f} с\n")

    clear_pages()
    from async_scraper import run as a_run
    time_a = asyncio.run(a_run(URLS))
    print(f"\nasync:           {time_a:.3f} с\n")

    print("Итого:")
    print(f"  threading:       {time_t:.3f} с")
    print(f"  multiprocessing: {time_m:.3f} с")
    print(f"  async:           {time_a:.3f} с")


if __name__ == "__main__":
    main()
