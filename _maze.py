#!/usr/bin/env python

import pprint
import random
from collections import defaultdict
from utils import flatten

random.seed(5) # For testing purposes

SIZE = 15



class Cell(object):

    def __init__(self, x, y):_

        self.x = x
        self.y = y

        self.connections = []

    def connect(self, cell, connection=None):

        if connection is None:
            connection = Connection(self, cell)

        self.connections.append(connection)
        cell.connect(self, connection)

    def __str__(self):
        return '<Cell ({0},{1})>'.format(self.x, self.y)

    def __repr__(self):
        return str(self)




class Connection(object):

    def __init__(self, cell1, cell2):

        self.cell1 = cell1
        self.cell2 = cell2




class Maze(object):



class Node(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.neighbours = []
        self.junctions = []

    def add_neighbour(self, node):
        self.neighbours.append(node)

    def add_junction(self, node):
        #print '({0},{1}) -> ({2},{3})'.format(self.x, self.y, node.x, node.y)
        self.junctions.append(node)

    def __repr__(self):
        return '<Node ({0},{1})>'.format(self.x, self.y)


    def __str__(self):
        return repr(self)



class MazeSolver(object):

    def __init__(self):

        pass


    def solve(self, method, nodes):

        return getattr(self, method)(nodes)


    def random_mouse(self, nodes):

        start = nodes[0][0]
        end = nodes[-1][-1]

        node = start
        previous = None
        yield node
        while node != end:
            if len(node.junctions) == 1:
                previous = node
                node = node.junctions[0]
            else:
                junctions = filter(lambda n: n != previous, node.junctions)
                previous = node
                node = random.choice(junctions)

            yield node


    def wall_follower(self, nodes):

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

        start = nodes[0][0]
        end = nodes[-1][-1]

        node = start
        yield node
        previous = None
        orientation = ORIENTATION_RIGHT

        while node != end:
            junctions = filter(lambda n: n != previous, node.junctions) # skip previous

            if previous and len(node.junctions) == 1:
                orientation = (previous.x - node.x, previous.y - node.y)
                previous = node
                node = node.junctions[0]
            elif len(junctions) == 1:
                orientation = (junctions[0].x - node.x, junctions[0].y - node.y)
                previous = node
                node = junctions[0]
            else:

                junction_value = 0
                for junction in junctions:
                    orientation_junction = (junction.x - node.x, junction.y - node.y)

                    direction = get_direction(orientation, orientation_junction)
                    if direction == ORIENTATION_RIGHT:
                        new_orientation = orientation_junction
                        break
                    elif direction == ORIENTATION_AHEAD and junction_value < VALUE_AHEAD:
                        new_orientation = orientation_junction
                        junction_value = VALUE_AHEAD
                    elif direction == ORIENTATION_LEFT and junction_value < VALUE_LEFT:
                        new_orientation = orientation_junction
                        junction_value = VALUE_LEFT

                for junction in node.junctions:
                    orientation_junction = (junction.x - node.x, junction.y - node.y)
                    if orientation_junction == new_orientation:
                        next = junction
                        break

                orientation = new_orientation
                previous = node
                node = next
            yield node





class Maze(object):


    def __init__(self):

        self.nodes = self.generate_nodes()
        self.maze_solver = MazeSolver()

    def generate_maze(self, method):

        self.nodes = self.generate_nodes()
        return getattr(self, method)()


    def generate_nodes(self):

        nodes = [[] for i in range(SIZE)]

        for i in range(SIZE):
            for j in range(SIZE):
                node = Node(j, i)
                nodes[i].append(node)

        for i, row in enumerate(nodes):
            for j, node in enumerate(row):
                if node.x < SIZE-1: # has a right neighbour
                    node.add_neighbour(nodes[i][j+1])
                if node.x > 0: # has a left neighbour
                    node.add_neighbour(nodes[i][j-1])
                if node.y < SIZE-1: # has a lower neighbour
                    node.add_neighbour(nodes[i+1][j])
                if node.y > 0: # has a upper neighbour
                    node.add_neighbour(nodes[i-1][j])

        return nodes

    def solve(self, method):

        return self.maze_solver.solve(method, self.nodes)


    def depth_first(self):

        stack = []
        total_cells = SIZE**2
        visited_cells = 1
        node = random.choice(random.choice(self.nodes))
        node.visited = True

        while visited_cells < total_cells:
            neighbours = filter(lambda n: not n.visited, node.neighbours)
            if neighbours:
                next = random.choice(neighbours)
                next.visited = True
                node.add_junction(next)
                next.add_junction(node)
                stack.append(next)
                visited_cells += 1
            else:
                next = stack.pop()

            node = next

        return self.nodes


    def aldous_broder(self):

        total_nodes = SIZE**2
        visited_nodes = 1

        node = random.choice(random.choice(self.nodes))

        while visited_nodes < total_nodes:
            next = random.choice(node.neighbours)
            if not next.visited:
                node.add_junction(next)
                next.add_junction(node)
                next.visited = True

                visited_nodes += 1
            node = next


        return self.nodes


    def wilsons(self):

        nodes = list(flatten(self.nodes))
        a = nodes.pop(random.randint(0, len(nodes)-1))
        a.visited = True

        while nodes:
            node = b = random.choice(nodes)

            while node != a:
                next = random.choice(node.neighbours)
                node.next = next

                node = next

            node = b
            while not node.visited:
                node.visited = True
                nodes.remove(node)
                node.add_junction(node.next)
                node.next.add_junction(node)
                node = node.next

        return self.nodes


    def binary_tree(self):

        for row in self.nodes:
            for node in row:
                if node.y == 0 and node.x < len(row)-1:
                    right = self.nodes[node.y][node.x+1]
                    right.add_junction(node)
                    node.add_junction(right)
                elif node.x == len(row)-1:
                    upper = self.nodes[node.y-1][node.x]
                    upper.add_junction(node)
                    node.add_junction(upper)
                elif random.randint(0, 1):
                    upper = self.nodes[node.y-1][node.x]
                    upper.add_junction(node)
                    node.add_junction(upper)
                else:
                    right = self.nodes[node.y][node.x+1]
                    right.add_junction(node)
                    node.add_junction(right)

        return self.nodes



    def sidewinder(self):

        for row in self.nodes:
            run = []
            cur_cell = row[0]
            run.append(cur_cell)
            while cur_cell != row[-1] or run:
                if random.randint(0, 1) and cur_cell.x < len(row)-1:
                    right = self.nodes[cur_cell.y][cur_cell.x+1]
                    right.add_junction(cur_cell)
                    cur_cell.add_junction(right)
                    cur_cell = right
                    run.append(cur_cell)
                elif run and cur_cell.y > 0:
                    print run
                    cell = random.choice(run)
                    north = self.nodes[cell.y-1][cell.x]
                    north.add_junction(cell)
                    cell.add_junction(north)
                    run = []
                    try:
                        cur_cell = self.nodes[cur_cell.y][cur_cell.x+1]
                    except IndexError:
                        pass
                else:
                    run = []

        return self.nodes



    def hunt_and_kill(self):

        node = random.choice(random.choice(self.nodes))
        node.visited = True

        def hunt():
            for row in self.nodes:
                for node in row:
                    if node.visited:
                        unvisited = filter(lambda n: not n.visited, node.neighbours)
                        if unvisited:
                            return random.choice(unvisited)


        while True:
            unvisited = filter(lambda n: not n.visited, node.neighbours)
            if unvisited:
                next = random.choice(unvisited)
                next.visited = True
                next.add_junction(node)
                node.add_junction(next)
            else:
                next = hunt()
                if next is None:
                    break
                next.visited = True
                next.add_junction(node)
                node.add_junction(next)

            node = next



        return self.nodes
