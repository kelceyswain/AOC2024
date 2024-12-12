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

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def is_horizontal(self, other):
        return self.x == other.x

    def is_vertical(self, other):
        return self.y == other.y


@dataclass
class Plot:
    location: Coord
    crop: str
    explored: bool = False

    def __hash__(self):
        return hash((self.location, self.crop))

    def adjacent_plots(self):
        return [
            self.location + Coord(0, -1),
            self.location + Coord(1, 0),
            self.location + Coord(0, 1),
            self.location + Coord(-1, 0)
        ]


class Region:
    def __init__(self, plot: Plot, area):
        self._plots = set()
        self.crop = plot.crop
        self.top = plot.location.y
        self.bottom = 0
        self.left = plot.location.x
        self.right = 0
        self.add_plot(plot, area)
        self.perimeter_coords = set()
        self.sides = 0

        plot.explored = True

    def add_plot(self, plot, area):
        self._plots.add(plot)
        if plot.location.x < self.left:
            self.left = plot.location.x
        if plot.location.y < self.top:
            self.top = plot.location.y
        if plot.location.x > self.right:
            self.right = plot.location.x
        if plot.location.y > self.bottom:
            self.bottom = plot.location.y
        for loc in plot.adjacent_plots():
            if loc in area:
                adjacent_plot = area.get(loc, None)
                if adjacent_plot:
                    if not adjacent_plot.explored and adjacent_plot.crop == self.crop:
                        adjacent_plot.explored = True
                        self.add_plot(adjacent_plot, area)

    @property
    def plots(self):
        coords = []
        for plot in self._plots:
            coords.append(plot.location)
        return coords

    def coord_in_region(self, coord):
        in_region = False
        for p in self._plots:
            if p.location == coord:
                in_region = True
        return in_region

    def __len__(self):
        return len(self._plots)

    def perimeter(self):
        count = 0
        for plot in self._plots:
            for loc in plot.adjacent_plots():
                if not self.coord_in_region(loc):
                    count += 1
                    self.perimeter_coords.add(loc)
        return count

    def find_sides(self):
        # Alright, who cares about edges, when we can count corners which is much easier
        sides = 0
        for p in self.plots:
            # convex corners
            top_left = [p+Coord(-1, 0),  p+Coord(0, -1)]
            top_right = [p+Coord(0, -1),  p+Coord(1, 0)]
            bottom_right = [p+Coord(1, 0),  p+Coord(0, 1)]
            bottom_left = [p+Coord(0, 1), p+Coord(-1, 0)]

            if all([i in self.perimeter_coords for i in top_left]):
                sides += 1
            if all([i in self.perimeter_coords for i in top_right]):
                sides += 1
            if all([i in self.perimeter_coords for i in bottom_right]):
                sides += 1
            if all([i in self.perimeter_coords for i in bottom_left]):
                sides += 1

            if all([i in self.plots for i in top_left]) and p+Coord(-1, -1) in self.perimeter_coords:
                sides += 1
            if all([i in self.plots for i in top_right]) and p+Coord(1, -1) in self.perimeter_coords:
                sides += 1
            if all([i in self.plots for i in bottom_right]) and p+Coord(1, 1) in self.perimeter_coords:
                sides += 1
            if all([i in self.plots for i in bottom_left]) and p+Coord(-1, 1) in self.perimeter_coords:
                sides += 1

        self.sides = sides
        return sides

    def __repr__(self):
        return f"Region({self.crop})"


if __name__ == "__main__":
    with open('./puzzle.txt') as puzzle_file:
        puzzle_text = puzzle_file.read().split('\n')

    area = {}
    for y, row in enumerate(puzzle_text):
        for x, crop in enumerate(row):
            area[Coord(x, y)] = (Plot(Coord(x, y), crop))

    regions = []
    part_1 = 0
    part_2 = 0
    for c, a in area.items():
        if a.explored is False:
            regions.append(Region(a, area))

    for r in regions:
        cost = r.perimeter()*len(r)
        part_1 += cost

    print(f"Part 1: {part_1}")

    for r in regions:
        cost = r.find_sides()*len(r)
        part_2 += cost

    print(f"Part 2: {part_2}")
