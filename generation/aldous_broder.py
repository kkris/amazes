from random import choice
from base import Algorithm

class AldousBroder(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)

        self.visited_cells = set()


    def generate(self):

        total_cells = self.size**2
        cell = choice(choice(self.cells))

        while len(self.visited_cells) < total_cells:
            next = choice(list(self.get_neighbours(cell)))
            if not next in self.visited_cells:
                cell.connect(next)

                self.visited_cells.add(next)

            cell = next

        return self.cells
