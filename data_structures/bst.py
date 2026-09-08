from collections import deque
from typing import Any, List, Optional


class BSTError(Exception):
    """Base exception for BST operations."""
    pass


class BSTEmptyError(BSTError):
    """Raised when operating on an empty BST."""
    pass


class BSTValueError(BSTError):
    """Raised when an invalid value is provided."""
    pass


class TreeNode:
    """A single node in a Binary Search Tree."""

    __slots__ = ("value", "left", "right")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.value})"


class BinarySearchTree:
    """Binary Search Tree implementation.

    - No duplicates allowed (raises BSTValueError).
    - Delete handles leaf, one-child, and two-children cases.
    - Height convention: empty tree = 0, single node = 1.
    """

    def __init__(self) -> None:
        self._root: Optional[TreeNode] = None
        self._size: int = 0

    @property
    def root(self) -> Optional[TreeNode]:
        return self._root

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def insert(self, value: Any) -> None:
        """Insert a value. Raises BSTValueError on duplicate."""
        if self._root is None:
            self._root = TreeNode(value)
            self._size += 1
            return
        self._insert(self._root, value)

    def _insert(self, node: TreeNode, value: Any) -> None:
        if value == node.value:
            raise BSTValueError(f"Value {value} already exists in BST.")
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                self._size += 1
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
                self._size += 1
            else:
                self._insert(node.right, value)

    def search(self, value: Any) -> Optional[TreeNode]:
        """Return the node containing value, or None."""
        return self._search(self._root, value)

    def _search(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def search_path(self, value: Any) -> List[TreeNode]:
        """Return the path from root to the node (or where it would be)."""
        path: List[TreeNode] = []
        self._search_path(self._root, value, path)
        return path

    def _search_path(self, node: Optional[TreeNode], value: Any, path: List[TreeNode]) -> None:
        if node is None:
            return
        path.append(node)
        if value == node.value:
            return
        if value < node.value:
            self._search_path(node.left, value, path)
        else:
            self._search_path(node.right, value, path)

    def delete(self, value: Any) -> Any:
        """Delete node with given value. Returns deleted value.

        Raises BSTEmptyError if tree is empty.
        Raises BSTValueError if value not found.
        """
        if self._root is None:
            raise BSTEmptyError("Cannot delete from an empty BST.")
        self._root, deleted = self._delete(self._root, value)
        if deleted is None:
            raise BSTValueError(f"Value {value} not found in BST.")
        self._size -= 1
        return deleted

    def _delete(self, node: TreeNode, value: Any) -> tuple:
        """Return (new_node_subtree, deleted_value)."""
        if value < node.value:
            if node.left:
                left, deleted = self._delete(node.left, value)
                node.left = left
                return node, deleted
            return node, None
        elif value > node.value:
            if node.right:
                right, deleted = self._delete(node.right, value)
                node.right = right
                return node, deleted
            return node, None
        else:
            deleted = node.value
            if node.left is None and node.right is None:
                return None, deleted
            elif node.left is None:
                return node.right, deleted
            elif node.right is None:
                return node.left, deleted
            else:
                successor = self._find_min(node.right)
                node.value = successor.value
                node.right, _ = self._delete(node.right, successor.value)
                return node, deleted

    def _find_min(self, node: TreeNode) -> TreeNode:
        while node.left is not None:
            node = node.left
        return node

    def inorder(self) -> List[Any]:
        """Return inorder traversal (sorted)."""
        result: List[Any] = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node: Optional[TreeNode], result: List[Any]) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def preorder(self) -> List[Any]:
        """Return preorder traversal."""
        result: List[Any] = []
        self._preorder(self._root, result)
        return result

    def _preorder(self, node: Optional[TreeNode], result: List[Any]) -> None:
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> List[Any]:
        """Return postorder traversal."""
        result: List[Any] = []
        self._postorder(self._root, result)
        return result

    def _postorder(self, node: Optional[TreeNode], result: List[Any]) -> None:
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

    def level_order(self) -> List[Any]:
        """Return level-order (BFS) traversal. O(n) time, O(w) space."""
        if self._root is None:
            return []
        result: List[Any] = []
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def find_min(self) -> Any:
        """Return minimum value. Raises BSTEmptyError if empty."""
        if self._root is None:
            raise BSTEmptyError("Cannot find minimum: BST is empty.")
        return self._find_min(self._root).value

    def find_max(self) -> Any:
        """Return maximum value. Raises BSTEmptyError if empty."""
        if self._root is None:
            raise BSTEmptyError("Cannot find maximum: BST is empty.")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.value

    def height(self) -> int:
        """Return height. Empty = 0, single node = 1."""
        return self._height(self._root)

    def _height(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        left_h = self._height(node.left)
        right_h = self._height(node.right)
        return 1 + max(left_h, right_h)

    def clear(self) -> None:
        """Remove all nodes."""
        self._root = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        vals = self.inorder()
        return "BST({" + ", ".join(str(v) for v in vals) + "})" if vals else "BST({})"

    def get_all_nodes(self) -> List[TreeNode]:
        """Return all nodes level-by-level for visualization. O(n) time."""
        if self._root is None:
            return []
        result: List[TreeNode] = []
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            result.append(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result
