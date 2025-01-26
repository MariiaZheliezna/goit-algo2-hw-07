import timeit
from functools import lru_cache
import matplotlib.pyplot as plt

# Функція з використанням LRU-кешу
@lru_cache(None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

# Реалізація Splay Tree
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def splay(self, root, key):
        if root is None or root.key == key:
            return root

        if root.key > key:
            if root.left is None:
                return root
            if root.left.key > key:
                root.left.left = self.splay(root.left.left, key)
                root = self.right_rotate(root)
            elif root.left.key < key:
                root.left.right = self.splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self.left_rotate(root.left)
            return root if root.left is None else self.right_rotate(root)
        else:
            if root.right is None:
                return root
            if root.right.key > key:
                root.right.left = self.splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self.right_rotate(root.right)
            elif root.right.key < key:
                root.right.right = self.splay(root.right.right, key)
                root = self.left_rotate(root)
            return root if root.right is None else self.left_rotate(root)

    def search(self, key):
        self.root = self.splay(self.root, key)
        if self.root is not None and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        self.root = self.splay(self.root, key)
        if self.root.key == key:
            return
        new_node = Node(key, value)
        if self.root.key > key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

def fibonacci_splay(n, tree):
    result = tree.search(n)
    if result is not None:
        return result
    if n < 2:
        return n
    result = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, result)
    return result

# Вимірювання часу виконання обчислень
def measure_time(func, *args):
    start = timeit.default_timer()
    result = func(*args)
    end = timeit.default_timer()
    return end - start, result

fib_numbers = list(range(0, 951, 50))
lru_times = []
splay_times = []

tree = SplayTree()

for n in fib_numbers:
    time_lru, _ = measure_time(fibonacci_lru, n)
    lru_times.append(time_lru)

    time_splay, _ = measure_time(fibonacci_splay, n, tree)
    splay_times.append(time_splay)

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(fib_numbers, lru_times, label='LRU Cache', marker='o')
plt.plot(fib_numbers, splay_times, label='Splay Tree', marker='x')
plt.xlabel('Fibonacci Number (n)')
plt.ylabel('Average Execution Time (seconds)')
plt.title('Fibonacci Computation: LRU Cache vs Splay Tree')
plt.legend()
plt.grid(True)
plt.show()

# Вивід таблиці
print(f"{'Fibonacci Number (n)':<20} {'LRU Cache Time (s)':<20} {'Splay Tree Time (s)':<20}")
for n, lru_time, splay_time in zip(fib_numbers, lru_times, splay_times):
    print(f"{n:<20} {lru_time:<20.6f} {splay_time:<20.6f}")