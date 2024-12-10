from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Location:
    height: int
    _topography: "Topography" = None

    def __repr__(self):
        return f"Location({self.coord}, {self.height})"

    def __hash__(self):
        return hash(self.coord)

    @property
    def coord(self):
        for coord, location in self._topography._locations.items():
            if location is self:
                return coord
        # This will only happen if the Location is not in Topography
        return None

    def adjacent_locations(self):
        x = self.coord.x
        y = self.coord.y
        adjacent_coords = [Coord(x-1, y), Coord(x+1, y), Coord(x, y-1), Coord(x, y+1)]
        return [
            self._topography.get_location(coord)
            for coord in adjacent_coords
            if self._topography.get_location(coord) is not None
        ]

    def is_height(self, h):
        # return True if height == h
        if self.height == h:
            return True
        return False

    def ways_up(self):
        route = []
        for adj in self.adjacent_locations():
            if adj.is_height(self.height+1):
                route.append(adj)
        return route


class Topography:
    def __init__(self):
        self._locations = {}
        self._dimensions = Coord(0, 0)

    def add_location(self, coord: Coord, height: int):
        location = Location(height=height, _topography=self)
        self._locations[coord] = location
        # lots of plus ones
        if coord.x+1 >= self._dimensions.x:
            self._dimensions.x = coord.x+1
        if coord.y+1 >= self._dimensions.y:
            self._dimensions.y = coord.y+1

    def __str__(self):
        out_string = ""
        for y in range(self._dimensions.y):
            row = ""
            for x in range(self._dimensions.x):
                row += str(self._locations[Coord(x, y)].height)
            row += '\n'
            out_string += (row)
        return out_string

    @property
    def locations(self):
        return [(coord, loc) for coord, loc in self._locations.items()]

    def get_location(self, coord: Coord):
        return self._locations.get(coord, None)

    def get_trailheads(self):
        trailheads = []
        for c, l in self._locations.items():
            if l.is_height(0):
                trailheads.append(l)
        return trailheads


def walk(locations: list[Location]):
    return_list = []
    for loc in locations:
        if loc.height == 9:
            return_list.append(loc)
        else:
            return_list.extend(walk(loc.ways_up()))
    return return_list


if __name__ == "__main__":
    t = Topography()

    with open("./puzzle.txt", 'r') as puzzle_file:
        puzzle_input = puzzle_file.readlines()
        for y, row in enumerate(puzzle_input):
            for x, height in enumerate(row):
                if height != "\n":
                    t.add_location(Coord(x, y), int(height))

    trailheads = t.get_trailheads()
    routes = {}
    for trail in trailheads:
        routes[trail] = walk([trail])

    part_1 = 0
    part_2 = 0
    for key, route in routes.items():
        part_1 += len(set(route))
        part_2 += len(route)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
