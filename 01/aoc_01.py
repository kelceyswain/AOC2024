#! /usr/bin/env python

class ImportantPlaces:
    def __init__(self, a: list, b: list):
        a = sorted(a)
        b = sorted(b)
        if len(a) != len(b):
            raise IndexError("The two lists must be of equal length")
        distance = 0
        for i, obj in enumerate(a):
            d = abs(a[i] - b[i])
            distance += d
        print(f"Part 1: {distance}")


class Similarity:
    def __init__(self, a: list, b: list):
        score = 0
        for i in a:
            s = b.count(i)
            score += (s * i)
        print(f"Part 2: {score}")


if __name__ == "__main__":
    list_a, list_b = [], []
    with open("puzzle.txt", 'r') as input_file:
        input_text = input_file.read()
        for line in input_text.split('\n'):
            num = line.split()
            list_a.append(int(num[0]))
            list_b.append(int(num[1]))
    i = ImportantPlaces(list_a, list_b)
    i2 = Similarity(list_a, list_b)
