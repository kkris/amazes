from random import choice, randint
from base import Algorithm

class HuntAndKill(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)

        self.visited_cells = set()

    def get_unvisited_neighbours(self, cell):

        return list(filter(lambda c: c not in self.visited_cells, self.get_neighbours(cell)))

    def generate(self):

        def hunt():
            for row in self.cells:
                for cell in row:
                    if cell in self.visited_cells:
                        unvisited = self.get_unvisited_neighbours(cell)
                        if unvisited:
                            next = choice(unvisited)
                            cell.connect(next)
                            return next


        cell = choice(choice(self.cells))
        self.visited_cells.add(cell)

        while True:
            unvisited = self.get_unvisited_neighbours(cell)
            if unvisited:
                next = choice(unvisited)
                cell.connect(next)
            else:
                next = hunt()
                if next is None:
                    break

            self.visited_cells.add(next)

            cell = next

        return self.cells
