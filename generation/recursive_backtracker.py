from random import choice, randint
from base import Algorithm

class RecursiveBacktracker(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)

        self.visited_cells = set()

    def get_unvisited_neighbours(self, cell):

        return list(filter(lambda c: c not in self.visited_cells, self.get_neighbours(cell)))

    def generate(self):

        stack = []
        cell = choice(choice(self.cells))
        self.visited_cells.add(cell)
        stack.append(cell)

        while True:
            if not stack:
                break
            unvisited = self.get_unvisited_neighbours(cell)
            if unvisited:
                next = choice(unvisited)
                cell.connect(next)
                self.visited_cells.add(next)
                stack.append(next)
            else:
                next = stack.pop()

            cell = next

        return self.cells
