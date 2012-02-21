from random import choice, randint
from base import Algorithm

class SideWinder(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)


    def generate(self):

        for row in self.cells:
            run = []
            for cell in row:
                run.append(cell)
                if (randint(0, 1) or cell.y == 0) and cell != row[-1]:
                    right = row[cell.x+1]
                    cell.connect(right)
                elif run and cell.y > 0:
                    cell = choice(run)
                    upper = self.cells[cell.y-1][cell.x]
                    cell.connect(upper)
                    run = []

                #print run
            if run:
                cell = choice(run)
                north = self.cells[cell.y-1][cell.x]
                cell.connect(north)
        return self.cells
