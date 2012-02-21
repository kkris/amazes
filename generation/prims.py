from random import choice, randint
from base import Algorithm

class Prims(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)

        self.visited_cells = set()

    def get_unvisited_neighbours(self, cell):

        return list(filter(lambda c: c not in self.visited_cells, self.get_neighbours(cell)))

    def get_visited_neighbours(self, cell):

        return list(filter(lambda c: c in self.visited_cells, self.get_neighbours(cell)))

    def generate(self):

        frontiers = []

        cell = choice(choice(self.cells))
        self.visited_cells.add(cell)
        frontiers.extend(self.get_unvisited_neighbours(cell))
        while frontiers:
            cell = choice(frontiers)
            neighbour = choice(self.get_visited_neighbours(cell))
            cell.connect(neighbour)
            frontiers.remove(cell)
            self.visited_cells.add(cell)
            for frontier in self.get_unvisited_neighbours(cell):
                if not frontier in frontiers:
                    frontiers.append(frontier)

        return self.cells
