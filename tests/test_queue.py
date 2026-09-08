import unittest
from data_structures.queue import Queue, QueueError, QueueEmptyError, QueueValueError


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_new_queue_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)

    def test_enqueue_single(self):
        self.queue.enqueue(10)
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.front(), 10)
        self.assertEqual(self.queue.rear(), 10)

    def test_enqueue_multiple(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)
        self.assertEqual(self.queue.size(), 3)
        self.assertEqual(self.queue.front(), 10)
        self.assertEqual(self.queue.rear(), 30)

    def test_fifo_behavior(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)
        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 20)
        self.assertEqual(self.queue.dequeue(), 30)
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_single(self):
        self.queue.enqueue(42)
        val = self.queue.dequeue()
        self.assertEqual(val, 42)
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_from_empty(self):
        with self.assertRaises(QueueEmptyError):
            self.queue.dequeue()

    def test_dequeue_error_message(self):
        with self.assertRaises(QueueEmptyError) as ctx:
            self.queue.dequeue()
        self.assertIn("empty", str(ctx.exception).lower())

    def test_front(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.front(), 10)
        self.assertEqual(self.queue.size(), 2)

    def test_front_from_empty(self):
        with self.assertRaises(QueueEmptyError):
            self.queue.front()

    def test_front_error_message(self):
        with self.assertRaises(QueueEmptyError) as ctx:
            self.queue.front()
        self.assertIn("empty", str(ctx.exception).lower())

    def test_rear(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.rear(), 20)
        self.assertEqual(self.queue.size(), 2)

    def test_rear_from_empty(self):
        with self.assertRaises(QueueEmptyError):
            self.queue.rear()

    def test_rear_error_message(self):
        with self.assertRaises(QueueEmptyError) as ctx:
            self.queue.rear()
        self.assertIn("empty", str(ctx.exception).lower())

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(10)
        self.assertFalse(self.queue.is_empty())
        self.queue.dequeue()
        self.assertTrue(self.queue.is_empty())

    def test_size(self):
        self.assertEqual(self.queue.size(), 0)
        self.queue.enqueue(10)
        self.assertEqual(self.queue.size(), 1)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.size(), 2)
        self.queue.dequeue()
        self.assertEqual(self.queue.size(), 1)

    def test_clear(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)

    def test_traverse(self):
        self.assertEqual(self.queue.traverse(), [])
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)
        self.assertEqual(self.queue.traverse(), [10, 20, 30])

    def test_traverse_after_dequeue(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)
        self.queue.dequeue()
        self.assertEqual(self.queue.traverse(), [20, 30])

    def test_duplicate_values(self):
        self.queue.enqueue(10)
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.size(), 3)
        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 20)

    def test_zero(self):
        self.queue.enqueue(0)
        self.assertEqual(self.queue.front(), 0)
        self.assertEqual(self.queue.rear(), 0)
        self.assertEqual(self.queue.dequeue(), 0)

    def test_negative_values(self):
        self.queue.enqueue(-5)
        self.queue.enqueue(-10)
        self.assertEqual(self.queue.front(), -5)
        self.assertEqual(self.queue.rear(), -10)
        self.assertEqual(self.queue.dequeue(), -5)
        self.assertEqual(self.queue.dequeue(), -10)

    def test_len_method(self):
        self.assertEqual(len(self.queue), 0)
        self.queue.enqueue(10)
        self.assertEqual(len(self.queue), 1)
        self.queue.dequeue()
        self.assertEqual(len(self.queue), 0)

    def test_repr(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        r = repr(self.queue)
        self.assertIn("Queue", r)
        self.assertIn("10", r)
        self.assertIn("20", r)

    def test_enqueue_dequeue_interleaved(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.dequeue(), 10)
        self.queue.enqueue(30)
        self.assertEqual(self.queue.dequeue(), 20)
        self.assertEqual(self.queue.dequeue(), 30)
        self.assertTrue(self.queue.is_empty())

    def test_large_sequence(self):
        for i in range(100):
            self.queue.enqueue(i)
        self.assertEqual(self.queue.size(), 100)
        for i in range(100):
            self.assertEqual(self.queue.dequeue(), i)
        self.assertTrue(self.queue.is_empty())

    def test_front_rear_after_operations(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)
        self.queue.dequeue()
        self.assertEqual(self.queue.front(), 20)
        self.assertEqual(self.queue.rear(), 30)


if __name__ == "__main__":
    unittest.main()
