from random import choice
from base import Algorithm

ORIENTATION_RIGHT = (1, 0)
ORIENTATION_LEFT = (-1, 0)
ORIENTATION_AHEAD = (1, 1)

VALUE_AHEAD = 2
VALUE_LEFT = 1

def get_direction(o1, o2):
    if o1[0] == o2[1] and o1[1] == -o2[0]:
        return ORIENTATION_RIGHT
    elif o1[0] == -o2[1] and o1[1] == o2[0]:
        return ORIENTATION_LEFT
    elif o1[0] - o2[0] >= 0 and o1[1] - o2[1] >= 0:
        return ORIENTATION_AHEAD
    else:
        return None

class WallFollower(Algorithm):

    def __init__(self, cells):

        Algorithm.__init__(self, cells)


    def solve(self):

        start = self.cells[0][0]
        end = self.cells[-1][-1]

        cell = start
        yield cell
        previous = None
        orientation = ORIENTATION_RIGHT

        while cell != end:
            adjacent = filter(lambda c: c != previous, cell.adjacent)

            if previous and len(list(cell.adjacent)) == 1:
                orientation = (previous.x - cell.x, previous.y - cell.y)
                previous = cell
                cell = cell.adjacent.next()
            elif len(adjacent) == 1:
                orientation = (adjacent[0].x - cell.x, adjacent[0].y - cell.y)
                previous = cell
                cell = adjacent[0]
            else:
                value = 0
                for adjacent_cell in adjacent:
                    orientation_adjacent = (adjacent_cell.x - cell.x, adjacent_cell.y - cell.y)

                    direction = get_direction(orientation, orientation_adjacent)
                    if direction == ORIENTATION_RIGHT:
                        new_orientation = orientation_adjacent
                        break
                    elif direction == ORIENTATION_AHEAD and value < VALUE_AHEAD:
                        new_orientation = orientation_adjacent
                        value = VALUE_AHEAD
                    elif direction == ORIENTATION_LEFT and value < VALUE_LEFT:
                        new_orientation = orientation_adjacent
                        value = VALUE_LEFT

                for adjacent in cell.adjacent:
                    orientation_adjacent = (adjacent.x - cell.x, adjacent.y - cell.y)
                    if orientation_adjacent == new_orientation:
                        next = adjacent
                        break

                orientation = new_orientation
                previous = cell
                cell = next
            yield cell
