from typing import Any, List, Optional


class ArrayError(Exception):
    """Base exception for Array operations."""
    pass


class ArrayIndexError(ArrayError):
    """Raised when an invalid index is accessed."""
    pass


class ArrayValueError(ArrayError):
    """Raised when an invalid value is provided."""
    pass


class ArrayEmptyError(ArrayError):
    """Raised when operating on an empty array."""
    pass


class Array:
    """Array data structure implemented using a Python list."""

    def __init__(self) -> None:
        self._data: List[Any] = []

    def insert(self, index: int, value: Any) -> None:
        """Insert a value at the specified index.
        
        Args:
            index: Position to insert the value (0 <= index <= size)
            value: Value to insert
            
        Raises:
            ArrayIndexError: If index is out of valid range
        """
        if index < 0 or index > len(self._data):
            raise ArrayIndexError(f"Index {index} out of range [0, {len(self._data)}]")
        self._data.insert(index, value)

    def append(self, value: Any) -> None:
        """Append a value to the end of the array.
        
        Args:
            value: Value to append
        """
        self._data.append(value)

    def delete(self, index: int) -> Any:
        """Delete and return the value at the specified index.
        
        Args:
            index: Position to delete (0 <= index < size)
            
        Returns:
            The deleted value
            
        Raises:
            ArrayIndexError: If index is out of range
            ArrayEmptyError: If array is empty
        """
        if not self._data:
            raise ArrayEmptyError("Cannot delete from an empty array")
        if index < 0 or index >= len(self._data):
            raise ArrayIndexError(f"Index {index} out of range [0, {len(self._data) - 1}]")
        return self._data.pop(index)

    def search(self, value: Any) -> int:
        """Search for a value and return its first index.
        
        Args:
            value: Value to search for
            
        Returns:
            Index of the first occurrence of value
            
        Raises:
            ArrayEmptyError: If array is empty
            ArrayValueError: If value is not found
        """
        if not self._data:
            raise ArrayEmptyError("Cannot search an empty array")
        try:
            return self._data.index(value)
        except ValueError:
            raise ArrayValueError(f"Value {value} not found in array")

    def update(self, index: int, value: Any) -> Any:
        """Update the value at the specified index.
        
        Args:
            index: Position to update (0 <= index < size)
            value: New value
            
        Returns:
            The old value at that index
            
        Raises:
            ArrayIndexError: If index is out of range
            ArrayEmptyError: If array is empty
        """
        if not self._data:
            raise ArrayEmptyError("Cannot update an empty array")
        if index < 0 or index >= len(self._data):
            raise ArrayIndexError(f"Index {index} out of range [0, {len(self._data) - 1}]")
        old_value = self._data[index]
        self._data[index] = value
        return old_value

    def get(self, index: int) -> Any:
        """Get the value at the specified index.
        
        Args:
            index: Position to get (0 <= index < size)
            
        Returns:
            The value at the specified index
            
        Raises:
            ArrayIndexError: If index is out of range
            ArrayEmptyError: If array is empty
        """
        if not self._data:
            raise ArrayEmptyError("Cannot get from an empty array")
        if index < 0 or index >= len(self._data):
            raise ArrayIndexError(f"Index {index} out of range [0, {len(self._data) - 1}]")
        return self._data[index]

    def size(self) -> int:
        """Return the number of elements in the array."""
        return len(self._data)

    def clear(self) -> None:
        """Remove all elements from the array."""
        self._data.clear()

    def traverse(self) -> List[Any]:
        """Return a copy of all elements in order."""
        return self._data.copy()

    def is_empty(self) -> bool:
        """Check if the array is empty."""
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> Any:
        return self.get(index)

    def __setitem__(self, index: int, value: Any) -> None:
        self.update(index, value)

    def __repr__(self) -> str:
        return f"Array({self._data})"