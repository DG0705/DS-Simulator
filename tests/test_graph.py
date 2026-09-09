import unittest
from data_structures.graph import (
    UndirectedGraph, GraphError, GraphEmptyError,
    GraphVertexError, GraphEdgeError, GraphValueError,
)


class TestGraphAddVertex(unittest.TestCase):
    def test_empty_graph(self):
        g = UndirectedGraph()
        self.assertTrue(g.is_empty())
        self.assertEqual(g.size(), 0)

    def test_add_one_vertex(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        self.assertEqual(g.size(), 1)
        self.assertTrue(g.has_vertex("A"))

    def test_add_multiple_vertices(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        self.assertEqual(g.size(), 3)
        self.assertEqual(g.vertices(), ["A", "B", "C"])

    def test_duplicate_vertex_raises(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        with self.assertRaises(GraphVertexError):
            g.add_vertex("A")

    def test_add_numeric_vertices(self):
        g = UndirectedGraph()
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        self.assertEqual(g.size(), 3)
        self.assertEqual(g.vertices(), [1, 2, 3])

    def test_insertion_order_preserved(self):
        g = UndirectedGraph()
        g.add_vertex("C")
        g.add_vertex("A")
        g.add_vertex("B")
        self.assertEqual(g.vertices(), ["C", "A", "B"])


class TestGraphHasVertex(unittest.TestCase):
    def test_has_vertex_empty(self):
        g = UndirectedGraph()
        self.assertFalse(g.has_vertex("A"))

    def test_has_vertex_exists(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        self.assertTrue(g.has_vertex("A"))

    def test_has_vertex_missing(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        self.assertFalse(g.has_vertex("B"))


class TestGraphRemoveVertex(unittest.TestCase):
    def test_remove_vertex(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        g.remove_vertex("A")
        self.assertFalse(g.has_vertex("A"))
        self.assertEqual(g.size(), 1)
        self.assertFalse(g.has_edge("A", "B"))

    def test_remove_vertex_cleans_edges(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.remove_vertex("A")
        self.assertFalse(g.has_vertex("A"))
        self.assertFalse(g.has_edge("A", "B"))
        self.assertFalse(g.has_edge("B", "A"))
        self.assertEqual(g.edges(), [])

    def test_remove_missing_vertex_raises(self):
        g = UndirectedGraph()
        with self.assertRaises(GraphVertexError):
            g.remove_vertex("A")


class TestGraphAddEdge(unittest.TestCase):
    def test_add_edge(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("B", "A"))

    def test_undirected_behavior(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        neighbors_a = g.neighbors("A")
        neighbors_b = g.neighbors("B")
        self.assertIn("B", neighbors_a)
        self.assertIn("A", neighbors_b)

    def test_self_loop_raises(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        with self.assertRaises(GraphValueError):
            g.add_edge("A", "A")

    def test_add_edge_missing_vertex_raises(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        with self.assertRaises(GraphVertexError):
            g.add_edge("A", "B")

    def test_duplicate_edge_raises(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        with self.assertRaises(GraphEdgeError):
            g.add_edge("A", "B")

    def test_duplicate_edge_reverse_raises(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        with self.assertRaises(GraphEdgeError):
            g.add_edge("B", "A")


class TestGraphHasEdge(unittest.TestCase):
    def test_has_edge_empty(self):
        g = UndirectedGraph()
        self.assertFalse(g.has_edge("A", "B"))

    def test_has_edge_exists(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("B", "A"))

    def test_has_edge_missing(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        self.assertFalse(g.has_edge("A", "B"))

    def test_has_edge_missing_vertex(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        self.assertFalse(g.has_edge("A", "B"))


class TestGraphRemoveEdge(unittest.TestCase):
    def test_remove_edge(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        self.assertFalse(g.has_edge("A", "B"))
        self.assertFalse(g.has_edge("B", "A"))

    def test_remove_edge_reverse_order(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        g.remove_edge("B", "A")
        self.assertFalse(g.has_edge("A", "B"))

    def test_remove_missing_edge_raises(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        with self.assertRaises(GraphEdgeError):
            g.remove_edge("A", "B")

    def test_remove_edge_missing_vertex_raises(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        with self.assertRaises(GraphVertexError):
            g.remove_edge("A", "B")


class TestGraphNeighbors(unittest.TestCase):
    def test_neighbors(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        self.assertEqual(g.neighbors("A"), ["B", "C"])

    def test_neighbors_isolated(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        self.assertEqual(g.neighbors("A"), [])

    def test_neighbors_missing_vertex_raises(self):
        g = UndirectedGraph()
        with self.assertRaises(GraphVertexError):
            g.neighbors("A")

    def test_neighbors_deterministic(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("C")
        g.add_vertex("B")
        g.add_edge("A", "C")
        g.add_edge("A", "B")
        result = g.neighbors("A")
        self.assertEqual(result, ["B", "C"])


class TestGraphVerticesEdges(unittest.TestCase):
    def test_vertices_insertion_order(self):
        g = UndirectedGraph()
        for v in ["C", "A", "B"]:
            g.add_vertex(v)
        self.assertEqual(g.vertices(), ["C", "A", "B"])

    def test_edges(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        edges = g.edges()
        self.assertEqual(edges, [("A", "B"), ("B", "C")])

    def test_edges_empty(self):
        g = UndirectedGraph()
        self.assertEqual(g.edges(), [])


class TestGraphMixedTypes(unittest.TestCase):
    def test_mixed_string_int_vertices(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex(1)
        g.add_vertex("B")
        self.assertEqual(g.size(), 3)
        self.assertIn("A", g.vertices())
        self.assertIn(1, g.vertices())
        self.assertIn("B", g.vertices())

    def test_mixed_type_edges(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex(1)
        g.add_edge("A", 1)
        self.assertTrue(g.has_edge("A", 1))
        self.assertTrue(g.has_edge(1, "A"))

    def test_mixed_type_neighbors(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex(1)
        g.add_vertex("B")
        g.add_edge("A", 1)
        g.add_edge("A", "B")
        neighbors = g.neighbors("A")
        self.assertIn(1, neighbors)
        self.assertIn("B", neighbors)

    def test_mixed_type_edges_display(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex(1)
        g.add_edge("A", 1)
        edges = g.edges()
        self.assertEqual(len(edges), 1)


class TestGraphSizeIsEmpty(unittest.TestCase):
    def test_size(self):
        g = UndirectedGraph()
        self.assertEqual(g.size(), 0)
        g.add_vertex("A")
        self.assertEqual(g.size(), 1)

    def test_len(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        self.assertEqual(len(g), 2)

    def test_is_empty(self):
        g = UndirectedGraph()
        self.assertTrue(g.is_empty())
        g.add_vertex("A")
        self.assertFalse(g.is_empty())


class TestGraphClear(unittest.TestCase):
    def test_clear(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.clear()
        self.assertTrue(g.is_empty())
        self.assertEqual(g.size(), 0)
        self.assertEqual(g.edges(), [])

    def test_clear_empty(self):
        g = UndirectedGraph()
        g.clear()
        self.assertTrue(g.is_empty())


class TestGraphRepr(unittest.TestCase):
    def test_repr_empty(self):
        g = UndirectedGraph()
        self.assertEqual(repr(g), "UndirectedGraph({})")

    def test_repr(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex("B")
        g.add_edge("A", "B")
        r = repr(g)
        self.assertIn("A", r)
        self.assertIn("B", r)


if __name__ == "__main__":
    unittest.main()
