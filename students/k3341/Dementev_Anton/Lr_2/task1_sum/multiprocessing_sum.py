import argparse
import time
from multiprocessing import Pool

from common import DEFAULT_N, expected_sum, split_ranges


def calculate_sum(start: int, end: int) -> int:
    total = 0
    for value in range(start, end + 1):
        total += value
    return total


def run(n: int, workers: int) -> tuple[int, float]:
    ranges = split_ranges(n, workers)
    start_time = time.perf_counter()
    with Pool(processes=workers) as pool:
        partials = pool.starmap(calculate_sum, ranges)
    total = sum(partials)
    elapsed = time.perf_counter() - start_time
    return total, elapsed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    total, elapsed = run(args.n, args.workers)
    check = expected_sum(args.n)
    print(f"[multiprocessing] N={args.n}, процессов={args.workers}")
    print(f"  сумма    = {total}")
    print(f"  контроль = {check} ({'OK' if total == check else 'ОШИБКА'})")
    print(f"  время    = {elapsed:.3f} с")
