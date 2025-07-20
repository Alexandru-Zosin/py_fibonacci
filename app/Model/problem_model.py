# models.py

class PowerOperation:
    def __init__(self, base: int, exponent: int):
        self.base = base
        self.exponent = exponent

    def compute(self) -> int:
        return self.base ** self.exponent


class FibonacciOperation:
    def __init__(self, n: int):
        self.n = n

    def compute(self) -> int:
        a, b = 0, 1
        for _ in range(self.n):
            a, b = b, a + b
        return a


class FactorialOperation:
    def __init__(self, n: int):
        self.n = n

    def compute(self) -> int:
        result = 1
        for i in range(2, self.n + 1):
            result *= i
        return result
 