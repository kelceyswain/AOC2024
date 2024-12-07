#! /usr/bin/env python3

from itertools import product


def possible_operators(result: int, operands: list[int], part=1):
    def add(n: int, m: int):
        return n + m

    def multiply(n: int, m: int):
        return n * m

    def concatenation(n: int, m: int):
        return int(str(n) + str(m))

    if part == 1:
        operators = [add, multiply]
    elif part == 2:
        operators = [add, multiply, concatenation]

    operator_combinations = set(product(operators, repeat=len(operands)-1))

    # print(result, operands)
    results = []

    for ops in operator_combinations:
        operands_new = operands.copy()
        # Take the first value as the initial running total
        init = operands_new.pop(0)
        for i, rest in enumerate(operands_new):
            # print(ops)
            init = ops[i](init, rest)
        results.append(init)

    if result in results:
        return True
    return False


if __name__ == "__main__":
    puzzle_input = {}
    part_1 = 0
    part_2 = 0
    with open("./puzzle.txt", 'r') as puzzle_file:
        for line in puzzle_file.readlines():
            result, operands = line.split(':')
            puzzle_input[int(result)] = [int(i) for i in operands.split()]
    for key in puzzle_input:
        if possible_operators(key, puzzle_input[key], part=1):
            part_1 += key
    print(f"Part 1: {part_1}")

    for key in puzzle_input:
        if possible_operators(key, puzzle_input[key], part=2):
            part_2 += key
    print(f"Part 2: {part_2}")
