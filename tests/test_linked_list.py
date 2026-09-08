import unittest
from data_structures.linked_list import (
    SinglyLinkedList, Node,
    LinkedListError, LinkedListEmptyError, LinkedListIndexError, LinkedListValueError,
)


class TestNode(unittest.TestCase):
    def test_node_creation(self):
        node = Node(10)
        self.assertEqual(node.data, 10)
        self.assertIsNone(node.next)

    def test_node_with_next(self):
        n2 = Node(20)
        n1 = Node(10, n2)
        self.assertEqual(n1.data, 10)
        self.assertIs(n1.next, n2)

    def test_node_repr(self):
        node = Node(42)
        self.assertEqual(repr(node), "Node(42)")


class TestSinglyLinkedList(unittest.TestCase):
    def setUp(self):
        self.ll = SinglyLinkedList()

    # --- Empty list ---
    def test_empty_list(self):
        self.assertTrue(self.ll.is_empty())
        self.assertEqual(self.ll.size(), 0)
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)
        self.assertEqual(self.ll.traverse(), [])

    # --- Insert at head ---
    def test_insert_at_head_single(self):
        self.ll.insert_at_head(10)
        self.assertEqual(self.ll.size(), 1)
        self.assertEqual(self.ll.head.data, 10)
        self.assertEqual(self.ll.tail.data, 10)
        self.assertIsNone(self.ll.head.next)

    def test_insert_at_head_multiple(self):
        self.ll.insert_at_head(30)
        self.ll.insert_at_head(20)
        self.ll.insert_at_head(10)
        self.assertEqual(self.ll.traverse(), [10, 20, 30])
        self.assertEqual(self.ll.head.data, 10)
        self.assertEqual(self.ll.tail.data, 30)

    def test_insert_at_head_head_tail_consistency(self):
        self.ll.insert_at_head(10)
        self.ll.insert_at_head(20)
        self.assertEqual(self.ll.head.data, 20)
        self.assertEqual(self.ll.head.next.data, 10)
        self.assertEqual(self.ll.tail.data, 10)

    # --- Insert at tail ---
    def test_insert_at_tail_single(self):
        self.ll.insert_at_tail(10)
        self.assertEqual(self.ll.size(), 1)
        self.assertEqual(self.ll.head.data, 10)
        self.assertEqual(self.ll.tail.data, 10)
        self.assertIsNone(self.ll.head.next)

    def test_insert_at_tail_multiple(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        self.assertEqual(self.ll.traverse(), [10, 20, 30])
        self.assertEqual(self.ll.head.data, 10)
        self.assertEqual(self.ll.tail.data, 30)

    # --- Insert at index ---
    def test_insert_at_index_beginning(self):
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        self.ll.insert_at_index(0, 10)
        self.assertEqual(self.ll.traverse(), [10, 20, 30])
        self.assertEqual(self.ll.head.data, 10)

    def test_insert_at_index_end(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_index(2, 30)
        self.assertEqual(self.ll.traverse(), [10, 20, 30])
        self.assertEqual(self.ll.tail.data, 30)

    def test_insert_at_index_middle(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(30)
        self.ll.insert_at_index(1, 20)
        self.assertEqual(self.ll.traverse(), [10, 20, 30])

    def test_insert_at_index_single_into_empty(self):
        self.ll.insert_at_index(0, 42)
        self.assertEqual(self.ll.traverse(), [42])
        self.assertEqual(self.ll.head.data, 42)
        self.assertEqual(self.ll.tail.data, 42)

    def test_insert_at_index_invalid_negative(self):
        with self.assertRaises(LinkedListIndexError):
            self.ll.insert_at_index(-1, 10)

    def test_insert_at_index_invalid_too_large(self):
        self.ll.insert_at_tail(10)
        with self.assertRaises(LinkedListIndexError):
            self.ll.insert_at_index(2, 20)

    # --- Delete head ---
    def test_delete_head_single(self):
        self.ll.insert_at_tail(10)
        val = self.ll.delete_head()
        self.assertEqual(val, 10)
        self.assertTrue(self.ll.is_empty())
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

    def test_delete_head_multiple(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        val = self.ll.delete_head()
        self.assertEqual(val, 10)
        self.assertEqual(self.ll.traverse(), [20, 30])
        self.assertEqual(self.ll.head.data, 20)

    def test_delete_head_empty(self):
        with self.assertRaises(LinkedListEmptyError):
            self.ll.delete_head()

    def test_delete_head_error_message(self):
        with self.assertRaises(LinkedListEmptyError) as ctx:
            self.ll.delete_head()
        self.assertIn("empty", str(ctx.exception).lower())

    # --- Delete tail ---
    def test_delete_tail_single(self):
        self.ll.insert_at_tail(10)
        val = self.ll.delete_tail()
        self.assertEqual(val, 10)
        self.assertTrue(self.ll.is_empty())
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

    def test_delete_tail_multiple(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        val = self.ll.delete_tail()
        self.assertEqual(val, 30)
        self.assertEqual(self.ll.traverse(), [10, 20])
        self.assertEqual(self.ll.tail.data, 20)

    def test_delete_tail_empty(self):
        with self.assertRaises(LinkedListEmptyError):
            self.ll.delete_tail()

    def test_delete_tail_error_message(self):
        with self.assertRaises(LinkedListEmptyError) as ctx:
            self.ll.delete_tail()
        self.assertIn("empty", str(ctx.exception).lower())

    def test_delete_tail_head_tail_same(self):
        self.ll.insert_at_tail(10)
        val = self.ll.delete_tail()
        self.assertEqual(val, 10)
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

    # --- Delete at index ---
    def test_delete_at_index_beginning(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        val = self.ll.delete_at_index(0)
        self.assertEqual(val, 10)
        self.assertEqual(self.ll.traverse(), [20, 30])
        self.assertEqual(self.ll.head.data, 20)

    def test_delete_at_index_end(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        val = self.ll.delete_at_index(2)
        self.assertEqual(val, 30)
        self.assertEqual(self.ll.traverse(), [10, 20])
        self.assertEqual(self.ll.tail.data, 20)

    def test_delete_at_index_middle(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        val = self.ll.delete_at_index(1)
        self.assertEqual(val, 20)
        self.assertEqual(self.ll.traverse(), [10, 30])

    def test_delete_at_index_invalid(self):
        self.ll.insert_at_tail(10)
        with self.assertRaises(LinkedListIndexError):
            self.ll.delete_at_index(1)

    def test_delete_at_index_empty(self):
        with self.assertRaises(LinkedListEmptyError):
            self.ll.delete_at_index(0)

    # --- Search ---
    def test_search_found(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        idx = self.ll.search(20)
        self.assertEqual(idx, 1)

    def test_search_first_occurrence(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(20)
        idx = self.ll.search(20)
        self.assertEqual(idx, 1)

    def test_search_not_found(self):
        self.ll.insert_at_tail(10)
        with self.assertRaises(LinkedListValueError):
            self.ll.search(99)

    def test_search_empty(self):
        with self.assertRaises(LinkedListEmptyError):
            self.ll.search(10)

    def test_search_error_message(self):
        self.ll.insert_at_tail(10)
        with self.assertRaises(LinkedListValueError) as ctx:
            self.ll.search(99)
        self.assertIn("not found", str(ctx.exception).lower())

    # --- Update ---
    def test_update(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        old = self.ll.update(1, 99)
        self.assertEqual(old, 20)
        self.assertEqual(self.ll.traverse(), [10, 99])

    def test_update_invalid_index(self):
        self.ll.insert_at_tail(10)
        with self.assertRaises(LinkedListIndexError):
            self.ll.update(1, 20)

    def test_update_empty(self):
        with self.assertRaises(LinkedListEmptyError):
            self.ll.update(0, 10)

    # --- Get ---
    def test_get(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.assertEqual(self.ll.get(0), 10)
        self.assertEqual(self.ll.get(1), 20)

    def test_get_invalid_index(self):
        self.ll.insert_at_tail(10)
        with self.assertRaises(LinkedListIndexError):
            self.ll.get(1)

    def test_get_empty(self):
        with self.assertRaises(LinkedListEmptyError):
            self.ll.get(0)

    # --- Traverse ---
    def test_traverse_empty(self):
        self.assertEqual(self.ll.traverse(), [])

    def test_traverse(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        self.assertEqual(self.ll.traverse(), [10, 20, 30])

    # --- Size ---
    def test_size(self):
        self.assertEqual(self.ll.size(), 0)
        self.ll.insert_at_head(10)
        self.assertEqual(self.ll.size(), 1)
        self.ll.insert_at_tail(20)
        self.assertEqual(self.ll.size(), 2)
        self.ll.delete_head()
        self.assertEqual(self.ll.size(), 1)

    def test_len_method(self):
        self.assertEqual(len(self.ll), 0)
        self.ll.insert_at_tail(10)
        self.assertEqual(len(self.ll), 1)

    # --- Is empty ---
    def test_is_empty(self):
        self.assertTrue(self.ll.is_empty())
        self.ll.insert_at_head(10)
        self.assertFalse(self.ll.is_empty())
        self.ll.delete_head()
        self.assertTrue(self.ll.is_empty())

    # --- Clear ---
    def test_clear(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        self.ll.clear()
        self.assertTrue(self.ll.is_empty())
        self.assertEqual(self.ll.size(), 0)
        self.assertIsNone(self.ll.head)
        self.assertIsNone(self.ll.tail)

    # --- Duplicate values ---
    def test_duplicate_values(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.assertEqual(self.ll.size(), 3)
        self.assertEqual(self.ll.search(10), 0)
        self.ll.delete_head()
        self.assertEqual(self.ll.search(10), 0)

    # --- Zero ---
    def test_zero(self):
        self.ll.insert_at_tail(0)
        self.assertEqual(self.ll.head.data, 0)
        self.assertEqual(self.ll.get(0), 0)

    # --- Negative values ---
    def test_negative_values(self):
        self.ll.insert_at_tail(-5)
        self.ll.insert_at_tail(-10)
        self.assertEqual(self.ll.traverse(), [-5, -10])
        self.assertEqual(self.ll.get(0), -5)

    # --- Repr ---
    def test_repr(self):
        self.assertEqual(repr(self.ll), "Empty List")
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.assertEqual(repr(self.ll), "10 -> 20")

    # --- HEAD/TAIL pointer correctness ---
    def test_head_tail_after_operations(self):
        self.ll.insert_at_head(20)
        self.ll.insert_at_head(10)
        self.ll.insert_at_tail(30)
        self.assertEqual(self.ll.head.data, 10)
        self.assertEqual(self.ll.tail.data, 30)
        self.ll.delete_head()
        self.assertEqual(self.ll.head.data, 20)
        self.ll.delete_tail()
        self.assertEqual(self.ll.head.data, 20)
        self.assertEqual(self.ll.tail.data, 20)

    # --- Node chain integrity ---
    def test_node_chain_integrity(self):
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)
        node = self.ll.head
        count = 0
        while node is not None:
            count += 1
            node = node.next
        self.assertEqual(count, 3)
        self.assertIsNone(node)

    # --- Interleaved operations ---
    def test_interleaved_operations(self):
        self.ll.insert_at_head(20)
        self.ll.insert_at_tail(30)
        self.ll.insert_at_head(10)
        self.assertEqual(self.ll.traverse(), [10, 20, 30])
        self.ll.delete_tail()
        self.assertEqual(self.ll.traverse(), [10, 20])
        self.ll.insert_at_index(1, 15)
        self.assertEqual(self.ll.traverse(), [10, 15, 20])


if __name__ == "__main__":
    unittest.main()
