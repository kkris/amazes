#!/usr/bin/env python

import pprint
import random
from collections import defaultdict
from utils import flatten

from generation import generation_algorithms
from solving import solving_algorithms

#random.seed(5) # For testing purposes



class Cell(object):

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.connections = []

    def connect(self, cell, connection=None):

        if connection is None:
            connection = Connection(self, cell)
            cell.connect(self, connection)

        self.connections.append(connection)

    @property
    def adjacent(self):
        for connection in self.connections:
            if connection.cell1 == self:
                yield connection.cell2
            else:
                yield connection.cell1

    def __str__(self):
        return '<Cell ({0},{1})>'.format(self.x, self.y)

    def __repr__(self):
        return str(self)




class Connection(object):

    def __init__(self, cell1, cell2):

        self.cell1 = cell1
        self.cell2 = cell2

        self.marks = 0 # some solving algorithms mark paths


    def __str__(self):
        return '<Connection ({0},{1}) <-> ({2},{3})>'.format(self.cell1.x, self.cell1.y, self.cell2.x, self.cell2.y)

    def __repr__(self):
        return str(self)




class Maze(object):

    def __init__(self, size):

        self.size = size
        self.cells = self.generate_cells()


    def generate_cells(self):

        cells = [[] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                cell = Cell(j, i)
                cells[i].append(cell)

        return cells


    def generate(self, algorithm):

        algorithm = generation_algorithms[algorithm]
        return algorithm(self.size, self.cells).generate()


class Mazes(object):

    def __init__(self, size):

        self.size = size


    def generate(self, algorithm):
        maze = Maze(self.size)
        return maze.generate(algorithm)


    def solve(self, algorithm, cells):
        solver = solving_algorithms[algorithm]
        return solver(cells).solve()
