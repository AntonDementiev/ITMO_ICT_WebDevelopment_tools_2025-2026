import argparse
import threading
import time

from common import DEFAULT_N, expected_sum, split_ranges


def calculate_sum(start: int, end: int, results: list, index: int) -> None:
    total = 0
    for value in range(start, end + 1):
        total += value
    results[index] = total


def run(n: int, workers: int) -> tuple[int, float]:
    ranges = split_ranges(n, workers)
    results = [0] * len(ranges)
    threads = []

    start_time = time.perf_counter()
    for idx, (start, end) in enumerate(ranges):
        t = threading.Thread(target=calculate_sum, args=(start, end, results, idx))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    total = sum(results)
    elapsed = time.perf_counter() - start_time
    return total, elapsed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    total, elapsed = run(args.n, args.workers)
    check = expected_sum(args.n)
    print(f"[threading] N={args.n}, потоков={args.workers}")
    print(f"  сумма    = {total}")
    print(f"  контроль = {check} ({'OK' if total == check else 'ОШИБКА'})")
    print(f"  время    = {elapsed:.3f} с")
