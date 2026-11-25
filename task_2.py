import re
from collections.abc import Callable, Iterable, Iterator
from math import fsum


NUMBER = re.compile(r"(?<=\s)[+-]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?=\s)")


def generator_numbers(text: str) -> Iterator[float]:
    """Послідовно повертає числа, оточені пробільними символами."""
    for match in NUMBER.finditer(text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Iterable[float]]) -> float:
    """Підсумовує значення, які передана функція знаходить у тексті."""
    return fsum(func(text))


if __name__ == "__main__":
    text = "Загальний дохід становить 1000.01 доларів, ще 27.45 і 324.00 доларів."
    print(f"Загальний дохід: {sum_profit(text, generator_numbers):.2f}")
