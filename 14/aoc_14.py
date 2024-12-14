#! /usr/bin/env python3

import re
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Robot(Point):
    d_x: int
    d_y: int
    space: tuple[int, int] = (11, 7)

    def __str__(self):
        return f"Robot({self.x}, {self.y})"

    def move(self, n):
        x = (self.x + (self.d_x * n)) % self.space[0]
        y = (self.y + (self.d_y * n)) % self.space[1]
        return (x, y)

    def is_in_sector(self, sector: tuple[Point, Point]):
        if sector[0].x <= self.x < sector[1].x and sector[0].y <= self.y < sector[1].y:
            return True
        return False

    def position(self):
        return Point(self.x, self.y)


def part_1():
    size = (101, 103)
    with open("./puzzle.txt", 'r') as puzzle_file:
        puzzle_text = puzzle_file.read()
    r_pat = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

    nw = (Point(0, 0), Point(size[0] // 2, size[1] // 2))
    ne = (Point((size[0] // 2)+1,  0), Point(size[0], size[1] // 2))
    sw = (Point(0, (size[1] // 2)+1), Point(size[0] // 2, size[1]))
    se = (Point((size[0] // 2)+1, (size[1] // 2)+1), Point(size[0], size[1]))

    sectors = {nw: 0, ne: 0, sw: 0, se: 0}

    for line in puzzle_text.split('\n'):
        p_x, p_y, d_x, d_y = r_pat.findall(line)[0]
        r = Robot(
            int(p_x), int(p_y),
            int(d_x), int(d_y),
            size
        )
        r.x, r.y = r.move(100)

        for s in sectors.keys():
            if r.is_in_sector(s):
                sectors[s] += 1

    part_1 = 1
    for key in sectors:
        part_1 *= sectors[key]

    print(f"Part 1: {part_1}")


def draw(n, r, s):
    # Create an empty grid with the given width and height
    grid = [[' ' for _ in range(s[0])] for _ in range(s[1])]

    # Plot the objects on the grid
    for robot in r:
        # Ensure the coordinates are within bounds
        x, y = robot.move(n)
        grid[y][x] = '#'  # Use 'O' or any symbol to represent the object

    # Convert the grid into an ASCII drawing
    for row in grid:  # Reverse to make (0,0) bottom-left
        print(''.join(row))


def part_2():
    size = (101, 103)
    robots = []
    with open("./puzzle.txt", 'r') as puzzle_file:
        puzzle_text = puzzle_file.read()
    r_pat = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

    for line in puzzle_text.split('\n'):
        p_x, p_y, d_x, d_y = r_pat.findall(line)[0]
        r = Robot(
            int(p_x), int(p_y),
            int(d_x), int(d_y),
            size
        )
        robots.append(r)

    for i in range(7050, 7090):
        # 7083
        draw(i, robots, size)
        print(i)
        input()


if __name__ == "__main__":
    part = 1
    if part == 1:
        part_1()
    elif part == 2:
        part_2()
    else:
        pass
