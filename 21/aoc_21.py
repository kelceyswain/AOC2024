#! /usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict, Set

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def buttons(self):
        output_hv = []
        if self.x < 0:
            for i in range(abs(self.x)):
                output_hv.append("<")
        else:
            for i in range(self.x):
                output_hv.append(">")
        if self.y < 0:
            for i in range(abs(self.y)):
                output_hv.append("^")
        else:
            for i in range(self.y):
                output_hv.append("v")
        output_hv.append("A")
        output_vh = []
        if self.y < 0:
            for i in range(abs(self.y)):
                output_vh.append("^")
        else:
            for i in range(self.y):
                output_vh.append("v")
        if self.x < 0:
            for i in range(abs(self.x)):
                output_vh.append("<")
        else:
            for i in range(self.x):
                output_vh.append(">")
        output_vh.append("A")
        return (output_hv, output_vh)


class Keypad:
    def __init__(self, keys, buttons=[]):
        self.buttons = buttons
        self.keys = keys
        self.perform = []
        self.valid_points = set(keys.values())

    def find_route(self, start, end):
        route = self.keys[end] - self.keys[start]
        return route.buttons()[0]

    def run(self):
        output = []
        self.buttons.insert(0, "A")
        for i in range(len(self.buttons) - 1):
            output.extend(self.find_route(self.buttons[i], self.buttons[i+1]))
        return output


class Codepad(Keypad):
    def __init__(self, *args, **kwargs):
        keys = {
            "A": Point(2, 3),
            "0": Point(1, 3),
            "1": Point(0, 2),
            "2": Point(1, 2),
            "3": Point(2, 2),
            "4": Point(0, 1),
            "5": Point(1, 1),
            "6": Point(2, 1),
            "7": Point(0, 0),
            "8": Point(1, 0),
            "9": Point(2, 0)
        }
        super(Codepad, self).__init__(keys, *args, **kwargs)


class Robot(Keypad):
    def __init__(self, *args, **kwargs):
        keys = {
            "A": Point(2, 0),
            "^": Point(1, 0),
            "<": Point(0, 1),
            "v": Point(1, 1),
            ">": Point(2, 1)
        }
        super(Robot, self).__init__(keys, *args, **kwargs)


if __name__ == "__main__":
    part_1 = 0
    with open("test.txt") as puzzle_file:
        puzzle_text = puzzle_file.readlines()
    for row in puzzle_text:
        num = int(row[0:3])
        code = list(row[0:4])
        k = Codepad(code)
        r1 = Robot(k.run())
        r2 = Robot(r1.run())
        me = r2.run()
        print(f"{len(me)} * {num}")
        part_1 += len(me) * num
    print(part_1)

code = ["1", "7", "9", "A"]
k = Codepad(code)
r1 = Robot(k.run())
#r2 = Robot(r1.run())
print(r1.run())
