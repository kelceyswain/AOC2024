#! /usr/bin/env python3


class Map:
    """
        Hold the information for the map including size and obstacles
        keep a count of what locations have been walked through
    """
    def __init__(self, size: tuple[int, int], obstacles: list[tuple[int, int]]):
        self._size_x, self._size_y = size
        self._obstacles = obstacles

    def __repr__(self):
        out_string = ""
        print(self._obstacles)
        for y in range(self._size_y+1):
            for x in range(self._size_x+1):
                if (x, y) in self._obstacles:
                    char = '#'
                else:
                    char = '.'
                out_string += char
            out_string += ("\n")
        return out_string

    def is_obstacle(self, position):
        if position in self._obstacles:
            return True
        else:
            return False

    def is_outside(self, position):
        x, y = position
        if x > self._size_x or y > self._size_y:
            return True
        if x < 0 or y < 0:
            return True
        return False

    def add_obstacle(self, position):
        if position not in self._obstacles:
            self._obstacles.append(position)


class Guard:
    def __init__(self, position: tuple[int, int], direction: str, map: Map):
        if len(direction) > 1:
            raise ValueError("Only one character")
        self._position = position
        self._direction = direction
        self._map = map
        self._visited = [position]
        self._visited_direction = [(position, direction)]

    def __repr__(self):
        return f"position: {self._position}\ndirection: {self._direction}"

    def move(self):
        next = ()
        if self._direction == '^':
            # Look north one space
            next = (self._position[0], self._position[1]-1)
        elif self._direction == '>':
            # Look east one space
            next = (self._position[0]+1, self._position[1])
        elif self._direction == 'v':
            # Look south one space
            next = (self._position[0], self._position[1]+1)
        elif self._direction == '<':
            # Look west one space
            next = (self._position[0]-1, self._position[1])
        if self._map.is_obstacle(next):
            dirs = ['^', '>', 'v', '<']
            dir_index = (dirs.index(self._direction) + 1) % 4
            self._direction = dirs[dir_index]
            return True
        elif self._map.is_outside(next):
            # Is out of the map
            return False
        else:
            self._position = next
            if self._position not in self._visited:
                self._visited.append(self._position)
            if (self._position, self._direction) not in self._visited_direction:
                self._visited_direction.append((self._position, self._direction))
            else:
                return "loop"
            return True

    @property
    def visited(self):
        return self._visited


if __name__ == "__main__":
    with open("./puzzle.txt") as puzzle_input:
        puzzle_string = puzzle_input.read()

    max_x, max_y = 0, 0
    obstacles = []
    guard_pos = ()
    guard_dir = ''
    for y, line in enumerate(puzzle_string.split('\n')):
        if y > max_y:
            max_y = y
        for x, character in enumerate(line):
            if x > max_x:
                max_x = x
            if character == '#':
                obstacles.append((x, y))
            elif character in ['^', '>', 'v', '<']:
                guard_pos = (x, y)
                guard_dir = character
    size = (max_x, max_y)

    m = Map(size, obstacles.copy())
    g = Guard(guard_pos, guard_dir, m)

    while True:
        # Keep walking until the g leaves the map
        if g.move():
            continue
        else:
            break
    print(f"Part 1: {len(g.visited)}")

    # Do it again repeatedly for part 2
    part_2 = 0
    # We only need to check positions the guard visits originally
    # and remove the guard starting position
    test_locations = g.visited.copy()
    # The first location is the starting position, so skip that
    test_locations = test_locations[1:]
    for x, y in test_locations:
        # It turns out I was never taking a fresh copy of the obstacles
        # and lists are weird in python, like pointers to memory addresses
        m = Map(size, obstacles.copy())
        g = Guard(guard_pos, guard_dir, m)

        m.add_obstacle((x, y))
        while True:
            result = g.move()
            if result:
                if result == "loop":
                    # print(f"({x}, {y}) = loop")
                    part_2 += 1
                    break
                continue
            else:
                # print(f"({x}, {y}) = escape")
                break
    print(f"Part 2: {part_2}")
