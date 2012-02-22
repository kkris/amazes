import unittest

from amazes.generator.graph import Node, Edge, Graph

class TestNode(unittest.TestCase):

    def test_creation(self):

        node = Node(0, 0)

        assert node.x == 0
        assert node.y == 0
        assert len(node.edges) == 0


    def test_add_remove_edge(self):

        node1 = Node(0, 0)
        node2 = Node(0, 1)

        node1.connect(node2)

        assert node1.is_connected_to(node2)
        assert node2.is_connected_to(node1)

        node1.disconnect(node2)

        assert not node1.is_connected_to(node2)
        assert not node2.is_connected_to(node1)


    def test_connected_nodes(self):

        node1 = Node(0, 0)
        node2 = Node(0, 1)
        node3 = Node(1, 0)

        assert list(node1.connected_nodes) == []

        node1.connect(node2)
        assert list(node1.connected_nodes) == [node2]
        assert list(node2.connected_nodes) == [node1]

        node1.connect(node3)
        assert node2 in list(node1.connected_nodes)
        assert node3 in list(node1.connected_nodes)




class TestGraph(unittest.TestCase):

    def test_creation(self):

        graph = Graph(4, 4)

        assert len(graph.nodes) == 4
        assert len(graph.nodes[0]) == 4
