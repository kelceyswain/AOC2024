from collections import Counter


def rule(c: Counter):
    new_counter = Counter()

    # I am sure this could have been written more succinctly
    # but I started with the rule as written in the puzzle
    def rule(n):
        if n == 0:
            return 1
        n_length = len(str(n))
        if n_length % 2 == 0:
            a = int(str(n)[:n_length // 2])
            b = int(str(n)[n_length // 2:])
            return [a, b]
        else:
            return n * 2024

    for stone in list(c):
        new_stone = rule(stone)
        if isinstance(new_stone, list):
            for s in new_stone:
                new_counter[s] += c[stone]
        else:
            new_counter[rule(stone)] += c[stone]
    return new_counter


if __name__ == "__main__":
    with open("./puzzle.txt", 'r') as puzzle_file:
        puzzle_input = puzzle_file.read().split()
    puzzle_input = [int(i) for i in puzzle_input]

    c = Counter(puzzle_input)
    for _ in range(25):
        c = rule(c)
    print(f"Part 1: {sum(c.values())}")

    # And another 50 more times to make it up to 75
    for _ in range(50):
        c = rule(c)
    print(f"Part 2: {sum(c.values())}")
