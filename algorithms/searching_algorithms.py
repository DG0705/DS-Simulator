"""Searching algorithms with array snapshots for the visualizer."""


LINEAR_SEARCH_CODE = (
    "def linear_search(values, target):",
    "    for index, value in enumerate(values):",
    "        if value == target:",
    "            return index",
    "    return -1",
)

BINARY_SEARCH_CODE = (
    "def binary_search(values, target):",
    "    low, high = 0, len(values) - 1",
    "    while low <= high:",
    "        middle = (low + high) // 2",
    "        if values[middle] == target:",
    "            return middle",
    "        if values[middle] < target:",
    "            low = middle + 1",
    "        else:",
    "            high = middle - 1",
    "    return -1",
)


class SearchSnapshot(list):
    """Array state plus the indices and source line for one search step."""

    def __init__(self, values, pointers=None, compared=None, code_line=None, matched=None):
        super().__init__(values)
        self.pointers = dict(pointers or {})
        self.compared = set(compared or ())
        self.code_line = code_line
        self.matched = matched

    def clone(self):
        return SearchSnapshot(self, self.pointers, self.compared, self.code_line, self.matched)


def linear_search(values, target, on_step=None):
    """Return the first matching index, or -1, using a left-to-right scan."""
    items = list(values)
    for index, value in enumerate(items):
        found = value == target
        if on_step:
            message = f"Compare {value} at position {index + 1} with target {target}."
            if found:
                message = f"Found target {target} at position {index + 1}."
            on_step(message, SearchSnapshot(items, {"i": index}, {index}, 3 if not found else 4, index if found else None))
        if found:
            return index
    if on_step:
        on_step(f"Target {target} was not found.", SearchSnapshot(items, code_line=5))
    return -1


def binary_search(values, target, on_step=None):
    """Return a matching index, or -1, in an ascending sorted sequence."""
    items = list(values)
    if any(items[index] > items[index + 1] for index in range(len(items) - 1)):
        raise ValueError("Binary Search requires values in ascending order.")

    low, high = 0, len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        value = items[middle]
        if value == target:
            if on_step:
                on_step(
                    f"Found target {target} at position {middle + 1}.",
                    SearchSnapshot(items, {"low": low, "mid": middle, "high": high}, {middle}, 6, middle),
                )
            return middle
        if on_step:
            on_step(
                f"Compare middle value {value} at position {middle + 1} with target {target}.",
                SearchSnapshot(items, {"low": low, "mid": middle, "high": high}, {middle}, 5),
            )
        if value < target:
            low = middle + 1
            line = 8
            message = f"{value} is smaller than {target}; continue in the right half."
        else:
            high = middle - 1
            line = 10
            message = f"{value} is larger than {target}; continue in the left half."
        if on_step:
            on_step(message, SearchSnapshot(items, {"low": low, "high": high}, code_line=line))

    if on_step:
        on_step(f"Target {target} was not found.", SearchSnapshot(items, code_line=11))
    return -1


SEARCH_FUNCTIONS = {
    "Linear Search": linear_search,
    "Binary Search": binary_search,
}


def searching_trace(name, values, target):
    """Return (steps, index) for the named search algorithm."""
    steps = []

    def record(description, snapshot):
        steps.append((description, snapshot.clone()))

    result = SEARCH_FUNCTIONS[name](values, target, on_step=record)
    return steps, result
