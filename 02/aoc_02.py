#! /usr/bin/env python

puzzle_input = []
with open("puzzle.txt") as input_file:
    for line in input_file.read().split('\n'):
        puzzle_input.append([int(i) for i in line.split()])


def is_safe(line):
    direction = []
    for i in range(len(line)-1):
        if abs(line[i] - line[i+1]) > 3:
            return False
        if abs(line[i] - line[i+1]) == 0:
            return False
        if line[i] > line[i+1]:
            direction.append(-1)
        if line[i] < line[i+1]:
            direction.append(1)
        if line[i] == line[i+1]:
            direction.append(0)
        if len(set(direction)) != 1:
            return False
    return True


def is_safe_dampened(line):
    valid = []
    variations = [line]

    for i in range(len(line)):
        new_line = line.copy()
        new_line.pop(i)
        variations.append(new_line)

    for v in variations:
        valid.append(is_safe(v))

    if True in valid:
        return True
    return False


part_1 = 0
part_2 = 0
for line in puzzle_input:
    if is_safe(line):
        part_1 += 1
    if is_safe_dampened(line):
        part_2 += 1
print(f"part 1: {part_1}\npart 2: {part_2}")
