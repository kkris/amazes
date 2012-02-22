from random import randint, choice

from amazes.generator.graph import Graph
from amazes.utils import flatten


def get_unvisited_neighbours(graph, visited_nodes, node):

    neighbours = graph.get_neighbours_for_node(node)
    return filter(lambda n: n not in visited_nodes, neighbours)


def get_visited_neighbours(graph, visited_nodes, node):

    neighbours = graph.get_neighbours_for_node(node)
    return filter(lambda n: n in visited_nodes, neighbours)


class MazeGenerator(object):
    name = 'MazeGenerator'

    pass



class BinaryTree(MazeGenerator):

    name = 'Binarytree'

    def generate(self, width, height):

        graph = Graph(width, height)

        for row in graph.nodes:
            for node in row:
                if node.y == 0 and node != row[-1]:
                    node.connect(row[node.x + 1])
                elif node == row[-1] and node.y > 0:
                    node.connect(graph.nodes[node.y - 1][node.x])
                elif randint(0, 1) and node.y > 0:
                    node.connect(graph.nodes[node.y - 1][node.x])
                elif node != row[-1]:
                    node.connect(row[node.x + 1])

        return graph



class AldousBroder(MazeGenerator):

    name = 'Aldous-Broder'

    def generate(self, width, height):

        graph = Graph(width, height)

        total_nodes = width * height
        visited_nodes = set()

        node = choice(choice(graph.nodes))
        visited_nodes.add(node)
        while len(visited_nodes) < total_nodes:
            next = choice(list(graph.get_neighbours_for_node(node)))
            if next not in visited_nodes:
                node.connect(next)
                visited_nodes.add(next)
            node = next

        return graph


class DepthFirst(MazeGenerator):

    name = 'Depth-first'

    def generate(self, width, height):

        graph = Graph(width, height)

        stack = []
        visited_nodes = set()
        total_nodes = width * height

        node = choice(choice(graph.nodes))
        visited_nodes.add(node)

        while len(visited_nodes) < total_nodes:
            unvisited = get_unvisited_neighbours(graph, visited_nodes, node)
            if unvisited:
                next = choice(unvisited)
                node.connect(next)

                stack.append(next)
                visited_nodes.add(next)
            else:
                next = stack.pop()

            node = next

        return graph



class HuntAndKill(MazeGenerator):

    name = 'Hunt and Kill'

    def generate(self, width, height):

        graph = Graph(width, height)

        visited_nodes = set()

        def hunt():
            for n in flatten(graph.nodes):
                if n in visited_nodes:
                    unvisited = get_unvisited_neighbours(graph, visited_nodes, n)
                    if unvisited:
                        next = choice(unvisited)
                        n.connect(next)
                        return next

        node = choice(choice(graph.nodes))
        visited_nodes.add(node)

        while True:
            unvisited = get_unvisited_neighbours(graph, visited_nodes, node)
            if unvisited:
                next = choice(unvisited)
                node.connect(next)
            else:
                next = hunt()
                if next is None:
                    break

            visited_nodes.add(next)

            node = next

        return graph



class Prims(MazeGenerator):

    name = 'Prim\'s'

    def generate(self, width, height):

        graph = Graph(width, height)

        visited_nodes = set()

        frontiers = []
        node = choice(choice(graph.nodes))
        visited_nodes.add(node)

        neighbours = get_unvisited_neighbours(graph, visited_nodes, node)
        frontiers.extend(neighbours)

        while frontiers:
            node = choice(frontiers)
            visited = get_visited_neighbours(graph, visited_nodes, node)
            neighbour = choice(visited)
            node.connect(neighbour)
            frontiers.remove(node)
            visited_nodes.add(node)

            for frontier in get_unvisited_neighbours(graph, visited_nodes, node):
                if not frontier in frontiers:
                    frontiers.append(frontier)

        return graph



class RecursiveBacktracker(MazeGenerator):

    name = 'Recursive Backtracker'

    def generate(self, width, height):

        graph = Graph(width, height)

        visited_nodes = set()
        stack = []

        node = choice(choice(graph.nodes))
        visited_nodes.add(node)
        stack.append(node)

        while True:
            if not stack:
                break

            unvisited = get_unvisited_neighbours(graph, visited_nodes, node)
            if unvisited:
                next = choice(unvisited)
                node.connect(next)
                visited_nodes.add(next)
                stack.append(next)
            else:
                next = stack.pop()

            node = next

        return graph


class SideWinder(MazeGenerator):

    name = 'Sidewinder'

    def generate(self, width, height):

        graph = Graph(width, height)

        for row in graph.nodes:
            run = []
            for node in row:
                run.append(node)
                if (randint(0, 1) or node.y == 0) and node != row[-1]:
                    right = row[node.x + 1]
                    node.connect(right)
                elif run and node.y > 0:
                    node = choice(run)
                    upper = graph.nodes[node.y - 1][node.x]
                    node.connect(upper)
                    run = []

            if run:
                node = choice(run)
                upper = graph.nodes[node.y - 1][node.x]
                node.connect(upper)

        return graph



class Wilsons(MazeGenerator):

    name = 'Wilsons'

    def generate(self, width, height):

        graph = Graph(width, height)

        visited_nodes = set()

        nodes = list(flatten(graph.nodes))
        node = choice(nodes)
        nodes.remove(node)

        visited_nodes.add(node)

        while nodes:
            path = {}
            node = n = choice(nodes)
            while node not in visited_nodes:
                next = choice(list(graph.get_neighbours_for_node(node)))
                path[node] = next

                node = next

            node = n
            while node not in visited_nodes:
                next = path[node]
                node.connect(next)
                visited_nodes.add(node)
                nodes.remove(node)

                node = next

        return graph
