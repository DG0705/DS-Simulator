"""Sorting algorithms used by the Sorting view.

Each function returns a sorted copy and leaves the input unchanged.
"""

QUICK_SORT_CODE = (
    "def quick_sort(a):",
    "    pending = [(0, len(a) - 1)]",
    "    while pending:",
    "        low, high = pending.pop()",
    "        if low >= high: continue",
    "        pivot_index = (low + high) // 2",
    "        pivot = a[pivot_index]",
    "        i, j = low, high",
    "        while i <= j:",
    "            while a[i] < pivot:",
    "                i += 1",
    "            while a[j] > pivot:",
    "                j -= 1",
    "            if i <= j:",
    "                a[i], a[j] = a[j], a[i]",
    "                i += 1",
    "                j -= 1",
    "        if low < j:",
    "            pending.append((low, j))",
    "        if i < high:",
    "            pending.append((i, high))",
    "    return a",
)


class PointerSnapshot(list):
    """Array snapshot with pointer positions for the sorting visualizer."""

    def __init__(self, values, pointers=None, compared=None, code_line=None):
        super().__init__(values)
        self.pointers = dict(pointers or {})
        self.compared = set(compared or ())
        self.code_line = code_line

    def clone(self):
        return PointerSnapshot(self, self.pointers, self.compared, self.code_line)


def quick_sort(values, on_step=None):
    result = list(values)
    if len(result) < 2:
        if on_step:
            on_step("The array has fewer than two values, so it is already sorted.", PointerSnapshot(result, code_line=22))
        return result

    pending = [(0, len(result) - 1)]
    if on_step:
        on_step("Add the full array as the first partition to process.", PointerSnapshot(result, code_line=2))
    while pending:
        low, high = pending.pop()
        if on_step:
            on_step(
                f"Take partition {low + 1}–{high + 1} from the pending stack.",
                PointerSnapshot(result, code_line=4),
            )
        if low >= high:
            if on_step:
                on_step("This partition has at most one value, so skip it.", PointerSnapshot(result, code_line=5))
            continue

        pivot_index = (low + high) // 2
        pivot = result[pivot_index]
        left, right = low, high
        if on_step:
            on_step(
                f"Choose {pivot} at position {pivot_index + 1} as the pivot for positions {low + 1}–{high + 1}. Set i to {left + 1} and j to {right + 1}.",
                PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, code_line=8),
            )
        while left <= right:
            while result[left] < pivot:
                if on_step:
                    on_step(
                        f"Compare i: {result[left]} < pivot {pivot}, so i must move right.",
                        PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, {left, pivot_index}, 10),
                    )
                left += 1
                if on_step:
                    on_step(
                        f"Increment i to position {left + 1}.",
                        PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, code_line=11),
                    )
            if on_step:
                on_step(
                    f"Compare i: {result[left]} is not less than pivot {pivot}, so i stops.",
                    PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, {left, pivot_index}, 10),
                )
            while result[right] > pivot:
                if on_step:
                    on_step(
                        f"Compare j: {result[right]} > pivot {pivot}, so j must move left.",
                        PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, {right, pivot_index}, 12),
                    )
                right -= 1
                if on_step:
                    on_step(
                        f"Decrement j to position {right + 1}.",
                        PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, code_line=13),
                    )
            if on_step:
                on_step(
                    f"Compare j: {result[right]} is not greater than pivot {pivot}, so j stops.",
                    PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, {right, pivot_index}, 12),
                )
            if left <= right:
                if on_step:
                    on_step(
                        f"i ({left + 1}) has not crossed j ({right + 1}); swap {result[left]} and {result[right]}.",
                        PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, {left, right}, 14),
                    )
                result[left], result[right] = result[right], result[left]
                if pivot_index == left:
                    pivot_index = right
                elif pivot_index == right:
                    pivot_index = left
                if on_step:
                    on_step(
                        "Swap complete.",
                        PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, {left, right}, 15),
                    )
                left += 1
                if on_step:
                    on_step(
                        f"Increment i to position {left + 1} after the swap.",
                        PointerSnapshot(result, {"i": left, "j": right, "pivot": pivot_index}, code_line=16),
                    )
                right -= 1
                if on_step:
                    pointers = {"pivot": pivot_index}
                    if left <= high:
                        pointers["i"] = left
                    if right >= low:
                        pointers["j"] = right
                    on_step(
                        f"Decrement j to position {right + 1} after the swap." if right >= low else "Decrement j past the start of this partition.",
                        PointerSnapshot(result, pointers, code_line=17),
                    )

        if on_step:
            on_step(
                f"i and j have crossed. Partition {low + 1}–{high + 1} is complete.",
                PointerSnapshot(result, {"pivot": pivot_index}, code_line=9),
            )

        if low < right:
            pending.append((low, right))
            if on_step:
                on_step(
                    f"Add left partition {low + 1}–{right + 1} to the pending stack.",
                    PointerSnapshot(result, code_line=19),
                )
        if left < high:
            pending.append((left, high))
            if on_step:
                on_step(
                    f"Add right partition {left + 1}–{high + 1} to the pending stack.",
                    PointerSnapshot(result, code_line=21),
                )

    if on_step:
        on_step("No partitions remain; return the sorted array.", PointerSnapshot(result, code_line=22))
    return result


