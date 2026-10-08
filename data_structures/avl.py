"""Self-balancing AVL tree with the same public operations as BinarySearchTree."""

from copy import deepcopy
from dataclasses import dataclass

from data_structures.bst import BinarySearchTree, BSTEmptyError, BSTValueError


@dataclass(frozen=True)
class AVLStep:
    description: str
    root: object
    focus_values: tuple = ()
    rotation_values: tuple = ()
    rotation_type: str = ""


class AVLNode:
    __slots__ = ("value", "left", "right", "height")

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree(BinarySearchTree):
    """Binary search tree that keeps each node's balance factor within 1."""

    @staticmethod
    def _node_height(node):
        return node.height if node is not None else 0

    def height(self):
        return self._node_height(self._root)

    def _update_height(self, node):
        node.height = 1 + max(self._node_height(node.left), self._node_height(node.right))

    def _rotate_left(self, node):
        child = node.right
        node.right = child.left
        child.left = node
        self._update_height(node)
        self._update_height(child)
        return child

    def _rotate_right(self, node):
        child = node.left
        node.left = child.right
        child.right = node
        self._update_height(node)
        self._update_height(child)
        return child

    def _rebalance(self, node):
        self._update_height(node)
        balance = self._node_height(node.left) - self._node_height(node.right)
        if balance > 1:
            if self._node_height(node.left.left) < self._node_height(node.left.right):
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._node_height(node.right.right) < self._node_height(node.right.left):
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, value):
        self._root = self._insert_avl(self._root, value)

    def _insert_avl(self, node, value):
        if node is None:
            self._size += 1
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert_avl(node.left, value)
        elif value > node.value:
            node.right = self._insert_avl(node.right, value)
        else:
            raise BSTValueError(f"Value {value} already exists in AVL tree.")
        return self._rebalance(node)

    def delete(self, value):
        if self._root is None:
            raise BSTEmptyError("Cannot delete from an empty AVL tree.")
        self._root = self._delete_avl(self._root, value)
        self._size -= 1
        return value

    def _delete_avl(self, node, value):
        if node is None:
            raise BSTValueError(f"Value {value} not found in AVL tree.")
        if value < node.value:
            node.left = self._delete_avl(node.left, value)
        elif value > node.value:
            node.right = self._delete_avl(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_avl(node.right, successor.value)
        return self._rebalance(node)

    def find_min(self):
        if self._root is None:
            raise BSTEmptyError("Cannot find minimum: AVL tree is empty.")
        return self._find_min(self._root).value

    def find_max(self):
        if self._root is None:
            raise BSTEmptyError("Cannot find maximum: AVL tree is empty.")
        node = self._root
        while node.right:
            node = node.right
        return node.value

    def __repr__(self):
        return f"AVLTree({self.inorder()})"

    def plan_insert(self, value):
        """Return every insertion step and a separate tree with the final result."""
        if self.search(value) is not None:
            raise BSTValueError(f"Value {value} already exists in AVL tree.")
        working = deepcopy(self)
        steps = []

        def emit(description, focus=(), rotation=(), rotation_type=""):
            steps.append(AVLStep(description, deepcopy(working.root), tuple(focus),
                                 tuple(rotation), rotation_type))

        if working.root is None:
            working._root = AVLNode(value)
            working._size = 1
            emit(f"Insert {value} as the root; left height = 0, right height = 0, BF = 0.", (value,))
            return steps, working

        path = []
        node = working.root
        while node:
            path.append(node)
            direction = "left" if value < node.value else "right"
            emit(f"Compare {value} with {node.value}: move {direction}.", (node.value,))
            child = node.left if value < node.value else node.right
            if child is None:
                new_node = AVLNode(value)
                if value < node.value:
                    node.left = new_node
                else:
                    node.right = new_node
                working._size += 1
                emit(f"Insert {value} below {node.value}; new node height = 1, BF = 0.",
                     (value, node.value))
                break
            node = child

        for index in range(len(path) - 1, -1, -1):
            working._trace_rebalance(path, index, emit)
        return steps, working

    def plan_delete(self, value):
        """Return every deletion step and a separate tree with the final result."""
        if self.root is None:
            raise BSTEmptyError("Cannot delete from an empty AVL tree.")
        if self.search(value) is None:
            raise BSTValueError(f"Value {value} not found in AVL tree.")
        working = deepcopy(self)
        steps = []

        def emit(description, focus=(), rotation=(), rotation_type=""):
            steps.append(AVLStep(description, deepcopy(working.root), tuple(focus),
                                 tuple(rotation), rotation_type))

        path = []
        node = working.root
        while node.value != value:
            path.append(node)
            direction = "left" if value < node.value else "right"
            emit(f"Compare {value} with {node.value}: move {direction}.", (node.value,))
            node = node.left if value < node.value else node.right
        path.append(node)
        emit(f"Found {value}; inspect its children before deletion.", (value,))

        if node.left and node.right:
            successor_parent = node
            successor = node.right
            emit(f"Find the inorder successor in the right subtree of {value}.",
                 (node.value, successor.value))
            while successor.left:
                path.append(successor)
                successor_parent = successor
                successor = successor.left
                emit(f"Move left to successor candidate {successor.value}.",
                     (successor.value,))
            node.value = successor.value
            emit(f"Replace {value} with inorder successor {successor.value}.",
                 (successor.value,))
            if successor_parent is node:
                node.right = successor.right
            else:
                successor_parent.left = successor.right
            working._size -= 1
            emit(f"Remove the old successor node {successor.value}.",
                 (successor_parent.value,))
            rebalance_path = path
        else:
            parent = path[-2] if len(path) > 1 else None
            replacement = node.left if node.left else node.right
            working._replace_child(parent, node, replacement)
            working._size -= 1
            emit(f"Remove {value}; connect its parent to its remaining child.",
                 (parent.value,) if parent else ())
            rebalance_path = path[:-1]

        for index in range(len(rebalance_path) - 1, -1, -1):
            working._trace_rebalance(rebalance_path, index, emit)
        return steps, working

    def _replace_child(self, parent, old, new):
        if parent is None:
            self._root = new
        elif parent.left is old:
            parent.left = new
        else:
            parent.right = new

    def _trace_rebalance(self, path, index, emit):
        node = path[index]
        parent = path[index - 1] if index else None
        self._update_height(node)
        left_height = self._node_height(node.left)
        right_height = self._node_height(node.right)
        balance = left_height - right_height
        emit(f"At {node.value}: left height {left_height} - right height {right_height} "
             f"= BF {balance:+d}; node height = {node.height}.", (node.value,))

        if balance > 1:
            child = node.left
            child_balance = self._node_height(child.left) - self._node_height(child.right)
            if child_balance < 0:
                grandchild = child.right
                affected = (node.value, child.value, grandchild.value)
                emit(f"LR imbalance at {node.value}: rotate left at {child.value}, "
                     f"then right at {node.value}.", rotation=affected, rotation_type="LR")
                node.left = self._rotate_left(child)
                emit(f"LR step 1: left rotation at {child.value} completed.",
                     rotation=affected, rotation_type="LR")
            else:
                affected = (node.value, child.value)
                emit(f"LL imbalance at {node.value}: rotate right at {node.value}.",
                     rotation=affected, rotation_type="LL")
            replacement = self._rotate_right(node)
            self._replace_child(parent, node, replacement)
            emit(f"Right rotation at {node.value} completed; {replacement.value} is subtree root.",
                 rotation=affected, rotation_type="LR" if child_balance < 0 else "LL")
        elif balance < -1:
            child = node.right
            child_balance = self._node_height(child.left) - self._node_height(child.right)
            if child_balance > 0:
                grandchild = child.left
                affected = (node.value, child.value, grandchild.value)
                emit(f"RL imbalance at {node.value}: rotate right at {child.value}, "
                     f"then left at {node.value}.", rotation=affected, rotation_type="RL")
                node.right = self._rotate_right(child)
                emit(f"RL step 1: right rotation at {child.value} completed.",
                     rotation=affected, rotation_type="RL")
            else:
                affected = (node.value, child.value)
                emit(f"RR imbalance at {node.value}: rotate left at {node.value}.",
                     rotation=affected, rotation_type="RR")
            replacement = self._rotate_left(node)
            self._replace_child(parent, node, replacement)
            emit(f"Left rotation at {node.value} completed; {replacement.value} is subtree root.",
                 rotation=affected, rotation_type="RL" if child_balance > 0 else "RR")
