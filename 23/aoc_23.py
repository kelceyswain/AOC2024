
class Computer:
    def __init__(self, name):
        self.name = name
        self._network = set([self])
        self._connections = [self]

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    @property
    def network(self):
        return sorted(self._network, key=lambda c: c.name)

    @network.setter
    def network(self, computer):
        if computer not in self._network:
            self._network.append(computer)

    @network.deleter
    def network(self, computer):
        if computer in self._network:
            self._network.remove(computer)

    @property
    def connections(self):
        return sorted(set(self._connections), key=lambda c: c.name)

    def add_to_network(self, other):
        if other not in self._connections:
            self._connections.append(other)
        if self not in other._connections:
            other._connections.append(self)

        combined_network = self._network.union(other._network, {self, other})

        for computer in combined_network:
            computer._network = combined_network


def build_network(connections):
    computer_map = {}

    for connection in connections:
        computer1, computer2 = connection.split("-")

        if computer1 not in computer_map:
            computer_map[computer1] = Computer(computer1)
        if computer2 not in computer_map:
            computer_map[computer2] = Computer(computer2)

        computer_map[computer1].add_to_network(computer_map[computer2])

    return computer_map


if __name__ == "__main__":
    with open("test.txt", "r") as puzzle_file:
        puzzle_text = puzzle_file.read().split("\n")
    network = build_network(puzzle_text)
    for key, value in network.items():
        # if len(value.connections) == 3:

        print(key, value.connections)
