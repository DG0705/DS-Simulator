"""Reusable source-code panel for data-structure operations."""

import ast
import textwrap
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QTextCursor, QTextFormat
from PyQt6.QtWidgets import QFrame, QLabel, QPlainTextEdit, QTextEdit, QVBoxLayout


ROOT = Path(__file__).resolve().parents[1]

OPERATION_METHODS = {
    "Array": {"Append": "append", "Insert": "insert", "Delete": "delete", "Search": "search", "Update": "update", "Get": "get", "Traverse": "traverse", "Clear": "clear"},
    "Stack": {"Push": "push", "Pop": "pop", "Peek": "peek", "Is Empty": "is_empty", "Size": "size", "Traverse": "traverse", "Clear": "clear"},
    "Queue": {"Enqueue": "enqueue", "Dequeue": "dequeue", "Front": "front", "Rear": "rear", "Is Empty": "is_empty", "Size": "size", "Traverse": "traverse", "Clear": "clear"},
    "Linked List": {"Insert at Head": "insert_at_head", "Insert at Tail": "insert_at_tail", "Insert at Index": "insert_at_index", "Delete Head": "delete_head", "Delete Tail": "delete_tail", "Delete at Index": "delete_at_index", "Search": "search", "Update": "update", "Get": "get", "Traverse": "traverse", "Size": "size", "Is Empty": "is_empty", "Clear": "clear"},
    "Binary Search Tree": {"Insert": "_insert", "Delete": "_delete", "Search": "_search", "Inorder Traversal": "_inorder", "Preorder Traversal": "_preorder", "Postorder Traversal": "_postorder", "Level Order Traversal": "level_order", "Find Minimum": "find_min", "Find Maximum": "find_max", "Height": "_height", "Size": "size", "Is Empty": "is_empty", "Clear": "clear"},
    "AVL Tree": {"Insert": "_insert_avl", "Delete": "_delete_avl", "Search": "_search", "Inorder Traversal": "_inorder", "Preorder Traversal": "_preorder", "Postorder Traversal": "_postorder", "Level Order Traversal": "level_order", "Find Minimum": "find_min", "Find Maximum": "find_max", "Height": "height", "Size": "size", "Is Empty": "is_empty", "Clear": "clear"},
    "Heap": {"Insert": "insert", "Extract Max": "extract_max", "Peek": "peek", "Build Heap": "build_heap", "Traverse": "traverse", "Size": "size", "Is Empty": "is_empty", "Clear": "clear"},
    "Graph": {"Add Vertex": "add_vertex", "Add Edge": "add_edge", "Remove Vertex": "remove_vertex", "Remove Edge": "remove_edge", "Neighbors": "neighbors", "Vertices": "vertices", "Edges": "edges", "BFS": "bfs", "DFS": "dfs", "Size": "size", "Is Empty": "is_empty", "Has Vertex": "has_vertex", "Has Edge": "has_edge", "Clear": "clear"},
}

STRUCTURE_FILES = {
    "Array": "data_structures/array.py", "Stack": "data_structures/stack.py",
    "Queue": "data_structures/queue.py", "Linked List": "data_structures/linked_list.py",
    "Binary Search Tree": "data_structures/bst.py", "AVL Tree": "data_structures/avl.py",
    "Heap": "data_structures/heap.py", "Graph": "data_structures/graph.py",
}

INHERITED_AVL_METHODS = {"_search", "_inorder", "_preorder", "_postorder", "level_order", "size", "is_empty", "clear"}

ADJACENCY_MATRIX_CODE = """def graph_from_adjacency_matrix(matrix):
    graph = UndirectedGraph()
    node_count = len(matrix)
    for node in range(node_count):
        graph.add_vertex(str(node + 1))
    for row in range(node_count):
        for column in range(row + 1, node_count):
            if matrix[row][column] == 1:
                graph.add_edge(str(row + 1), str(column + 1))
    return graph"""

AVL_EXPLAINED_CODE = """class AVLTree:
    # Height of an empty subtree is 0.
    def height(self, node):
        return node.height if node is not None else 0

    def update_height(self, node):
        left_height = self.height(node.left)
        right_height = self.height(node.right)
        node.height = 1 + max(left_height, right_height)

    def balance_factor(self, node):
        # BF = left subtree height - right subtree height
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, old_root):
        # Used for an LL imbalance.
        new_root = old_root.left
        moved_subtree = new_root.right
        new_root.right = old_root
        old_root.left = moved_subtree
        self.update_height(old_root)
        self.update_height(new_root)
        return new_root

    def rotate_left(self, old_root):
        # Used for an RR imbalance.
        new_root = old_root.right
        moved_subtree = new_root.left
        new_root.left = old_root
        old_root.right = moved_subtree
        self.update_height(old_root)
        self.update_height(new_root)
        return new_root

    def rebalance(self, node):
        self.update_height(node)
        balance = self.balance_factor(node)

        if balance > 1:              # left side is too tall
            if self.balance_factor(node.left) < 0:
                # LR case: left rotation, then right rotation
                node.left = self.rotate_left(node.left)
            # LL case: one right rotation
            return self.rotate_right(node)

        if balance < -1:             # right side is too tall
            if self.balance_factor(node.right) > 0:
                # RL case: right rotation, then left rotation
                node.right = self.rotate_right(node.right)
            # RR case: one left rotation
            return self.rotate_left(node)

        return node                   # already balanced

    def insert(self, node, value):
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self.insert(node.left, value)
        elif value > node.value:
            node.right = self.insert(node.right, value)
        else:
            raise ValueError("Duplicate values are not allowed")
        # Recalculate heights and rotate while recursion unwinds.
        return self.rebalance(node)

    def delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value > node.value:
            node.right = self.delete(node.right, value)
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor = self.minimum(node.right)
            node.value = successor.value
            node.right = self.delete(node.right, successor.value)
        return self.rebalance(node)"""


class DataStructureCodePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(350)
        self.setMaximumWidth(520)
        self.setStyleSheet("QFrame { background: #111827; border-left: 1px solid #374151; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        self.title = QLabel("Python Code")
        self.title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        self.operation_label = QLabel("")
        self.operation_label.setStyleSheet("color: #FBBF24; font-size: 12px;")
        self.operation_label.setWordWrap(True)
        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setFont(QFont("Consolas", 10))
        self.editor.setStyleSheet("QPlainTextEdit { background: #111827; color: #E5E7EB; border: none; }")
        layout.addWidget(self.title)
        layout.addWidget(self.operation_label)
        layout.addWidget(self.editor, 1)
        self._execution_line = 1

    def show_operation(self, structure, operation):
        method = OPERATION_METHODS.get(structure, {}).get(operation)
        if structure == "AVL Tree" and operation in {"Insert", "Delete"}:
            code = AVL_EXPLAINED_CODE
            execution_line = self._line_containing(
                code, "def insert" if operation == "Insert" else "def delete"
            )
            self.operation_label.setText(
                f"{operation} · BF = left height − right height · LL/LR/RL/RR rotations"
            )
        elif structure == "Graph" and operation == "Adjacency Matrix":
            code, execution_line = ADJACENCY_MATRIX_CODE, 4
        elif method:
            filename = STRUCTURE_FILES[structure]
            if structure == "AVL Tree" and method in INHERITED_AVL_METHODS:
                filename = "data_structures/bst.py"
            if structure == "Graph" and method in {"bfs", "dfs"}:
                filename = "algorithms/graph_algorithms.py"
            code, execution_line = self._extract_method(ROOT / filename, method)
        else:
            code, execution_line = "# Select an operation to view its Python implementation.", 1
        self.title.setText(f"{structure} Python Code")
        if not (structure == "AVL Tree" and operation in {"Insert", "Delete"}):
            self.operation_label.setText(operation)
        self.editor.setPlainText(code)
        self._execution_line = execution_line
        self._highlight_line(1)

    def highlight_execution(self):
        self._highlight_line(self._execution_line)

    def highlight_avl_step(self, step):
        """Highlight the balance or rotation code represented by an AVL trace step."""
        if "def balance_factor" not in self.editor.toPlainText():
            return
        description = step.description.lower()
        rotation_lines = {
            "LL": "# LL case: one right rotation",
            "LR": "# LR case: left rotation, then right rotation",
            "RR": "# RR case: one left rotation",
            "RL": "# RL case: right rotation, then left rotation",
        }
        if "left rotation" in description and "completed" in description:
            needle = "def rotate_left"
        elif "right rotation" in description and "completed" in description:
            needle = "def rotate_right"
        elif step.rotation_type in rotation_lines:
            needle = rotation_lines[step.rotation_type]
        elif "bf" in description or "height" in description or "balance" in description:
            needle = "balance = self.balance_factor(node)"
        elif "insert" in description or "compare" in description:
            needle = "def insert"
        elif "delete" in description or "remove" in description:
            needle = "def delete"
        else:
            needle = "return self.rebalance(node)"
        self._highlight_line(self._line_containing(self.editor.toPlainText(), needle))

    @staticmethod
    def _line_containing(code, text):
        for number, line in enumerate(code.splitlines(), 1):
            if text in line:
                return number
        return 1

    @staticmethod
    def _extract_method(path, method_name):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        matches = [node for node in ast.walk(tree)
                   if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method_name]
        if not matches:
            return f"# Implementation for {method_name} was not found.", 1
        node = matches[0]
        lines = source.splitlines()[node.lineno - 1:node.end_lineno]
        code = textwrap.dedent("\n".join(lines))
        body = list(node.body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            body = body[1:]
        execution_line = (body[0].lineno - node.lineno + 1) if body else 1
        return code, max(1, execution_line)

    def _highlight_line(self, line_number):
        block = self.editor.document().findBlockByNumber(line_number - 1)
        if not block.isValid():
            return
        selection = QTextEdit.ExtraSelection()
        selection.cursor = QTextCursor(block)
        selection.format.setBackground(QColor("#92400E"))
        selection.format.setForeground(QColor("#FFFFFF"))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        self.editor.setExtraSelections([selection])
        self.editor.setTextCursor(selection.cursor)
        self.editor.ensureCursorVisible()
