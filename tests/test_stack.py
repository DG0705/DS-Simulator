import unittest
from data_structures.stack import Stack, StackError, StackEmptyError, StackValueError


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

    def test_push_single(self):
        self.stack.push(10)
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), 10)

    def test_push_multiple(self):
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)
        self.assertEqual(self.stack.size(), 3)
        self.assertEqual(self.stack.peek(), 30)

    def test_pop_single(self):
        self.stack.push(10)
        popped = self.stack.pop()
        self.assertEqual(popped, 10)
        self.assertTrue(self.stack.is_empty())

    def test_pop_lifo_order(self):
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)
        self.assertEqual(self.stack.pop(), 30)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.pop(), 10)
        self.assertTrue(self.stack.is_empty())

    def test_pop_from_empty_stack(self):
        with self.assertRaises(StackEmptyError):
            self.stack.pop()

    def test_pop_error_message(self):
        with self.assertRaises(StackEmptyError) as ctx:
            self.stack.pop()
        self.assertIn("empty", str(ctx.exception).lower())

    def test_peek_single(self):
        self.stack.push(10)
        self.assertEqual(self.stack.peek(), 10)
        self.assertEqual(self.stack.size(), 1)

    def test_peek_does_not_remove(self):
        self.stack.push(10)
        self.stack.push(20)
        peeked = self.stack.peek()
        self.assertEqual(peeked, 20)
        self.assertEqual(self.stack.size(), 2)

    def test_peek_from_empty_stack(self):
        with self.assertRaises(StackEmptyError):
            self.stack.peek()

    def test_peek_error_message(self):
        with self.assertRaises(StackEmptyError) as ctx:
            self.stack.peek()
        self.assertIn("empty", str(ctx.exception).lower())

    def test_size(self):
        self.assertEqual(self.stack.size(), 0)
        self.stack.push(10)
        self.assertEqual(self.stack.size(), 1)
        self.stack.push(20)
        self.assertEqual(self.stack.size(), 2)
        self.stack.pop()
        self.assertEqual(self.stack.size(), 1)

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    def test_clear(self):
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)
        self.stack.clear()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

    def test_traverse_top_to_bottom(self):
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)
        self.assertEqual(self.stack.traverse(), [30, 20, 10])

    def test_traverse_empty(self):
        self.assertEqual(self.stack.traverse(), [])

    def test_duplicate_values(self):
        self.stack.push(10)
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.size(), 3)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.pop(), 10)
        self.assertEqual(self.stack.pop(), 10)

    def test_negative_integers(self):
        self.stack.push(-5)
        self.stack.push(-10)
        self.assertEqual(self.stack.pop(), -10)
        self.assertEqual(self.stack.pop(), -5)

    def test_zero(self):
        self.stack.push(0)
        self.assertEqual(self.stack.peek(), 0)
        self.assertEqual(self.stack.pop(), 0)

    def test_len_method(self):
        self.assertEqual(len(self.stack), 0)
        self.stack.push(10)
        self.assertEqual(len(self.stack), 1)
        self.stack.pop()
        self.assertEqual(len(self.stack), 0)

    def test_repr(self):
        self.stack.push(10)
        self.stack.push(20)
        r = repr(self.stack)
        self.assertIn("Stack", r)
        self.assertIn("20", r)
        self.assertIn("10", r)

    def test_push_pop_interleaved(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.pop(), 20)
        self.stack.push(30)
        self.assertEqual(self.stack.pop(), 30)
        self.assertEqual(self.stack.pop(), 10)
        self.assertTrue(self.stack.is_empty())


if __name__ == "__main__":
    unittest.main()
