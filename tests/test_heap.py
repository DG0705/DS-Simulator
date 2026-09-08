import unittest
from data_structures.heap import MaxHeap, HeapError, HeapEmptyError, HeapValueError


def _assert_valid_max_heap(heap: MaxHeap):
    """Helper: verify max-heap property for every parent."""
    data = heap.data
    for i in range(len(data)):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(data):
            assert data[i] >= data[left], (
                f"Heap property violated at parent {i} ({data[i]}) < left child ({data[left]})"
            )
        if right < len(data):
            assert data[i] >= data[right], (
                f"Heap property violated at parent {i} ({data[i]}) < right child ({data[right]})"
            )


class TestMaxHeapInsert(unittest.TestCase):
    def test_insert_empty(self):
        h = MaxHeap()
        h.insert(50)
        self.assertEqual(h.size(), 1)
        self.assertEqual(h.data, [50])

    def test_insert_multiple(self):
        h = MaxHeap()
        for v in [50, 30, 70]:
            h.insert(v)
        self.assertEqual(h.size(), 3)
        _assert_valid_max_heap(h)

    def test_insert_maintains_heap_property(self):
        h = MaxHeap()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            h.insert(v)
        self.assertEqual(h.size(), 7)
        _assert_valid_max_heap(h)
        self.assertEqual(h.data[0], 80)

    def test_insert_duplicates(self):
        h = MaxHeap()
        h.insert(50)
        h.insert(50)
        self.assertEqual(h.size(), 2)
        _assert_valid_max_heap(h)

    def test_insert_negatives(self):
        h = MaxHeap()
        for v in [-5, -1, -10]:
            h.insert(v)
        _assert_valid_max_heap(h)
        self.assertEqual(h.peek(), -1)

    def test_insert_zero(self):
        h = MaxHeap()
        h.insert(0)
        h.insert(5)
        _assert_valid_max_heap(h)
        self.assertEqual(h.peek(), 5)


class TestMaxHeapPeek(unittest.TestCase):
    def test_peek_empty_raises(self):
        h = MaxHeap()
        with self.assertRaises(HeapEmptyError):
            h.peek()

    def test_peek_single(self):
        h = MaxHeap()
        h.insert(42)
        self.assertEqual(h.peek(), 42)

    def test_peek_multiple(self):
        h = MaxHeap()
        for v in [50, 30, 70]:
            h.insert(v)
        self.assertEqual(h.peek(), 70)

    def test_peek_does_not_remove(self):
        h = MaxHeap()
        h.insert(50)
        h.insert(70)
        h.peek()
        self.assertEqual(h.size(), 2)


class TestMaxHeapExtractMax(unittest.TestCase):
    def test_extract_empty_raises(self):
        h = MaxHeap()
        with self.assertRaises(HeapEmptyError):
            h.extract_max()

    def test_extract_single(self):
        h = MaxHeap()
        h.insert(42)
        val = h.extract_max()
        self.assertEqual(val, 42)
        self.assertTrue(h.is_empty())

    def test_extract_max_value(self):
        h = MaxHeap()
        for v in [50, 30, 70, 20, 40]:
            h.insert(v)
        self.assertEqual(h.extract_max(), 70)

    def test_extract_maintains_heap_property(self):
        h = MaxHeap()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            h.insert(v)
        h.extract_max()
        _assert_valid_max_heap(h)
        self.assertEqual(h.data[0], 70)

    def test_extract_repeated(self):
        h = MaxHeap()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            h.insert(v)
        extracted = []
        while not h.is_empty():
            extracted.append(h.extract_max())
        self.assertEqual(extracted, [80, 70, 60, 50, 40, 30, 20])
        self.assertTrue(h.is_empty())

    def test_extract_last_node(self):
        h = MaxHeap()
        h.insert(10)
        val = h.extract_max()
        self.assertEqual(val, 10)
        self.assertTrue(h.is_empty())
        self.assertEqual(h.data, [])


