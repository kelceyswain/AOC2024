
class Sector:
    def __init__(self, id, start: int, size: int):
        self.id = id
        self.start = start
        self.size = size
        self.cursor = 0

    def __repr__(self):
        out_string = ""
        out_string += f"ID: {self.id} "
        out_string += f"Start: {self.start} "
        out_string += f"Length: {self.size}"
        return out_string

    def __lt__(self, other):
        return self.start < other.start

    def take(self, n, new_index):
        # Returns the id and how many were taken
        if n > self.size:
            taken = self.size
            self.size = 0
        else:
            taken = n
            self.size -= n
        return Sector(self.id, new_index, taken)


class Drive:
    def __init__(self, drive_map):
        self.drive_map = []
        cursor = 0
        self.cursor = 0
        self.space_dict = {
            # Keep a track of where the last space of a given size was
            # and start looking from there.
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0
        }
        id = 0
        self.max_id = 0
        for i, s in enumerate(drive_map):
            if i % 2 == 0:
                self.drive_map.append(Sector(id, cursor, int(s)))
                if id > self.max_id:
                    self.max_id = id
                id += 1
                cursor += int(s)
            else:
                cursor += int(s)
        self.max_sector = self.drive_map[-1].start + self.drive_map[-1].size

    def __repr__(self):
        out_string = ""
        for sector in self.drive_map:
            out_string += str(sector) + "\n"
        return out_string

    def get_value(self, index):
        for sector in self.drive_map:
            if index >= sector.start and index < (sector.start + sector.size):
                return sector
        return None

    def clean(self):
        self.drive_map = [s for s in self.drive_map if s.size > 0]
        self.drive_map.sort()
        last_sector = self.drive_map[-1]
        self.max_sector = last_sector.start + last_sector.size

    def find_first_empty(self):
        cursor = self.cursor
        size = 0
        while True:
            if self.get_value(cursor) is not None:
                cursor += 1
                self.cursor = cursor
            else:
                break
            if cursor >= self.max_sector:
                break
        while True:
            if self.get_value(cursor + size) is None:
                size += 1
            else:
                break
            if cursor >= self.max_sector:
                break
        # print(f"First empty sector: {cursor}")
        return (cursor, size)

    def free_space(self):
        space_loc, space_size = self.find_first_empty()
        if space_loc >= self.max_sector:
            return False
        self.drive_map.append(self.drive_map[-1].take(space_size, space_loc))
        self.clean()
        return True

    def get_map_loction(self, id):
        for i, s in enumerate(self.drive_map):
            if s.id == id:
                return i
        return None

    def find_space(self, s, stop):
        # Start from where the last space of this size was found
        cursor = self.space_dict[s]
        # print(f"I need {s} spaces")
        satisfied = False
        while not satisfied:
            if self.get_value(cursor) is not None:
                # location at cursor is not empty
                cursor += 1
            else:
                # location at cursor is empty
                # print(f"space {cursor} is empty")
                empty = []
                for c in range(s):
                    # are the next s spaces empty too?
                    empty.append(self.get_value(cursor + c))
                if set(empty) == {None}:
                    # print(f"\tAll empty! {empty}")
                    self.space_dict[s] = cursor
                    satisfied = True
                else:
                    # print(f"\t but not the rest {empty}")
                    cursor += 1

            if cursor == stop:
                return (None, 0)
        # print(f"Found space at {cursor}")
        return (cursor, s)

    def move_files(self, id):
        loc = self.get_map_loction(id)
        size = self.drive_map[loc].size
        print(self.drive_map[loc])
        space_loc, space_size = self.find_space(size, self.drive_map[loc].start)
        if space_loc and space_loc < self.drive_map[loc].start:
            print(f"Moving id: {id} to space {space_loc}")
            self.drive_map.append(self.drive_map[loc].take(space_size, space_loc))
            self.clean()
        return True

    def checksum(self):
        checksum = 0
        print(self.max_sector)
        for i in range(self.max_sector):
            if self.get_value(i):
                value = self.get_value(i).id
                checksum += (i * value)
                print(i, value, checksum)
        return checksum


if __name__ == "__main__":
    with open("./puzzle.txt", 'r') as puzzle_file:
        puzzle_input = puzzle_file.read().strip()

    d = Drive(puzzle_input)

    part = 2

    # Part 1
    if part == 1:
        while True:
            if d.free_space():
                continue
            else:
                break

    # Part 2
    if part == 2:
        for i in range(d.max_id, 0, -1):
            d.move_files(i)

    print(f"Part {part}: {d.checksum()}")
