import random


class ValueCycle:

    def __init__(self, a: int, b: int, step: int):
        self.a = a
        self.b = b
        self.step = abs(step)

        self.direction = 1 if self.b > self.a else -1
        self.current_value = self.a

    def reset(self) -> None:
        self.direction = 1 if self.b > self.a else -1
        self.current_value = self.a

    def set_random_value(self):
        self.direction = random.choice([-1, 1])
        d = abs(self.a - self.b)
        min_value = min(self.a, self.b)
        n = d // self.step

        self.current_value = round(min_value + random.randint(0, n) * self.step)

    def __iter__(self):
        return self

    def __next__(self) -> int:
        result = self.current_value

        if not (self.a <= self.current_value + self.step * self.direction <= self.b):
            self.direction *= -1

        self.current_value += self.step * self.direction

        return result
