from random import choice
from base import Algorithm

class RandomMouse(Algorithm):

    def __init__(self, cells):

        Algorithm.__init__(self, cells)


    def solve(self):

        start = self.cells[0][0]
        end = self.cells[-1][-1]

        cell = start
        previous = None
        yield cell

        while cell != end:
            if len(list(cell.adjacent)) == 1:
                previous = cell
                cell = cell.adjacent.next()
            else:
                adjacent = filter(lambda c: c != previous, cell.adjacent)
                previous = cell
                cell = choice(adjacent)

            yield cell
