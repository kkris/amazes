from random import choice
from base import Algorithm


def get_next_cell(cell):

    def sort(cell, adjacent):
        for connection in cell.connections:
            if connection.cell1 == adjacent or connection.cell2 == adjacent:
                return connection.marks


    adjacents = sorted(cell.adjacent, key=lambda a: sort(cell, a))
    for adj in adjacents:
        for c in cell.connections:
            if c.cell1 == adj or c.cell2 == adj:
                connection = c
    return adjacents[0]


def mark_connection(cell, adjacent):
    for connection in cell.connections:
        if connection.cell1 == adjacent or connection.cell2 == adjacent:
            connection.marks += 1


class Tremaux(Algorithm):

    def __init__(self, cells):

        Algorithm.__init__(self, cells)


    def solve(self):

        start = self.cells[0][0]
        end = self.cells[-1][-1]
        cell = start
        yield cell

        while cell != end:
            next = get_next_cell(cell)
            mark_connection(cell, next)

            cell = next

            yield cell




class TremauxShortest(Algorithm):

    def __init__(self, cells):

        Algorithm.__init__(self, cells)

    def solve(self):

        start = self.cells[0][0]
        end = self.cells[-1][-1]
        cell = start

        while cell != end:
            next = get_next_cell(cell)
            mark_connection(cell, next)

            cell = next

        cell = start
        previous = None
        yield cell
        while cell != end:
            for connection in cell.connections:
                if connection.marks == 1:
                    next = connection.cell1 if connection.cell1 != cell else connection.cell2
                    if next != previous:
                        break

            previous = cell
            cell = next
            yield cell
