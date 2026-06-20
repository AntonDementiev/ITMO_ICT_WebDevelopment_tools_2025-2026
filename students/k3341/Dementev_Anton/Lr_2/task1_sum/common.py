TARGET_N = 10 ** 13
DEFAULT_N = 100_000_000


def split_ranges(n: int, parts: int) -> list[tuple[int, int]]:
    parts = max(1, parts)
    chunk = n // parts
    ranges: list[tuple[int, int]] = []
    start = 1
    for i in range(parts):
        end = n if i == parts - 1 else start + chunk - 1
        ranges.append((start, end))
        start = end + 1
    return ranges


def expected_sum(n: int) -> int:
    return n * (n + 1) // 2
