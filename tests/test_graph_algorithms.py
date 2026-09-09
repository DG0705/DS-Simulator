import unittest
from data_structures.graph import UndirectedGraph, GraphVertexError, GraphEmptyError
from algorithms.graph_algorithms import bfs, dfs


class TestBFS(unittest.TestCase):
    def test_empty_graph(self):
        g = UndirectedGraph()
        with self.assertRaises(GraphEmptyError):
            bfs(g, "A")

    def test_single_vertex(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        order, steps = bfs(g, "A")
        self.assertEqual(order, ["A"])
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0], ("A", []))

    def test_linear_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "D")
        order, steps = bfs(g, "A")
        self.assertEqual(order, ["A", "B", "C", "D"])

    def test_branching_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D", "E"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        g.add_edge("C", "E")
        order, steps = bfs(g, "A")
        self.assertEqual(order, ["A", "B", "C", "D", "E"])

    def test_disconnected_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("C", "D")
        order, steps = bfs(g, "A")
        self.assertEqual(order, ["A", "B"])
        self.assertEqual(len(steps), 2)

    def test_invalid_start_vertex(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        with self.assertRaises(GraphVertexError):
            bfs(g, "B")

    def test_deterministic_order(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D", "E"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("A", "D")
        g.add_edge("A", "E")
        order1, _ = bfs(g, "A")
        order2, _ = bfs(g, "A")
        self.assertEqual(order1, order2)

    def test_steps_recorded(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        order, steps = bfs(g, "A")
        self.assertEqual(steps[0], ("A", ["B", "C"]))
        self.assertEqual(steps[1], ("B", []))
        self.assertEqual(steps[2], ("C", []))

    def test_does_not_mutate_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        bfs(g, "A")
        self.assertEqual(g.vertices(), ["A", "B", "C"])
        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("A", "C"))

    def test_complex_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D", "E", "F"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        g.add_edge("B", "E")
        g.add_edge("C", "F")
        order, _ = bfs(g, "A")
        self.assertEqual(order, ["A", "B", "C", "D", "E", "F"])


class TestDFS(unittest.TestCase):
    def test_empty_graph(self):
        g = UndirectedGraph()
        with self.assertRaises(GraphEmptyError):
            dfs(g, "A")

    def test_single_vertex(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        order, steps = dfs(g, "A")
        self.assertEqual(order, ["A"])
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0], ("A", []))

    def test_linear_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "D")
        order, steps = dfs(g, "A")
        self.assertEqual(order, ["A", "B", "C", "D"])

    def test_branching_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D", "E"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        g.add_edge("C", "E")
        order, steps = dfs(g, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(len(order), 5)

    def test_disconnected_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("C", "D")
        order, steps = dfs(g, "A")
        self.assertEqual(order, ["A", "B"])

    def test_invalid_start_vertex(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        with self.assertRaises(GraphVertexError):
            dfs(g, "B")

    def test_deterministic_order(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D", "E"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("A", "D")
        g.add_edge("A", "E")
        order1, _ = dfs(g, "A")
        order2, _ = dfs(g, "A")
        self.assertEqual(order1, order2)

    def test_steps_recorded(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        order, steps = dfs(g, "A")
        self.assertEqual(steps[0][0], "A")
        self.assertEqual(len(order), 3)

    def test_does_not_mutate_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        dfs(g, "A")
        self.assertEqual(g.vertices(), ["A", "B", "C"])
        self.assertTrue(g.has_edge("A", "B"))
        self.assertTrue(g.has_edge("A", "C"))

    def test_complex_graph(self):
        g = UndirectedGraph()
        for v in ["A", "B", "C", "D", "E", "F"]:
            g.add_vertex(v)
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        g.add_edge("B", "E")
        g.add_edge("C", "F")
        order, _ = dfs(g, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(len(order), 6)


class TestMixedTypeTraversal(unittest.TestCase):
    def test_bfs_mixed_types(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex(1)
        g.add_vertex("B")
        g.add_edge("A", 1)
        g.add_edge("A", "B")
        order, _ = bfs(g, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(len(order), 3)

    def test_dfs_mixed_types(self):
        g = UndirectedGraph()
        g.add_vertex("A")
        g.add_vertex(1)
        g.add_vertex("B")
        g.add_edge("A", 1)
        g.add_edge("A", "B")
        order, _ = dfs(g, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(len(order), 3)


if __name__ == "__main__":
    unittest.main()
