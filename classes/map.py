import math
from dataclasses import dataclass


class Node:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.value = 0
        self.adjacent = []
        self.shortest_path = []

    def __repr__(self):
        return str("Row: "+str(self.row)+" Column: "+str(self.column))

    def show_adjacents(self):
        return str("Adjacents: "+str(self.adjacent))

@dataclass
class Map:
    size: int = 5

    def generate_map(self):
        self.grid = [[Node(y, x) for x in range(self.size)] for y in range(self.size)]
        self.grid[self.size-1][self.size-1].value = -1
        self.turrets = [[None for number in range(self.size)] for number in range(self.size)]
        self.create_edges()

    def create_edges(self):
        for row in range(self.size):
            for column in range(self.size):
                node = self.grid[row][column]
                if row > 0:
                    node.adjacent.append(self.grid[row - 1][column])
                if row < self.size - 1:
                    node.adjacent.append(self.grid[row + 1][column])
                if column > 0:
                    node.adjacent.append(self.grid[row][column - 1])
                if column < self.size - 1:
                    node.adjacent.append(self.grid[row][column + 1])

    def place_block(self, row, column):
        self.grid[row][column].value = 1
        placable = self.check_reachability()
        if (row == column == self.size - 1) or (row==column==0):
            placable = False
        if not placable:
            self.grid[row][column].value = 0

    def remove_block(self, row, column):
        if row == column == self.size - 1:
            pass
        else:
            self.grid[row][column].value = 0

    def place_turret(self, turret, row, column):
        self.grid[row][column].value = 1
        placable = self.check_reachability()
        if placable:
            self.turrets[row][column] = turret
            self.turrets[row][column].row = row
            self.turrets[row][column].column = column
            self.find_shortest_path()
        else:
            self.grid[row][column].value = 0
            print ("Not placable.")

    def find_passage_nodes(self):
        # Check on all the zero or less value tiles.
        self.passable: list[Node] = []
        for x in range(self.size):
            for y in range(self.size):
                node = self.grid[x][y]
                if node.value == 0:
                    self.passable.append(node)

    def check_reachability(self):
        self.find_passage_nodes()
        self.reachable = []
        # Initialize with the ending point.
        self.reachable.append(self.grid[self.size-1][self.size-1])
        for node in self.reachable:
            self.check_reachable_nodes(node)
        if len(self.passable) <= 0:
            return True
        return False
        
    def check_reachable_nodes(self, start: Node):
        for node in start.adjacent:
            if node in self.passable:
                self.reachable.append(node)
                self.passable.remove(node)

    def find_shortest_path(self):
        self.distance = [[999 for x in range(self.size)] for x in range(self.size)]
        self.distance[self.size-1][self.size-1] = 0
        self.previous_node = [[None for x in range(self.size)] for x in range(self.size)]
        attempt: list[Node] = []
        self.find_passage_nodes()
        attempt.append(self.grid[self.size-1][self.size-1])
        # Go through the nodes.
        for node in attempt:
            # Go through the nodes adjacent to the nodes.
            for anode in node.adjacent:
                if anode in self.passable:
                    attempt.append(anode)
                    self.passable.remove(anode)
                    if self.distance[node.row][node.column] + 1 < self.distance[anode.row][anode.column]:
                        self.distance[anode.row][anode.column] = self.distance[node.row][node.column] + 1
                        self.previous_node[anode.row][anode.column] = node