class TestMaxHeapBuildHeap(unittest.TestCase):
    def test_build_empty(self):
        h = MaxHeap()
        h.build_heap([])
        self.assertTrue(h.is_empty())

    def test_build_heap(self):
        h = MaxHeap()
        h.build_heap([50, 30, 70, 20, 40, 60, 80])
        _assert_valid_max_heap(h)
        self.assertEqual(h.size(), 7)
        self.assertEqual(h.data[0], 80)

    def test_build_heap_single(self):
        h = MaxHeap()
        h.build_heap([42])
        _assert_valid_max_heap(h)
        self.assertEqual(h.peek(), 42)

    def test_build_heap_overwrites(self):
        h = MaxHeap()
        h.insert(100)
        h.insert(200)
        h.build_heap([50, 30, 70])
        _assert_valid_max_heap(h)
        self.assertEqual(h.size(), 3)
        self.assertEqual(h.data[0], 70)

    def test_build_heap_duplicates(self):
        h = MaxHeap()
        h.build_heap([50, 50, 50])
        _assert_valid_max_heap(h)
        self.assertEqual(h.size(), 3)
        self.assertEqual(h.peek(), 50)


class TestMaxHeapTraverse(unittest.TestCase):
    def test_traverse_empty(self):
        h = MaxHeap()
        self.assertEqual(h.traverse(), [])

    def test_traverse_level_order(self):
        h = MaxHeap()
        h.build_heap([50, 30, 70, 20, 40, 60, 80])
        result = h.traverse()
        self.assertEqual(result[0], 80)
        self.assertEqual(len(result), 7)

    def test_traverse_returns_copy(self):
        h = MaxHeap()
        h.insert(50)
        t = h.traverse()
        t.append(999)
        self.assertEqual(h.size(), 1)


class TestMaxHeapSizeIsEmpty(unittest.TestCase):
    def test_size_empty(self):
        h = MaxHeap()
        self.assertEqual(h.size(), 0)
        self.assertEqual(len(h), 0)

    def test_size_after_inserts(self):
        h = MaxHeap()
        for v in [50, 30, 70]:
            h.insert(v)
        self.assertEqual(h.size(), 3)

    def test_size_after_extracts(self):
        h = MaxHeap()
        for v in [50, 30, 70]:
            h.insert(v)
        h.extract_max()
        h.extract_max()
        self.assertEqual(h.size(), 1)

    def test_is_empty(self):
        h = MaxHeap()
        self.assertTrue(h.is_empty())
        h.insert(10)
        self.assertFalse(h.is_empty())

    def test_clear(self):
        h = MaxHeap()
        for v in [50, 30, 70]:
            h.insert(v)
        h.clear()
        self.assertEqual(h.size(), 0)
        self.assertTrue(h.is_empty())
        self.assertEqual(h.data, [])


class TestMaxHeapIsValid(unittest.TestCase):
    def test_valid_empty(self):
        h = MaxHeap()
        self.assertTrue(h.is_valid_heap())

    def test_valid_after_inserts(self):
        h = MaxHeap()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            h.insert(v)
        self.assertTrue(h.is_valid_heap())

    def test_valid_after_build(self):
        h = MaxHeap()
        h.build_heap([50, 30, 70, 20, 40, 60, 80])
        self.assertTrue(h.is_valid_heap())

    def test_valid_after_extract(self):
        h = MaxHeap()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            h.insert(v)
        h.extract_max()
        self.assertTrue(h.is_valid_heap())


class TestMaxHeapRepr(unittest.TestCase):
    def test_repr_empty(self):
        h = MaxHeap()
        self.assertEqual(repr(h), "MaxHeap({})")

    def test_repr(self):
        h = MaxHeap()
        h.insert(50)
        h.insert(30)
        self.assertIn("50", repr(h))
        self.assertIn("30", repr(h))


if __name__ == "__main__":
    unittest.main()
