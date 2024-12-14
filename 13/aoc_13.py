import re
from dataclasses import dataclass
from math import gcd


def extended_gcd(a, b):
    """Extended Euclidean algorithm to find x, y such that a*x + b*y = gcd(a, b)."""
    if b == 0:
        return (a, 1, 0)  # gcd, x, y
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y


@dataclass
class Push:
    x: int
    y: int

    def gcd(self, other):
        gcd_x = gcd(self.x, other.x)
        gcd_y = gcd(self.y, other.y)
        return Push(gcd_x, gcd_y)

    def __add__(self, other):
        return Push(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Push(self.x - other.x, self.y - other.y)

    def __floordiv__(self, other):
        return Push(self.x // other.x, self.y // other.y)

    def __mul__(self, n):
        return Push(self.x * n, self.y * n)

    def __mod__(self, other):
        return Push(self.x % other.x, self.y % other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class ClawGame:
    def __init__(self, target: Push, a: Push, b: Push):
        self.target = target
        self.a = a
        self.b = b
        self.pairs = self.find_pairs()

    def cost(self):
        cost = []
        if self.pairs:
            for p in self.pairs:
                if p[0] <= 100 and p[1] <= 100:
                    cost.append(p[0] * 3 + p[1])
        if cost:
            print(min(cost))
            return min(cost)
        return 0

    def cost2(self):
        cost = []
        if self.pairs:
            for p in self.pairs:
                cost.append(p[0] * 3 + p[1])
        if cost:
            print(min(cost))
            return min(cost)
        return 0

    def find_pairs(self):
        pairs = []
        # To solve without brute force we need to do some funky
        # Euclid stuff.
        gcd_x, x_coeff, y_coeff = extended_gcd(self.a.x, self.b.x)
        gcd_y, _, _ = extended_gcd(self.a.y, self.b.y)

        if self.target.x % gcd_x != 0 or self.target.y % gcd_y != 0:
            # No solution
            return []

        # Scale the initial solution
        scale_x = self.target.x // gcd_x
        x_base = x_coeff * scale_x
        y_base = y_coeff * scale_x

        # Fundamental solution transform
        def generate_solution(k):
            return (
                x_base + k * (self.b.x // gcd_x),
                y_base - k * (self.a.x // gcd_x)
            )

        # search for solution starting at k=0 and going out both positive and negative
        k = 0
        while True:
            m, n = generate_solution(k)
            if m >= 0 and n >= 0:
                pairs.append((m, n))
            if k > 100000:
                break
            elif k >= 0:
                k = (k + 1) * -1
            else:
                k = k * -1
        return pairs


if __name__ == "__main__":
    part_1 = 0
    part_2 = 0
    m_pat = re.compile(r"Button (\w): X\+(\d+), Y\+(\d+)")
    t_pat = re.compile(r"Prize: X=(\d+), Y=(\d+)")
    with open("./test.txt", 'r') as puzzle_file:
        puzzle_text = puzzle_file.read()
    for game in puzzle_text.split("\n\n"):
        a, b = m_pat.findall(game)
        t = t_pat.findall(game)
        a_push = Push(int(a[1]), int(a[2]))
        b_push = Push(int(b[1]), int(b[2]))
        target = Push(int(t[0][0]), int(t[0][1]))
        game = ClawGame(target, a_push, b_push)
        part_1 += game.cost()
    print(f"Part 1: {part_1}")

    for game in puzzle_text.split("\n\n"):
        a, b = m_pat.findall(game)
        t = t_pat.findall(game)
        a_push = Push(int(a[1]), int(a[2]))
        b_push = Push(int(b[1]), int(b[2]))
        target = Push(int(t[0][0])+10000000000000, int(t[0][1])+10000000000000)
        game = ClawGame(target, a_push, b_push)
        part_2 += game.cost2()
    print(f"Part 2: {part_2}")
