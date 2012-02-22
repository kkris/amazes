from random import choice


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
        yield node, True
        previous = None
        orientation = ORIENTATION_RIGHT

        while node != end:
            neighbours = filter(lambda n: n != previous, node.connected_nodes)

            if previous and len(list(node.connected_nodes)) == 1:
                orientation = (previous.x - node.x, previous.y - node.y)
                previous = node
                node = node.connected_nodes.next()
            elif len(neighbours) == 1:
                orientation = (neighbours[0].x - node.x, neighbours[0].y - node.y)
                previous = node
                node = neighbours[0]
            else:
                value = 0
                for neighbour in neighbours:
                    orientation_neighbour = (neighbour.x - node.x, neighbour.y - node.y)

                    direction = get_direction(orientation, orientation_neighbour)
                    if direction == ORIENTATION_RIGHT:
                        new_orientation = orientation_neighbour
                        break
                    elif direction == ORIENTATION_AHEAD and value < VALUE_AHEAD:
                        new_orientation = orientation_neighbour
                        value = VALUE_AHEAD
                    elif direction == ORIENTATION_LEFT and value < VALUE_LEFT:
                        new_orientation = orientation_neighbour
                        value = VALUE_LEFT

                for neighbour in node.connected_nodes:
                    orientation_neighbour = (neighbour.x - node.x, neighbour.y - node.y)
                    if orientation_neighbour == new_orientation:
                        next = neighbour
                        break

                orientation = new_orientation
                previous = node
                node = next

            yield node, True




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
