from random import choice

class MazeSolver(object):
    name = 'Mazesolver'


class RandomMouse(MazeSolver):

    name = 'Random Mouse'

    def solve(self, graph):

        start = graph.nodes[0][0]
        end = graph.nodes[-1][-1]

        node = start
        previous = None
        yield node, True

        while node != end:
            if len(list(node.connected_nodes)) == 1:
                previous = node
                node = node.connected_nodes.next()
            else:
                neighbours = filter(lambda n: n != previous, node.connected_nodes)
                previous = node
                node = choice(neighbours)

            yield node, True



class WallFollower(MazeSolver):

    name = 'Wallfollower'

    def solve(self, graph):

        start = graph.nodes[0][0]
        end = graph.nodes[-1][-1]

        node = start
        previous = None
        yield node



class Flooding(MazeSolver):

    name = 'Flooding'

    def solve(self, graph):

        start = graph.nodes[0][0]
        end = graph.nodes[-1][-1]

        distances = {}

        def calculate_distance(node, distance):
            distances[node] = distance
            for neighbour in node.connected_nodes:
                if neighbour not in distances:
                    calculate_distance(neighbour, distance + 1)

        calculate_distance(start, 0)


        steps = [end]
        node = end
        while node != start:
            node = sorted(node.connected_nodes, key=lambda n: distances[n])[0]
            steps.append(node)

        steps.reverse()
        for step in steps:
            yield step, True



class FloodingWithDistanceDisplay(MazeSolver):

    name = 'Flooding (display distance)'

    def solve(self, graph):

        start = graph.nodes[0][0]
        end = graph.nodes[-1][-1]

        nodes = []
        distances = {}

        def calculate_distance(node, distance):
            distances[node] = distance
            nodes.append((node, distance))
            for neighbour in node.connected_nodes:
                if neighbour not in distances:
                    calculate_distance(neighbour, distance + 1)

        calculate_distance(start, 0)

        for node, distance in nodes:
            node.value = distance
            yield node, False

        steps = [end]
        node = end
        while node != start:
            node = sorted(node.connected_nodes, key=lambda n: distances[n])[0]
            steps.append(node)

        steps.reverse()
        for step in steps:
            yield step, True
