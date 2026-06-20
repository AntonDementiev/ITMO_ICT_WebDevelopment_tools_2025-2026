# Задача 1 — CPU-bound: сумма чисел

## Описание

Вычислить сумму всех чисел от 1 до N (целевое N = 10^13, практическое для замеров N = 10^8). Диапазон разбивается на части, каждая обрабатывается параллельно.

## Threading

Используется модуль `threading`. Каждый поток суммирует свою часть диапазона. Из-за GIL реального ускорения для CPU-bound задач нет — потоки выполняются по очереди.

```python
def calculate_sum(start, end, results, index):
    total = 0
    for value in range(start, end + 1):
        total += value
    results[index] = total
```

## Multiprocessing

Модуль `multiprocessing` создаёт отдельные процессы, каждый со своим GIL. Для CPU-bound задач это даёт реальное ускорение пропорционально числу ядер.

```python
with Pool(processes=workers) as pool:
    partials = pool.starmap(calculate_sum, ranges)
```

## Async

`asyncio.gather` запускает корутины. Для CPU-bound кода без I/O-операций это эквивалентно последовательному выполнению — async предназначен для I/O-bound задач.

## Запуск

```bash
cd Lr_2/task1_sum
python benchmark.py
```
