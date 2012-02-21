from random import choice, randint
from base import Algorithm

class BinaryTree(Algorithm):

    def __init__(self, size, cells):

        Algorithm.__init__(self, size, cells)


    def generate(self):

        for row in self.cells:
            for cell in row:
                if cell.y == 0 and cell != row[-1]:
                    right = row[cell.x+1]
                    cell.connect(right)
                elif cell.x == len(row)-1 and cell.y > 0:
                    upper = self.cells[cell.y-1][cell.x]
                    cell.connect(upper)
                elif randint(0, 1) and cell.y > 0:
                    upper = self.cells[cell.y-1][cell.x]
                    cell.connect(upper)
                elif cell != row[-1]:
                    right = row[cell.x+1]
                    cell.connect(right)

        return self.cells
