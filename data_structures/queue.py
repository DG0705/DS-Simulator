from collections import deque
from typing import Any, List


class QueueError(Exception):
    """Base exception for Queue operations."""
    pass


class QueueEmptyError(QueueError):
    """Raised when operating on an empty queue."""
    pass


class QueueValueError(QueueError):
    """Raised when an invalid value is provided."""
    pass


class Queue:
    """Linear Queue data structure implemented using collections.deque.

    FIFO (First In, First Out) principle.

    - enqueue(value): adds to REAR
    - dequeue(): removes from FRONT
    - front(): returns FRONT without removing
    - rear(): returns REAR without removing
    - traverse(): returns elements from FRONT to REAR
    """

    def __init__(self) -> None:
        self._data: deque = deque()

    def enqueue(self, value: Any) -> None:
        """Add a value to the rear of the queue.

        Args:
            value: Value to enqueue
        """
        self._data.append(value)

    def dequeue(self) -> Any:
        """Remove and return the front value.

        Returns:
            The value that was at the front

        Raises:
            QueueEmptyError: If queue is empty
        """
        if not self._data:
            raise QueueEmptyError("Cannot dequeue from an empty queue")
        return self._data.popleft()

    def front(self) -> Any:
        """Return the front value without removing it.

        Returns:
            The value at the front

        Raises:
            QueueEmptyError: If queue is empty
        """
        if not self._data:
            raise QueueEmptyError("Cannot get front of an empty queue")
        return self._data[0]

    def rear(self) -> Any:
        """Return the rear value without removing it.

        Returns:
            The value at the rear

        Raises:
            QueueEmptyError: If queue is empty
        """
        if not self._data:
            raise QueueEmptyError("Cannot get rear of an empty queue")
        return self._data[-1]

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._data) == 0

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._data)

    def clear(self) -> None:
        """Remove all elements from the queue."""
        self._data.clear()

    def traverse(self) -> List[Any]:
        """Return elements from FRONT to REAR."""
        return list(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        front_to_rear = list(self._data)
        return f"Queue(front -> {front_to_rear} <- rear)"
