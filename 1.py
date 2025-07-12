import random
from lru_utils import LRUCache
import timeit


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n // 2), random.randint(n // 2, n - 1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% запитів — Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% — Range
            if random.random() < p_hot:  # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:  # 5% — випадкові діапазони
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


def range_sum_no_cache(arr, left, right):
    return sum(arr[left:right + 1])


def range_sum_with_cache(arr, left, right, cache):
    cache_key = (left, right)

    if cache.get(cache_key) == -1:
        result = sum(arr[left:right + 1])
        cache.put(cache_key, result)
        return result
    else:
        return cache.get(cache_key)


def update_no_cache(array, index, value):
    array[index] = value


def update_with_cache(array, index, value, cache):
    array[index] = value

    for cache_entry in list(cache.cache.keys()):
        if cache_entry[0] <= index <= cache_entry[1]:
            del cache.cache[cache_entry]
            # No need to remove from the linked list, as it will be expired

def handle_queries_with_cache(arr, queries, cache):
    for query in queries:
        if query[0] == "Update":
            update_with_cache(arr, query[1], query[2], cache)
        elif query[0] == "Range":
            range_sum_with_cache(arr, query[1], query[2], cache)


def handle_queries_no_cache(arr, queries):
    for query in queries:
        if query[0] == "Update":
            update_no_cache(arr, query[1], query[2])
        elif query[0] == "Range":
            range_sum_no_cache(arr, query[1], query[2])


if __name__ == '__main__':
    n = 100_000
    q = 50_000

    queries = make_queries(n, q)

    arr = [random.randint(1, 100) for _ in range(n)]

    cache = LRUCache(1000)

    no_cache_time = timeit.timeit(lambda: handle_queries_no_cache(arr, queries), number=1)
    print(f"Без кешу : {no_cache_time:.4f} c")

    cache_time = timeit.timeit(lambda: handle_queries_with_cache(arr, queries, cache), number=1)
    print(f"LRU-кеш  : {cache_time:.4f} c  (Прискорення: x {no_cache_time / cache_time:.2f})")
