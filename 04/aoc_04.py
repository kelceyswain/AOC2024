#! /usr/bin/env python3
from itertools import product


class WordSearch:
    def __init__(self, puzzle_matrix, word="XMAS"):
        self._puzzle = puzzle_matrix
        self._x_max = len(puzzle_matrix[0])
        self._y_max = len(puzzle_matrix)
        self._word = word
        self._count = 0

    def test_letter(self, letter_index, x, y, d):
        if letter_index == len(self._word):
            return True
        if x >= self._x_max or y >= self._y_max:
            return False
        if x < 0 or y < 0:
            return False
        if self._puzzle[y][x] == self._word[letter_index]:
            # print(f"({x},{y}) is good, moving to ({x+d[0]}, {y+d[1]})")
            r = self.test_letter(letter_index+1, x+d[0], y+d[1], d)
            if r:
                return True

    def test_xmas(self, x, y):
        letter = self._puzzle[x][y]
        if y != 0 and x != 0 and y != self._y_max-1 and \
                x != self._x_max-1 and letter == 'A':
            corners = [
                self._puzzle[x-1][y-1],
                self._puzzle[x+1][y-1],
                self._puzzle[x+1][y+1],
                self._puzzle[x-1][y+1]
            ]
            if corners in [
                ['M', 'M', 'S', 'S'],
                ['S', 'M', 'M', 'S'],
                ['S', 'S', 'M', 'M'],
                ['M', 'S', 'S', 'M']
                # The only other 2 option is invalid
                # as they would make MAM and SAS crossing
            ]:
                return True
        return False

    def search(self):
        # Find all the first letters of `self._word`
        results = []
        for y, row in enumerate(self._puzzle):
            for x, letter in enumerate(row):
                current_letter = 0
                dirs = list(product([-1, 0, 1], [-1, 0, 1]))
                dirs.remove((0, 0))
                # Pick a direction and follow it until it either hits
                # the end of the word (return True)
                # or it fails (return False)
                for d in dirs:
                    if self.test_letter(current_letter, x, y, d):
                        results.append((x, y, d))
        print(f"Part 1: {len(results)}")
        result_2 = []
        for y, row in enumerate(self._puzzle):
            for x, letter in enumerate(row):
                if self.test_xmas(x, y):
                    result_2.append((x, y))
        # print(result_2)
        print(f"Part 2: {len(result_2)}")


if __name__ == "__main__":
    puzzle_matrix = []
    with open("./puzzle.txt") as input_string:
        for line in input_string.readlines():
            puzzle_matrix.append(list(line.replace('\n', '')))
    w = WordSearch(puzzle_matrix)
    w.search()
