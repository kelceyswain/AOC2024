#! /usr/bin/env python3

import curses


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Location({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


class Object:
    def __init__(self):
        self.location = None  # Updated by Map
        self.map = None

    def get_symbol(self):
        return "?"


class Character(Object):
    def move(self, dx, dy):
        """Move the character by a delta (dx, dy)."""
        if self.map:
            new_x = self.location.x + dx
            new_y = self.location.y + dy
            # Check boundaries and collisions
            if not (0 <= new_x < self.map.width and 0 <= new_y < self.map.height):
                return  # Out of bounds

            target = self.map.get_object_at(new_x, new_y)

            if target is None:
                # Empty, so move there
                self.map.move_object(self, new_x, new_y)
            elif isinstance(target, Box):
                chain = [(new_x, new_y)]
                current_x, current_y = new_x, new_y
                while True:
                    next_x = current_x + dx
                    next_y = current_y + dy

                    if not (0 <= next_x < self.map.width and 0 <= next_y < self.map.height):
                        return
                    next_target = self.map.get_object_at(next_x, next_y)
                    if next_target is not None:
                        if isinstance(next_target, Box):
                            chain.append((next_x, next_y))
                            current_x, current_y = next_x, next_y
                        else:
                            # Something in the way, oooo yeah
                            return

                    else:
                        # Empty space found, push all boxes in `chain`
                        for x, y in reversed(chain):
                            box = self.map.get_object_at(x, y)
                            self.map.move_object(box, x + dx, y + dy)
                        self.map.move_object(self, new_x, new_y)
                        return

    def get_symbol(self):
        return "@"


class Wall(Object):
    def get_symbol(self):
        return "#"


class Box(Object):
    def get_symbol(self):
        return "O"


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {}

    def add_object(self, obj, x, y):
        if (x, y) in self.grid:
            raise ValueError(f"Location ({x}, {y}) is already occupied!")
        self.grid[(x, y)] = obj
        obj.location = Location(x, y)  # Update object's location

    def move_object(self, obj, new_x, new_y):
        del self.grid[(obj.location.x, obj.location.y)]
        self.grid[(new_x, new_y)] = obj
        obj.location = Location(new_x, new_y)

    def get_object_at(self, x, y):
        """Retrieve the object at a specific location."""
        return self.grid.get((x, y), None)

    def can_move_to(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        target = self.get_object_at(x, y)
        return target is None  # Only empty spaces are movable to

    def remove_object(self, obj):
        """Remove an object from the map."""
        del self.grid[(obj.location.x, obj.location.y)]

    def render(self, stdscr):
        """Render the map as a grid using curses."""
        score = 0
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                obj = self.get_object_at(x, y)
                if obj:
                    row += obj.get_symbol()  # Get the symbol for the object
                    if isinstance(obj, Box):
                        score += (y * 100) + x
                else:
                    row += "."  # Empty space
            stdscr.addstr(y, 0, row)  # Write the row at the correct position
        stdscr.addstr(self.height + 1, 0, f"GPS = {score}")


class Game:
    def __init__(self, map_width, map_height, instructions):
        self.map = Map(map_width, map_height)
        self.instructions = instructions
        self.character = None

    def add_character(self, character, x, y):
        self.character = character
        self.map.add_object(character, x, y)
        character.map = self.map

    def add_object(self, obj, x, y):
        self.map.add_object(obj, x, y)
        obj.map = self.map

    def run(self, stdscr):
        # Configure curses settings
        curses.curs_set(0)  # Hide the cursor
        stdscr.clear()
        stdscr.nodelay(True)  # Non-blocking input
        stdscr.timeout(100)  # Refresh every 100ms

        # Mapping file commands to movement directions
        command_to_delta = {
            "^": (0, -1),  # Up
            "v": (0, 1),   # Down
            "<": (-1, 0),  # Left
            ">": (1, 0)    # Right
        }

        command_index = 0  # Track the current command index

        # Game loop
        while True:
            stdscr.clear()  # Clear the screen
            self.map.render(stdscr)  # Render the map
            stdscr.refresh()  # Refresh the display

            # Handle user input
            # key = stdscr.getch()
            # if key == curses.KEY_UP:
            #     self.character.move(0, -1)
            # elif key == curses.KEY_DOWN:
            #     self.character.move(0, 1)
            # elif key == curses.KEY_LEFT:
            #     self.character.move(-1, 0)
            # elif key == curses.KEY_RIGHT:
            #     self.character.move(1, 0)
            # elif key == ord("q"):  # Quit the game
            #     break

            if command_index < len(self.instructions):
                command = self.instructions[command_index]
                dx, dy = command_to_delta[command]
                self.character.move(dx, dy)
                command_index += 1


if __name__ == "__main__":
    with open("./puzzle.txt", "r") as puzzle_file:
        puzzle_map, puzzle_instructions = puzzle_file.read().split("\n\n")
        puzzle_instructions = "".join(puzzle_instructions.split("\n"))

    def main(stdscr):
        # Initialize the game
        size_x = len(puzzle_map.split("\n")[0])
        size_y = len(puzzle_map.split('\n'))
        game = Game(map_width=size_x, map_height=size_y, instructions=puzzle_instructions)

        character = Character()

        for y, row in enumerate(puzzle_map.split("\n")):
            for x, char in enumerate(row):
                if char == "@":
                    game.add_character(character, x, y)
                elif char == "O":
                    box = Box()
                    game.add_object(box, x, y)
                elif char == "#":
                    wall = Wall()
                    game.add_object(wall, x, y)

        # Run the game
        game.run(stdscr)

    curses.wrapper(main)  # Run the main function inside curses
