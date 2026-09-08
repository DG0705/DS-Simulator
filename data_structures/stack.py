from typing import Any, List


class StackError(Exception):
    """Base exception for Stack operations."""
    pass


class StackEmptyError(StackError):
    """Raised when operating on an empty stack."""
    pass


class StackValueError(StackError):
    """Raised when an invalid value is provided."""
    pass


class Stack:
    """Stack data structure implemented using a Python list.

    LIFO (Last In, First Out) principle.
    traverse() returns elements TOP -> BOTTOM (most recently pushed first).
    """

    def __init__(self) -> None:
        self._data: List[Any] = []

    def push(self, value: Any) -> None:
        """Push a value onto the top of the stack.

        Args:
            value: Value to push
        """
        self._data.append(value)

    def pop(self) -> Any:
        """Remove and return the top value.

        Returns:
            The value that was on top

        Raises:
            StackEmptyError: If stack is empty
        """
        if not self._data:
            raise StackEmptyError("Cannot pop from an empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """Return the top value without removing it.

        Returns:
            The value on top

        Raises:
            StackEmptyError: If stack is empty
        """
        if not self._data:
            raise StackEmptyError("Cannot peek at an empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._data) == 0

    def size(self) -> int:
        """Return the number of elements in the stack."""
        return len(self._data)

    def clear(self) -> None:
        """Remove all elements from the stack."""
        self._data.clear()

    def traverse(self) -> List[Any]:
        """Return elements in TOP -> BOTTOM order (most recently pushed first)."""
        return list(reversed(self._data))

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        top_to_bottom = list(reversed(self._data))
        return f"Stack(top -> {top_to_bottom})"
