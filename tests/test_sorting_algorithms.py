import random
import unittest

from algorithms.sorting_algorithms import merge_sort, quick_sort, radix_sort, sorting_trace


class SortingAlgorithmTests(unittest.TestCase):
    def test_algorithms_match_sorted_for_integer_inputs(self):
        samples = [
            [], [7], [5, 1, 5, -4, 0, -4, 12],
            list(range(30)), list(range(30, -1, -1)),
            [0, -1000, 9999, -1, 10, 10, 0],
        ]
        generator = random.Random(42)
        samples.extend(
            [generator.randint(-10000, 10000) for _ in range(length)]
            for length in (2, 10, 100, 501)
        )
        for algorithm in (radix_sort, quick_sort, merge_sort):
            for sample in samples:
                with self.subTest(algorithm=algorithm.__name__, sample=sample[:5]):
                    original = sample.copy()
                    self.assertEqual(algorithm(sample), sorted(sample))
                    self.assertEqual(sample, original)

    def test_radix_sort_rejects_non_integers(self):
        with self.assertRaises(TypeError):
            radix_sort([1, 2.5])

    def test_traces_end_with_sorted_snapshot(self):
        values = [43, -5, 8, 3, 8, 0]
        for name in ("Radix Sort", "Quick Sort", "Merge Sort"):
            with self.subTest(name=name):
                steps, result = sorting_trace(name, values)
                self.assertTrue(steps)
                self.assertTrue(all(len(snapshot) == len(values) for _, snapshot in steps))
                self.assertEqual(steps[-1][1], sorted(values))
                self.assertEqual(result, sorted(values))
                self.assertEqual(values, [43, -5, 8, 3, 8, 0])

    def test_one_digit_radix_reveals_each_placement(self):
        values = [9, 8, 7, 4, 3, 1]
        steps, result = sorting_trace("Radix Sort", values)
        self.assertEqual(len(steps), len(values))
        self.assertEqual(
            [sum(item is not None for item in snapshot) for _, snapshot in steps],
            list(range(1, len(values) + 1)),
        )
        self.assertEqual(result, [1, 3, 4, 7, 8, 9])

    def test_quick_sort_trace_exposes_pointer_comparisons_and_moves(self):
        steps, result = sorting_trace("Quick Sort", [8, 3, 7, 1, 5])
        descriptions = [description for description, _ in steps]
        self.assertEqual(result, [1, 3, 5, 7, 8])
        self.assertTrue(any("Compare i" in text for text in descriptions))
        self.assertTrue(any("Compare j" in text for text in descriptions))
        self.assertTrue(any("Increment i" in text for text in descriptions))
        self.assertTrue(any("Decrement j" in text for text in descriptions))
        self.assertTrue(any("pivot" in getattr(snapshot, "pointers", {}) for _, snapshot in steps))
        self.assertTrue(all(getattr(snapshot, "code_line", None) for _, snapshot in steps))
        self.assertEqual(steps[-1][1].code_line, 22)


if __name__ == "__main__":
    unittest.main()
