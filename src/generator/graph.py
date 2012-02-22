class Node(object):
    """
    A class representing a node with specific coordinates.
    """

    def __init__(self, x, y, edges=None, value=None):

        self.x = x
        self.y = y
        self.value = value

        if edges:
            self.edges = edges
        else:
            self.edges = []


    def add_edge(self, edge):

        self.edges.append(edge)


    def remove_edge(self, edge):

        for node in edge.nodes:
            node._remove_edge(edge)

    def _remove_edge(self, edge):

        self.edges.remove(edge)


    def connect(self, other):

        edge = Edge(self, other)

    def disconnect(self, other):

        for edge in self.edges:
            if self in edge.nodes and other in edge.nodes:
                self.remove_edge(edge)

    @property
    def connected_nodes(self):

        for edge in self.edges:
            for node in edge.nodes:
                if node != self: yield node


    def is_connected_to(self, other):

        for edge in self.edges:
            if other in edge.nodes: return True

        return False


    def __str__(self):
        return '<Node({0}|{1})>'.format(self.x, self.y)

    def __repr__(self):
        return str(self)



class Edge(object):
    """
    A class representing an edge between two nodes.
    If a Edge is created it will automatically be added to the nodes.
    """

    def __init__(self, *nodes):

        self.nodes = nodes

        for node in nodes:
            if self not in node.edges:
                node.add_edge(self)


class Graph(object):

    def __init__(self, width, height):

        self.nodes = []

        for x in xrange(width):
            self.nodes.append([])
            for y in xrange(height):
                node = Node(y, x)
                self.nodes[x].append(node)

        self.nodes[0][0].is_start = True
        self.nodes[-1][-1].is_end = True


    def get_neighbours_for_node(self, node):
        """
        Yields the adjacent nodes.
        """
        x, y = node.x, node.y
        if self.nodes[y][-1] != node :
            yield self.nodes[y][x+1]
        if y < len(self.nodes)-1:
            yield self.nodes[y+1][x]
        if x > 0:
            yield self.nodes[y][x-1]
        if y > 0:
            yield self.nodes[y-1][x]
