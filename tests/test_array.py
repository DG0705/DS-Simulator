import unittest
from data_structures.array import Array, ArrayError, ArrayIndexError, ArrayValueError, ArrayEmptyError


class TestArray(unittest.TestCase):
    def setUp(self):
        self.array = Array()

    def test_append(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        self.assertEqual(self.array.size(), 3)
        self.assertEqual(self.array.traverse(), [10, 20, 30])

    def test_insert_at_beginning(self):
        self.array.append(20)
        self.array.append(30)
        self.array.insert(0, 10)
        self.assertEqual(self.array.traverse(), [10, 20, 30])

    def test_insert_at_end(self):
        self.array.append(10)
        self.array.append(20)
        self.array.insert(2, 30)
        self.assertEqual(self.array.traverse(), [10, 20, 30])

    def test_insert_in_middle(self):
        self.array.append(10)
        self.array.append(30)
        self.array.insert(1, 20)
        self.assertEqual(self.array.traverse(), [10, 20, 30])

    def test_insert_invalid_index_negative(self):
        with self.assertRaises(ArrayIndexError):
            self.array.insert(-1, 10)

    def test_insert_invalid_index_too_large(self):
        self.array.append(10)
        with self.assertRaises(ArrayIndexError):
            self.array.insert(2, 20)

    def test_delete_from_beginning(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        deleted = self.array.delete(0)
        self.assertEqual(deleted, 10)
        self.assertEqual(self.array.traverse(), [20, 30])

    def test_delete_from_end(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        deleted = self.array.delete(2)
        self.assertEqual(deleted, 30)
        self.assertEqual(self.array.traverse(), [10, 20])

    def test_delete_from_middle(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        deleted = self.array.delete(1)
        self.assertEqual(deleted, 20)
        self.assertEqual(self.array.traverse(), [10, 30])

    def test_delete_invalid_index_negative(self):
        self.array.append(10)
        with self.assertRaises(ArrayIndexError):
            self.array.delete(-1)

    def test_delete_invalid_index_too_large(self):
        self.array.append(10)
        with self.assertRaises(ArrayIndexError):
            self.array.delete(1)

    def test_delete_from_empty_array(self):
        with self.assertRaises(ArrayEmptyError):
            self.array.delete(0)

    def test_search_found(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        index = self.array.search(20)
        self.assertEqual(index, 1)

    def test_search_first_occurrence(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(20)
        self.array.append(30)
        index = self.array.search(20)
        self.assertEqual(index, 1)

    def test_search_not_found(self):
        self.array.append(10)
        self.array.append(20)
        with self.assertRaises(ArrayValueError):
            self.array.search(99)

    def test_search_empty_array(self):
        with self.assertRaises(ArrayEmptyError):
            self.array.search(10)

    def test_update(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        old = self.array.update(1, 25)
        self.assertEqual(old, 20)
        self.assertEqual(self.array.traverse(), [10, 25, 30])

    def test_update_invalid_index(self):
        self.array.append(10)
        with self.assertRaises(ArrayIndexError):
            self.array.update(1, 20)

    def test_update_empty_array(self):
        with self.assertRaises(ArrayEmptyError):
            self.array.update(0, 10)

    def test_get(self):
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        value = self.array.get(1)
        self.assertEqual(value, 20)

    def test_get_invalid_index(self):
        self.array.append(10)
        with self.assertRaises(ArrayIndexError):
            self.array.get(1)

    def test_get_empty_array(self):
        with self.assertRaises(ArrayEmptyError):
            self.array.get(0)

    def test_traverse(self):
        self.assertEqual(self.array.traverse(), [])
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        self.assertEqual(self.array.traverse(), [10, 20, 30])

    def test_clear(self):
        self.array.append(10)
        self.array.append(20)
        self.array.clear()
        self.assertEqual(self.array.size(), 0)
        self.assertTrue(self.array.is_empty())

    def test_size(self):
        self.assertEqual(self.array.size(), 0)
        self.array.append(10)
        self.assertEqual(self.array.size(), 1)
        self.array.append(20)
        self.assertEqual(self.array.size(), 2)
        self.array.delete(0)
        self.assertEqual(self.array.size(), 1)

    def test_is_empty(self):
        self.assertTrue(self.array.is_empty())
        self.array.append(10)
        self.assertFalse(self.array.is_empty())
        self.array.clear()
        self.assertTrue(self.array.is_empty())

    def test_duplicate_values(self):
        self.array.append(10)
        self.array.append(10)
        self.array.append(20)
        self.assertEqual(self.array.size(), 3)
        self.assertEqual(self.array.search(10), 0)
        self.array.delete(0)
        self.assertEqual(self.array.search(10), 0)

    def test_len_method(self):
        self.assertEqual(len(self.array), 0)
        self.array.append(10)
        self.assertEqual(len(self.array), 1)

    def test_getitem_setitem(self):
        self.array.append(10)
        self.array.append(20)
        self.assertEqual(self.array[0], 10)
        self.array[0] = 15
        self.assertEqual(self.array[0], 15)

    def test_repr(self):
        self.array.append(10)
        self.array.append(20)
        self.assertEqual(repr(self.array), "Array([10, 20])")


if __name__ == "__main__":
    unittest.main()