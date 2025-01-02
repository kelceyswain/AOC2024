def mix(secret, num):
    return secret ^ num


def prune(secret):
    return secret % 16777216


def next_secret(secret):
    s1 = prune(mix(secret * 64, secret))
    s2 = prune(mix(s1 // 32, s1))
    s3 = prune(mix(s2 * 2048, s2))
    return s3


part_1 = 0

if __name__ == "__main__":
    with open("puzzle.txt") as puzzle_file:
        puzzle_input = puzzle_file.read()
    for monkey in puzzle_input.split("\n"):
        monkey = int(monkey)
        for i in range(2000):
            monkey = next_secret(monkey)
        part_1 += monkey
    print(part_1)
