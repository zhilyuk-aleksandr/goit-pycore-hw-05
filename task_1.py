from collections.abc import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """Створює функцію Фібоначчі з окремим кешем у замиканні."""
    cache = {}

    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n not in cache:
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))
    print(fib(15))
