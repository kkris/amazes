class Algorithm(object):

    def __init__(self, size, cells):

        self.size = size
        self.cells = cells

    def get_neighbours(self, cell):
        if cell.x < self.size - 1:
            yield self.cells[cell.y][cell.x+1]
        if cell.x > 0:
            yield self.cells[cell.y][cell.x-1]
        if cell.y < self.size - 1:
            yield self.cells[cell.y+1][cell.x]
        if cell.y > 0:
            yield self.cells[cell.y-1][cell.x]