def merge_sort(values, on_step=None):
    result = list(values)
    length = len(result)
    buffer = result.copy()
    if length < 2 and on_step:
        on_step("Already sorted", result)
    width = 1
    while width < length:
        working = result.copy()
        for start in range(0, length, 2 * width):
            middle = min(start + width, length)
            end = min(start + 2 * width, length)
            left, right = start, middle
            if on_step:
                working[start:end] = [None] * (end - start)
            for index in range(start, end):
                if right >= end or (left < middle and result[left] <= result[right]):
                    buffer[index] = result[left]
                    left += 1
                else:
                    buffer[index] = result[right]
                    right += 1
                if on_step:
                    working[index] = buffer[index]
                    on_step(f"Merge runs of size {width}: place {buffer[index]} at position {index + 1}", working)
        result, buffer = buffer, result
        width *= 2
    return result


def radix_sort(values, on_step=None):
    """LSD radix sort for integers, including negative values."""
    numbers = list(values)
    if any(not isinstance(value, int) for value in numbers):
        raise TypeError("Radix sort requires integer values.")

    if len(numbers) < 2:
        if on_step:
            on_step("Already sorted", numbers)
        return numbers

    # Shifting every value by the same amount preserves its ordering while
    # making the digit passes work for negative integers too.
    offset = max(0, -min(numbers))
    items = [value + offset for value in numbers]
    maximum = max(items)
    exponent = 1
    while maximum // exponent:
        counts = [0] * 10
        for item in items:
            counts[(item // exponent) % 10] += 1
        for digit in range(1, 10):
            counts[digit] += counts[digit - 1]
        output = [None] * len(items)
        for item in reversed(items):
            digit = (item // exponent) % 10
            counts[digit] -= 1
            index = counts[digit]
            output[index] = item
            if on_step:
                snapshot = [value - offset if value is not None else None for value in output]
                on_step(
                    f"Digit {exponent}: place {item - offset} at position {index + 1}",
                    snapshot,
                )
        items = output
        exponent *= 10
    if exponent == 1 and on_step:
        on_step("All values are equal", numbers)
    return [item - offset for item in items]


SORTING_FUNCTIONS = {
    "Radix Sort": radix_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}


def sorting_trace(name, values):
    """Return (steps, result), with one full-array snapshot per algorithm pass."""
    steps = []

    def record(description, snapshot):
        steps.append((description, snapshot.clone() if isinstance(snapshot, PointerSnapshot) else list(snapshot)))

    result = SORTING_FUNCTIONS[name](values, on_step=record)
    return steps, result
