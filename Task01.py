import random
import time
from functools import lru_cache

# Функція для обчислення суми на відрізку без використання кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

# Функція для оновлення значення в масиві без використання кешу
def update_no_cache(array, index, value):
    array[index] = value

# Використовуємо LRU-кеш для збереження результатів запитів на суму
@lru_cache(maxsize=1000)
def range_sum_with_cache(array, L, R):
    return sum(array[L:R+1])

# Функція для оновлення значення в масиві з видаленням з кешу
def update_with_cache(array, index, value):
    array[index] = value
    # Очищаємо кеш після оновлення масиву
    range_sum_with_cache.cache_clear()

# Тестування продуктивності
def test_performance():
    N = 100_000
    Q = 50_000
    array = [random.randint(1, 1000) for _ in range(N)]
    queries = [('Range', random.randint(0, N-1), random.randint(0, N-1)) if random.random() < 0.7 else ('Update', random.randint(0, N-1), random.randint(1, 1000)) for _ in range(Q)]

    unique_queries = set()

    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(array, min(query[1], query[2]), max(query[1], query[2]))
            unique_queries.add((query[0], min(query[1], query[2]), max(query[1], query[2])))
        elif query[0] == 'Update':
            update_no_cache(array, query[1], query[2])
            unique_queries.add((query[0], query[1], query[2]))
    no_cache_duration = time.time() - start_time

    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(tuple(array), min(query[1], query[2]), max(query[1], query[2]))
            unique_queries.add((query[0], min(query[1], query[2]), max(query[1], query[2])))
        elif query[0] == 'Update':
            update_with_cache(array, query[1], query[2])
            unique_queries.add((query[0], query[1], query[2]))
    with_cache_duration = time.time() - start_time

    print(f"Без кешу: {no_cache_duration:.2f} секунд")
    print(f"З кешем: {with_cache_duration:.2f} секунд")
    print(f"Кількість унікальних запитів: {len(unique_queries)} з {Q} запитів всього")

if __name__ == "__main__":
    test_performance()
