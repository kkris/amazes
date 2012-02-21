from random import choice
from base import Algorithm

class DepthFirst(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)

        self.visited_cells = set()

    def get_unvisited_neighbours(self, cell):

        return list(filter(lambda c: c not in self.visited_cells, self.get_neighbours(cell)))

    def generate(self):

        stack = []
        total_cells = self.size**2
        cell = choice(choice(self.cells))
        self.visited_cells.add(cell)

        while len(self.visited_cells) < total_cells:
            neighbours = self.get_unvisited_neighbours(cell)
            if neighbours:
                next = choice(neighbours)
                cell.connect(next)

                stack.append(next)
                self.visited_cells.add(next)
            else:
                next = stack.pop()

            cell = next

        return self.cells
