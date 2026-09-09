from collections import deque
from typing import Any, List, Tuple
from data_structures.graph import UndirectedGraph, GraphVertexError, GraphEmptyError


def bfs(graph: UndirectedGraph, start_vertex: Any) -> Tuple[List[Any], List[Tuple[Any, List[Any]]]]:
    """Breadth-first search traversal.

    Returns (traversal_order, steps) where:
    - traversal_order: list of vertices in visit order
    - steps: list of (current_vertex, newly_discovered_vertices) tuples
    """
    if graph.is_empty():
        raise GraphEmptyError("Cannot traverse an empty graph.")
    if not graph.has_vertex(start_vertex):
        raise GraphVertexError(f"Vertex '{start_vertex}' not found in graph.")

    visited: set = set()
    queue: deque = deque([start_vertex])
    visited.add(start_vertex)
    traversal_order: List[Any] = []
    steps: List[Tuple[Any, List[Any]]] = []

    while queue:
        current = queue.popleft()
        traversal_order.append(current)
        newly_discovered: List[Any] = []

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                newly_discovered.append(neighbor)

        steps.append((current, newly_discovered))

    return traversal_order, steps


def dfs(graph: UndirectedGraph, start_vertex: Any) -> Tuple[List[Any], List[Tuple[Any, List[Any]]]]:
    """Depth-first search traversal (iterative with explicit stack).

    Returns (traversal_order, steps) where:
    - traversal_order: list of vertices in visit order
    - steps: list of (current_vertex, newly_discovered_vertices) tuples
    """
    if graph.is_empty():
        raise GraphEmptyError("Cannot traverse an empty graph.")
    if not graph.has_vertex(start_vertex):
        raise GraphVertexError(f"Vertex '{start_vertex}' not found in graph.")

    visited: set = set()
    stack: List[Any] = [start_vertex]
    traversal_order: List[Any] = []
    steps: List[Tuple[Any, List[Any]]] = []

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        traversal_order.append(current)
        newly_discovered: List[Any] = []

        for neighbor in reversed(graph.neighbors(current)):
            if neighbor not in visited:
                stack.append(neighbor)
                newly_discovered.append(neighbor)

        steps.append((current, newly_discovered))

    return traversal_order, steps
