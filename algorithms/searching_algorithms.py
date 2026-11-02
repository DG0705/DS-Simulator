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

JUMP_SEARCH_CODE = (
    "from math import sqrt",
    "def jump_search(values, target):",
    "    step = max(1, int(sqrt(len(values))))",
    "    start, end = 0, step",
    "    while start < len(values) and values[min(end, len(values)) - 1] < target:",
    "        start = end",
    "        end += step",
    "    for index in range(start, min(end, len(values))):",
    "        if values[index] == target:",
    "            return index",
    "        if values[index] > target:",
    "            break",
    "    return -1",
)

INTERPOLATION_SEARCH_CODE = (
    "def interpolation_search(values, target):",
    "    low, high = 0, len(values) - 1",
    "    while low <= high and values[low] <= target <= values[high]:",
    "        if values[low] == values[high]:",
    "            return low if values[low] == target else -1",
    "        middle = low + (target - values[low]) * (high - low) // (values[high] - values[low])",
    "        if values[middle] == target:",
    "            return middle",
    "        if values[middle] < target:",
    "            low = middle + 1",
    "        else:",
    "            high = middle - 1",
    "    return -1",
)

EXPONENTIAL_SEARCH_CODE = (
    "def exponential_search(values, target):",
    "    if not values:",
    "        return -1",
    "    if values[0] == target:",
    "        return 0",
    "    bound = 1",
    "    while bound < len(values) and values[bound] < target:",
    "        bound *= 2",
    "    low, high = bound // 2, min(bound, len(values) - 1)",
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


def _require_sorted(values, name):
    if any(values[index] > values[index + 1] for index in range(len(values) - 1)):
        raise ValueError(f"{name} requires values in ascending order.")


def jump_search(values, target, on_step=None):
    """Return the target index using square-root-sized jumps and a local scan."""
    items = list(values)
    _require_sorted(items, "Jump Search")
    length = len(items)
    if not length:
        if on_step:
            on_step(f"Target {target} was not found in the empty array.", SearchSnapshot(items, code_line=13))
        return -1

    step = max(1, int(len(items) ** 0.5))
    start, end = 0, step
    while start < length and items[min(end, length) - 1] < target:
        boundary = min(end, length) - 1
        if on_step:
            on_step(
                f"Block ending at position {boundary + 1} is below {target}; jump to the next block.",
                SearchSnapshot(items, {"start": start, "end": boundary}, {boundary}, 5),
            )
        start = end
        end += step

    if start < length and on_step:
        boundary = min(end, length) - 1
        on_step(
            f"Search linearly in positions {start + 1}–{boundary + 1}.",
            SearchSnapshot(items, {"start": start, "end": boundary}, code_line=8),
        )
    for index in range(start, min(end, length)):
        value = items[index]
        if on_step:
            on_step(
                f"Compare {value} at position {index + 1} with target {target}.",
                SearchSnapshot(items, {"i": index}, {index}, 9 if value != target else 10,
                               index if value == target else None),
            )
        if value == target:
            return index
        if value > target:
            if on_step:
                on_step("The current value is already greater than the target; stop this block scan.",
                        SearchSnapshot(items, {"i": index}, {index}, 12))
            break
    if on_step:
        on_step(f"Target {target} was not found.", SearchSnapshot(items, code_line=13))
    return -1


def interpolation_search(values, target, on_step=None):
    """Return the target index using value estimates in sorted integer data."""
    items = list(values)
    _require_sorted(items, "Interpolation Search")
    low, high = 0, len(items) - 1
    while low <= high and items[low] <= target <= items[high]:
        if items[low] == items[high]:
            if items[low] == target:
                if on_step:
                    on_step(f"All remaining values equal {target}; found it at position {low + 1}.",
                            SearchSnapshot(items, {"low": low, "high": high}, {low}, 5, low))
                return low
            break
        middle = low + ((target - items[low]) * (high - low) // (items[high] - items[low]))
        if on_step:
            on_step(
                f"Estimate position {middle + 1} from the target's value range.",
                SearchSnapshot(items, {"low": low, "mid": middle, "high": high}, {middle}, 6),
            )
        value = items[middle]
        if value == target:
            if on_step:
                on_step(f"Found target {target} at position {middle + 1}.",
                        SearchSnapshot(items, {"low": low, "mid": middle, "high": high}, {middle}, 8, middle))
            return middle
        if value < target:
            low = middle + 1
            line = 10
            message = f"{value} is smaller than {target}; continue to the right."
        else:
            high = middle - 1
            line = 12
            message = f"{value} is larger than {target}; continue to the left."
        if on_step:
            on_step(message, SearchSnapshot(items, {"low": low, "high": high}, code_line=line))
    if on_step:
        on_step(f"Target {target} was not found.", SearchSnapshot(items, code_line=13))
    return -1


def exponential_search(values, target, on_step=None):
    """Find a target by doubling a bound, then binary searching that range."""
    items = list(values)
    _require_sorted(items, "Exponential Search")
    length = len(items)
    if not length:
        if on_step:
            on_step(f"Target {target} was not found in the empty array.", SearchSnapshot(items, code_line=3))
        return -1
    if items[0] == target:
        if on_step:
            on_step(f"Found target {target} at position 1.", SearchSnapshot(items, {"i": 0}, {0}, 5, 0))
        return 0

    bound = 1
    while bound < length and items[bound] < target:
        if on_step:
            on_step(
                f"Value at position {bound + 1} is below {target}; double the search bound.",
                SearchSnapshot(items, {"i": bound}, {bound}, 7),
            )
        bound *= 2
        if on_step:
            on_step(f"Expand the bound to {bound}.", SearchSnapshot(items, {"i": min(bound, length - 1)}, code_line=8))

    low, high = bound // 2, min(bound, length - 1)
    while low <= high:
        middle = (low + high) // 2
        value = items[middle]
        if value == target:
            if on_step:
                on_step(f"Found target {target} at position {middle + 1}.",
                        SearchSnapshot(items, {"low": low, "mid": middle, "high": high}, {middle}, 13, middle))
            return middle
        if on_step:
            on_step(f"Compare {value} at position {middle + 1} within the bounded range.",
                    SearchSnapshot(items, {"low": low, "mid": middle, "high": high}, {middle}, 12))
        if value < target:
            low = middle + 1
            line = 15
            message = "The middle value is smaller; move the lower bound right."
        else:
            high = middle - 1
            line = 17
            message = "The middle value is larger; move the upper bound left."
        if on_step:
            on_step(message, SearchSnapshot(items, {"low": low, "high": high}, code_line=line))
    if on_step:
        on_step(f"Target {target} was not found.", SearchSnapshot(items, code_line=18))
    return -1


SEARCH_FUNCTIONS = {
    "Linear Search": linear_search,
    "Binary Search": binary_search,
    "Jump Search": jump_search,
    "Interpolation Search": interpolation_search,
    "Exponential Search": exponential_search,
}


def searching_trace(name, values, target):
    """Return (steps, index) for the named search algorithm."""
    steps = []

    def record(description, snapshot):
        steps.append((description, snapshot.clone()))

    result = SEARCH_FUNCTIONS[name](values, target, on_step=record)
    return steps, result
