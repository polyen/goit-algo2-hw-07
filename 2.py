import timeit
from functools import lru_cache
from splay_tree import SplayTree
import matplotlib.pyplot as plt


def plot_comparison(lru_time, splay_time):
    plt.figure(figsize=(12, 6))
    plt.plot(list(lru_time.keys()), list(lru_time.values()), label='LRU Cache', marker='o')
    plt.plot(list(splay_time.keys()), list(splay_time.values()), label='Splay Tree', marker='x')

    plt.title('Comparison of Fibonacci Calculation Methods')
    plt.xlabel('Fibonacci Number (n)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.xticks(list(lru_time.keys()))
    plt.show()

def table_comparison(lru_time, splay_time):
    print(f"{'Fibonacci Number':<20} {'LRU Cache Time (s)':<20} {'Splay Tree Time (s)':<20}")
    print("=" * 60)
    for n in lru_time.keys():
        print(f"{n:<20} {lru_time[n]:<20.6f} {splay_time[n]:<20.6f}")

@lru_cache(maxsize=1000)
def fibonacci_lru(n):
    """Обчислює n-ий член послідовності Фібоначчі з використанням LRU кешування."""
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n):
    """Обчислює n-ий член послідовності Фібоначчі з використанням splay-дерева."""
    tree = SplayTree()

    def fib(n):
        if n <= 1:
            return n
        if n not in tree:
            tree.insert(n, fib(n - 1) + fib(n - 2))
        return tree.find(n)

    return fib(n)


if __name__ == '__main__':
    values = [i * 50 for i in range(1, 19)]

    lru_time = {}
    splay_time = {}

    for n in values:
        lru_time[n] = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        splay_time[n] = timeit.timeit(lambda: fibonacci_splay(n), number=1)

    plot_comparison(lru_time, splay_time)
    table_comparison(lru_time, splay_time)

print('''Висновок: LRU кешування та splay дерево демонструють різні підходи до оптимізації обчислень. 
LRU кешування ефективно зберігає результати для повторних запитів, тоді як splay дерево забезпечує 
швидкий доступ до часто використовуваних елементів, але може бути менш ефективним для великих значень n 
через накладні витрати на балансування дерева.''')