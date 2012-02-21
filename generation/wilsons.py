from random import choice
from utils import flatten
from base import Algorithm



class Wilsons(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)

        self.visited_cells = set()


    def generate(self):

        cells = list(flatten(self.cells))
        a = choice(cells)
        cells.remove(a)

        self.visited_cells.add(a)

        while cells:
            path = {}
            cell = b = choice(cells)
            while cell not in self.visited_cells:
                next = choice(list(self.get_neighbours(cell)))
                path[cell] = next

                cell = next

            cell = b
            while cell not in self.visited_cells:
                next = path[cell]
                cell.connect(next)
                self.visited_cells.add(cell)
                cells.remove(cell)

                cell = next


        return self.cells
