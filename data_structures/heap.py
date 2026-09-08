from typing import Any, List


class HeapError(Exception):
    """Base exception for Heap operations."""
    pass


class HeapEmptyError(HeapError):
    """Raised when operating on an empty heap."""
    pass


class HeapValueError(HeapError):
    """Raised when an invalid value is provided."""
    pass


class MaxHeap:
    """Max Heap implementation using an array/list.

    Max Heap property: parent >= children.
    Zero-based indexing:
        parent(i) = (i - 1) // 2
        left(i) = 2*i + 1
        right(i) = 2*i + 2
    """

    def __init__(self) -> None:
        self._data: List[Any] = []

    @property
    def data(self) -> List[Any]:
        return list(self._data)

    def size(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _has_parent(self, i: int) -> bool:
        return i > 0

    def _has_left(self, i: int) -> bool:
        return self._left(i) < len(self._data)

    def _has_right(self, i: int) -> bool:
        return self._right(i) < len(self._data)

    def _heapify_up(self, i: int) -> None:
        """Restore heap property by moving node up. O(log n)."""
        while self._has_parent(i):
            parent_i = self._parent(i)
            if self._data[i] > self._data[parent_i]:
                self._swap(i, parent_i)
                i = parent_i
            else:
                break

    def _heapify_down(self, i: int) -> None:
        """Restore heap property by moving node down. O(log n)."""
        while True:
            largest = i
            left = self._left(i)
            right = self._right(i)

            if left < len(self._data) and self._data[left] > self._data[largest]:
                largest = left
            if right < len(self._data) and self._data[right] > self._data[largest]:
                largest = right

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def insert(self, value: Any) -> None:
        """Insert a value into the heap. O(log n)."""
        self._data.append(value)
        self._heapify_up(len(self._data) - 1)

    def peek(self) -> Any:
        """Return the maximum value without removing. O(1).

        Raises HeapEmptyError if empty.
        """
        if self.is_empty():
            raise HeapEmptyError("Cannot peek: the heap is empty.")
        return self._data[0]

    def extract_max(self) -> Any:
        """Remove and return the maximum value. O(log n).

        Raises HeapEmptyError if empty.
        """
        if self.is_empty():
            raise HeapEmptyError("Cannot extract maximum: the heap is empty.")
        max_val = self._data[0]
        last_val = self._data.pop()
        if self._data:
            self._data[0] = last_val
            self._heapify_down(0)
        return max_val

    def build_heap(self, values: List[Any]) -> None:
        """Build a heap from a list of values using bottom-up construction. O(n).

        Clears existing data before building.
        """
        self._data = list(values)
        if not self._data:
            return
        last_non_leaf = (len(self._data) // 2) - 1
        for i in range(last_non_leaf, -1, -1):
            self._heapify_down(i)

    def traverse(self) -> List[Any]:
        """Return the internal heap array representation. O(n).

        This is the level-order / array representation, NOT sorted order.
        """
        return list(self._data)

    def clear(self) -> None:
        """Remove all elements. O(1)."""
        self._data.clear()

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        vals = self._data
        return "MaxHeap({" + ", ".join(str(v) for v in vals) + "})" if vals else "MaxHeap({})"

    def is_valid_heap(self) -> bool:
        """Check if current array satisfies max-heap property. O(n)."""
        for i in range(len(self._data)):
            left = self._left(i)
            right = self._right(i)
            if left < len(self._data) and self._data[i] < self._data[left]:
                return False
            if right < len(self._data) and self._data[i] < self._data[right]:
                return False
        return True
