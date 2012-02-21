from random import choice
from base import Algorithm


def mark_cells(cell, distance):

    adjacent = filter(lambda a: not hasattr(a, 'distance'), cell.adjacent)
    for a in adjacent:
        a.distance = distance
        mark_cells(a, distance+1)


class Flooding(Algorithm):

    def __init__(self, cells):

        Algorithm.__init__(self, cells)


    def solve(self):

        start = self.cells[0][0]
        end = self.cells[-1][-1]

        start.distance = 0
        mark_cells(start, 1)

        steps = [end]
        cell = end
        while cell != start:
            next = sorted(cell.adjacent, key=lambda a: a.distance)[0]
            steps.append(next)
            cell = next

        steps.reverse()
        for step in steps:
            yield step
