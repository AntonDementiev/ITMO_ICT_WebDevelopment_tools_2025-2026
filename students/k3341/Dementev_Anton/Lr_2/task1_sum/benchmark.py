import asyncio
import time

from common import DEFAULT_N, expected_sum, split_ranges

N = DEFAULT_N
WORKERS = 8


def main():
    print(f"Бенчмарк: сумма 1..{N}, воркеров={WORKERS}\n")

    from threading_sum import run as threading_run
    total_t, time_t = threading_run(N, WORKERS)
    print(f"threading:       {time_t:.3f} с (сумма={'OK' if total_t == expected_sum(N) else 'ERR'})")

    from multiprocessing_sum import run as mp_run
    total_m, time_m = mp_run(N, WORKERS)
    print(f"multiprocessing: {time_m:.3f} с (сумма={'OK' if total_m == expected_sum(N) else 'ERR'})")

    from async_sum import run as async_run
    total_a, time_a = asyncio.run(async_run(N, WORKERS))
    print(f"async:           {time_a:.3f} с (сумма={'OK' if total_a == expected_sum(N) else 'ERR'})")

    print(f"\nИтого:")
    print(f"  threading:       {time_t:.3f} с")
    print(f"  multiprocessing: {time_m:.3f} с")
    print(f"  async:           {time_a:.3f} с")


if __name__ == "__main__":
    main()
