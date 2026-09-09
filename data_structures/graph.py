from typing import Any, Dict, List, Set, Tuple


class GraphError(Exception):
    """Base exception for Graph operations."""
    pass


class GraphEmptyError(GraphError):
    """Raised when operating on an empty graph."""
    pass


class GraphVertexError(GraphError):
    """Raised when a vertex operation fails."""
    pass


class GraphEdgeError(GraphError):
    """Raised when an edge operation fails."""
    pass


class GraphValueError(GraphError):
    """Raised when an invalid value is provided."""
    pass


class UndirectedGraph:
    """Undirected graph using adjacency-list representation.

    Vertices are stored as dictionary keys mapping to sets of neighbors.
    Self-loops are rejected.
    Duplicate edges are handled gracefully.
    """

    def __init__(self) -> None:
        self._adjacency: Dict[Any, Set[Any]] = {}

    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph. O(1).

        Raises GraphVertexError if vertex already exists.
        """
        if vertex in self._adjacency:
            raise GraphVertexError(f"Vertex '{vertex}' already exists in graph.")
        self._adjacency[vertex] = set()

    def add_edge(self, vertex1: Any, vertex2: Any) -> None:
        """Add an undirected edge between two vertices. O(1).

        Raises GraphValueError for self-loops.
        Raises GraphVertexError if either vertex does not exist.
        """
        if vertex1 == vertex2:
            raise GraphValueError("Self-loops are not allowed.")
        if vertex1 not in self._adjacency:
            raise GraphVertexError(f"Vertex '{vertex1}' not found in graph.")
        if vertex2 not in self._adjacency:
            raise GraphVertexError(f"Vertex '{vertex2}' not found in graph.")
        self._adjacency[vertex1].add(vertex2)
        self._adjacency[vertex2].add(vertex1)

    def remove_vertex(self, vertex: Any) -> None:
        """Remove a vertex and all its edges. O(degree).

        Raises GraphVertexError if vertex does not exist.
        """
        if vertex not in self._adjacency:
            raise GraphVertexError(f"Vertex '{vertex}' not found in graph.")
        for neighbor in list(self._adjacency[vertex]):
            self._adjacency[neighbor].discard(vertex)
        del self._adjacency[vertex]

    def remove_edge(self, vertex1: Any, vertex2: Any) -> None:
        """Remove an undirected edge between two vertices. O(1).

        Raises GraphVertexError if either vertex does not exist.
        Raises GraphEdgeError if edge does not exist.
        """
        if vertex1 not in self._adjacency:
            raise GraphVertexError(f"Vertex '{vertex1}' not found in graph.")
        if vertex2 not in self._adjacency:
            raise GraphVertexError(f"Vertex '{vertex2}' not found in graph.")
        if vertex2 not in self._adjacency[vertex1]:
            raise GraphEdgeError(f"Edge '{vertex1}' — '{vertex2}' does not exist.")
        self._adjacency[vertex1].discard(vertex2)
        self._adjacency[vertex2].discard(vertex1)

    def neighbors(self, vertex: Any) -> List[Any]:
        """Return list of neighbors. O(1).

        Raises GraphVertexError if vertex does not exist.
        """
        if vertex not in self._adjacency:
            raise GraphVertexError(f"Vertex '{vertex}' not found in graph.")
        return sorted(self._adjacency[vertex])

    def vertices(self) -> List[Any]:
        """Return sorted list of all vertices. O(V log V)."""
        return sorted(self._adjacency.keys())

    def edges(self) -> List[Tuple[Any, Any]]:
        """Return unique undirected edges as sorted tuples. O(V + E).

        Each edge appears once as (min, max).
        """
        edge_set: Set[Tuple[Any, Any]] = set()
        for v in self._adjacency:
            for n in self._adjacency[v]:
                edge = (min(v, n), max(v, n))
                edge_set.add(edge)
        return sorted(edge_set)

    def has_vertex(self, vertex: Any) -> bool:
        """Check if vertex exists. O(1)."""
        return vertex in self._adjacency

    def has_edge(self, vertex1: Any, vertex2: Any) -> bool:
        """Check if edge exists. O(1)."""
        if vertex1 not in self._adjacency or vertex2 not in self._adjacency:
            return False
        return vertex2 in self._adjacency[vertex1]

    def size(self) -> int:
        """Return number of vertices. O(1)."""
        return len(self._adjacency)

    def is_empty(self) -> bool:
        """Check if graph is empty. O(1)."""
        return len(self._adjacency) == 0

    def clear(self) -> None:
        """Remove all vertices and edges. O(1)."""
        self._adjacency.clear()

    def __len__(self) -> int:
        return len(self._adjacency)

    def __repr__(self) -> str:
        verts = self.vertices()
        edge_list = self.edges()
        if not verts:
            return "UndirectedGraph({})"
        edge_strs = [f"{a}—{b}" for a, b in edge_list]
        return f"UndirectedGraph({{{', '.join(str(v) for v in verts)} | {', '.join(edge_strs)}}})"
