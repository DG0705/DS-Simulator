from typing import Any, List, Optional


class Node:
    """A single node in a singly linked list."""

    __slots__ = ("data", "next")

    def __init__(self, data: Any, next_node: Optional["Node"] = None) -> None:
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        return f"Node({self.data})"


class LinkedListError(Exception):
    """Base exception for LinkedList operations."""
    pass


class LinkedListEmptyError(LinkedListError):
    """Raised when operating on an empty linked list."""
    pass


class LinkedListIndexError(LinkedListError):
    """Raised when an invalid index is used."""
    pass


class LinkedListValueError(LinkedListError):
    """Raised when an invalid value is provided."""
    pass


class SinglyLinkedList:
    """Singly Linked List with head and tail pointers.

    Maintains O(1) access to both head and tail.
    Zero-based indexing.
    """

    def __init__(self) -> None:
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size: int = 0

    @property
    def head(self) -> Optional[Node]:
        return self._head

    @property
    def tail(self) -> Optional[Node]:
        return self._tail

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def _get_node_at(self, index: int) -> Node:
        """Return the node at the given index. Caller must validate bounds."""
        current = self._head
        for _ in range(index):
            assert current is not None
            current = current.next
        assert current is not None
        return current

    def insert_at_head(self, value: Any) -> None:
        """Insert a value at the head of the list. O(1)."""
        new_node = Node(value, self._head)
        self._head = new_node
        if self._tail is None:
            self._tail = new_node
        self._size += 1

    def insert_at_tail(self, value: Any) -> None:
        """Insert a value at the tail of the list. O(1)."""
        new_node = Node(value)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def insert_at_index(self, index: int, value: Any) -> None:
        """Insert a value at the specified index. O(n).

        Valid range: 0 <= index <= size.
        """
        if index < 0 or index > self._size:
            raise LinkedListIndexError(
                f"Index {index} out of range [0, {self._size}]"
            )
        if index == 0:
            self.insert_at_head(value)
            return
        if index == self._size:
            self.insert_at_tail(value)
            return
        prev = self._get_node_at(index - 1)
        new_node = Node(value, prev.next)
        prev.next = new_node
        self._size += 1

    def delete_head(self) -> Any:
        """Remove and return the head value. O(1).

        Raises:
            LinkedListEmptyError: If list is empty.
        """
        if self._head is None:
            raise LinkedListEmptyError("Cannot delete head: the linked list is empty.")
        value = self._head.data
        self._head = self._head.next
        self._size -= 1
        if self._head is None:
            self._tail = None
        return value

    def delete_tail(self) -> Any:
        """Remove and return the tail value. O(n).

        Raises:
            LinkedListEmptyError: If list is empty.
        """
        if self._head is None:
            raise LinkedListEmptyError("Cannot delete tail: the linked list is empty.")
        if self._head is self._tail:
            value = self._head.data
            self._head = None
            self._tail = None
            self._size -= 1
            return value
        prev = self._head
        while prev.next is not self._tail:
            prev = prev.next
        value = self._tail.data
        prev.next = None
        self._tail = prev
        self._size -= 1
        return value

    def delete_at_index(self, index: int) -> Any:
        """Remove and return the value at the given index. O(n).

        Valid range: 0 <= index < size.

        Raises:
            LinkedListIndexError: If index is out of range.
            LinkedListEmptyError: If list is empty.
        """
        if self._head is None:
            raise LinkedListEmptyError("Cannot delete from an empty linked list.")
        if index < 0 or index >= self._size:
            raise LinkedListIndexError(
                f"Index {index} out of range [0, {self._size - 1}]"
            )
        if index == 0:
            return self.delete_head()
        prev = self._get_node_at(index - 1)
        removed = prev.next
        assert removed is not None
        prev.next = removed.next
        if removed is self._tail:
            self._tail = prev
        self._size -= 1
        return removed.data

    def search(self, value: Any) -> int:
        """Return the index of the first occurrence of value.

        Raises:
            LinkedListValueError: If value not found.
            LinkedListEmptyError: If list is empty.
        """
        if self._head is None:
            raise LinkedListEmptyError("Cannot search an empty linked list.")
        current = self._head
        index = 0
        while current is not None:
            if current.data == value:
                return index
            current = current.next
            index += 1
        raise LinkedListValueError(f"Value {value} not found in linked list.")

    def update(self, index: int, value: Any) -> Any:
        """Update the value at the given index and return the old value.

        Valid range: 0 <= index < size.

        Raises:
            LinkedListIndexError: If index is out of range.
            LinkedListEmptyError: If list is empty.
        """
        if self._head is None:
            raise LinkedListEmptyError("Cannot update an empty linked list.")
        if index < 0 or index >= self._size:
            raise LinkedListIndexError(
                f"Index {index} out of range [0, {self._size - 1}]"
            )
        node = self._get_node_at(index)
        old_value = node.data
        node.data = value
        return old_value

    def get(self, index: int) -> Any:
        """Return the value at the given index.

        Valid range: 0 <= index < size.

        Raises:
            LinkedListIndexError: If index is out of range.
            LinkedListEmptyError: If list is empty.
        """
        if self._head is None:
            raise LinkedListEmptyError("Cannot get from an empty linked list.")
        if index < 0 or index >= self._size:
            raise LinkedListIndexError(
                f"Index {index} out of range [0, {self._size - 1}]"
            )
        return self._get_node_at(index).data

    def traverse(self) -> List[Any]:
        """Return elements from HEAD to TAIL as a list."""
        result = []
        current = self._head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def clear(self) -> None:
        """Remove all elements from the list."""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        elements = self.traverse()
        return " -> ".join(str(x) for x in elements) if elements else "Empty List"
