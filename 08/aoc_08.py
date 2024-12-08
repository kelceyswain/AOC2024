#! /usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, d: int):
        return Point(self.x * d, self.y * d)

    # We will need to know if points are equal
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Point(self.x, self.y)

    # We are going to borrow __floordiv__ to
    # calculate the antinode of two Points
    def __floordiv__(self, other):
        dif = other - self
        return other + dif

    def in_range(self, top_left, bottom_right):
        if self.x < top_left.x:
            return False
        if self.x > bottom_right.x:
            return False
        if self.y < top_left.y:
            return False
        if self.y > bottom_right.y:
            return False
        return True


class Frequency:
    def __init__(self):
        self._antennae = []
        self._antinodes = []

    def __repr__(self):
        outstring = "Antennae: "
        for a in self._antennae:
            outstring += str(a)
            outstring += ' '
        outstring += "\n"
        outstring += "Antinodes: "
        for a in self._antinodes:
            outstring += str(a)
            outstring += ' '
        outstring += '\n'
        return outstring

    def add_antenna(self, antenna):
        for a in self._antennae:
            antinode_a = antenna // a
            antinode_b = a // antenna
            if antinode_a not in self._antinodes:
                self._antinodes.append(antinode_a)
            if antinode_b not in self._antinodes:
                self._antinodes.append(antinode_b)
        self._antennae.append(antenna)

    def add_antenna_2(self, antenna, origin: Point, range: Point):
        # This time we add the antenna itself
        if antenna not in self._antinodes:
            self._antinodes.append(antenna)
        for a in self._antennae:
            cursor_1 = antenna.copy()
            cursor_2 = a.copy()
            if cursor_1 == cursor_2:
                continue
            in_range = True
            while in_range:
                antinode_a = cursor_1 // cursor_2
                if not antinode_a.in_range(origin, range):
                    in_range = False
                elif antinode_a not in self._antinodes:
                    self._antinodes.append(antinode_a)
                cursor_1, cursor_2 = cursor_2, antinode_a
            # Now go the other way
            cursor_1 = antenna.copy()
            cursor_2 = a.copy()
            if cursor_1 == cursor_2:
                continue
            in_range = True
            while in_range:
                antinode_a = cursor_2 // cursor_1
                if not antinode_a.in_range(origin, range):
                    in_range = False
                elif antinode_a not in self._antinodes:
                    self._antinodes.append(antinode_a)
                cursor_1, cursor_2 = antinode_a, cursor_1
        self._antennae.append(antenna)

    @property
    def antennae(self):
        return self._antennae

    @property
    def antinodes(self):
        return self._antinodes


if __name__ == "__main__":
    frequencies = {}
    antinodes = []

    top_left = Point(0, 0)
    max_x = 0
    max_y = 0
    input_file = "./puzzle.txt"
    with open(input_file) as puzzle_file:
        for y, line in enumerate(puzzle_file.readlines()):
            if y > max_y:
                max_y = y
            for x, char in enumerate(line):
                if x > max_x:
                    max_x = x
                if char not in ['.', '\n']:
                    p = Point(x, y)
                    # Add a new Frequency if it isn't there
                    # then add the antenna
                    frequencies.setdefault(char, Frequency()).add_antenna(p)
    # readlines is making this count the new line as a char, so remove one
    max_x -= 1
    bottom_right = Point(max_x, max_y)
    for key in frequencies:
        for a in frequencies[key].antinodes:
            if a.in_range(top_left, bottom_right):
                antinodes.append(a)
        # print(f"Frequency: {key}\n{frequencies[key]}")
    print(f"Part 1: {len(set(antinodes))}")

    # Part 2
    frequencies_2 = {}
    antinodes_2 = []
    with open(input_file) as puzzle_file:
        for y, line in enumerate(puzzle_file.readlines()):
            for x, char in enumerate(line):
                if char not in ['.', '\n']:
                    p = Point(x, y)
                    frequencies_2.setdefault(
                        char,
                        Frequency()).add_antenna_2(
                            p,
                            top_left,
                            bottom_right
                        )
    for key in frequencies_2:
        for a in frequencies_2[key].antinodes:
            if a.in_range(top_left, bottom_right):
                antinodes_2.append(a)
        # print(f"Frequency: {key}\n{frequencies_2[key]}")
    print(f"Part 2: {len(set(antinodes_2))}")
