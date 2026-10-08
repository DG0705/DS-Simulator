import random
import unittest

from data_structures.avl import AVLTree
from data_structures.bst import BSTEmptyError, BSTValueError


def assert_avl_invariant(test_case, node):
    if node is None:
        return 0
    left_height = assert_avl_invariant(test_case, node.left)
    right_height = assert_avl_invariant(test_case, node.right)
    test_case.assertLessEqual(abs(left_height - right_height), 1)
    test_case.assertEqual(node.height, 1 + max(left_height, right_height))
    if node.left:
        test_case.assertLess(node.left.value, node.value)
    if node.right:
        test_case.assertGreater(node.right.value, node.value)
    return node.height


class AVLTreeTests(unittest.TestCase):
    def test_four_insertion_rotation_cases(self):
        for values in ([30, 20, 10], [10, 20, 30], [30, 10, 20], [10, 30, 20]):
            with self.subTest(values=values):
                tree = AVLTree()
                for value in values:
                    tree.insert(value)
                self.assertEqual(tree.root.value, 20)
                self.assertEqual(tree.inorder(), [10, 20, 30])
                self.assertEqual(tree.height(), 2)
                assert_avl_invariant(self, tree.root)

    def test_insert_delete_and_traversals(self):
        tree = AVLTree()
        values = [50, 20, 70, 10, 30, 60, 80, 25, 35, 65]
        for value in values:
            tree.insert(value)
        self.assertEqual(tree.size(), len(values))
        self.assertEqual(tree.find_min(), 10)
        self.assertEqual(tree.find_max(), 80)
        self.assertIsNotNone(tree.search(35))
        self.assertEqual(set(tree.level_order()), set(values))
        for value in (70, 20, 50, 10):
            self.assertEqual(tree.delete(value), value)
            self.assertIsNone(tree.search(value))
            assert_avl_invariant(self, tree.root)
        self.assertEqual(tree.inorder(), sorted(set(values) - {70, 20, 50, 10}))
        self.assertEqual(tree.size(), 6)

    def test_duplicates_missing_values_and_empty(self):
        tree = AVLTree()
        with self.assertRaises(BSTEmptyError):
            tree.delete(3)
        tree.insert(3)
        with self.assertRaises(BSTValueError):
            tree.insert(3)
        with self.assertRaises(BSTValueError):
            tree.delete(5)
        self.assertEqual(tree.inorder(), [3])
        self.assertEqual(tree.size(), 1)
        tree.clear()
        self.assertTrue(tree.is_empty())
        self.assertEqual(tree.height(), 0)

    def test_random_updates_preserve_balance(self):
        generator = random.Random(17)
        values = generator.sample(range(-500, 500), 150)
        tree = AVLTree()
        for value in values:
            tree.insert(value)
            assert_avl_invariant(self, tree.root)
        for value in generator.sample(values, len(values)):
            tree.delete(value)
            assert_avl_invariant(self, tree.root)
        self.assertTrue(tree.is_empty())

    def test_planned_inserts_show_each_rotation_type(self):
        cases = {
            "LL": [30, 20, 10],
            "RR": [10, 20, 30],
            "LR": [30, 10, 20],
            "RL": [10, 30, 20],
        }
        for rotation_type, values in cases.items():
            with self.subTest(rotation_type=rotation_type):
                tree = AVLTree()
                tree.insert(values[0])
                tree.insert(values[1])
                steps, planned = tree.plan_insert(values[2])
                self.assertEqual(tree.inorder(), sorted(values[:2]))
                self.assertEqual(planned.inorder(), [10, 20, 30])
                self.assertEqual(planned.root.value, 20)
                self.assertTrue(any(step.rotation_type == rotation_type for step in steps))
                self.assertTrue(any(step.rotation_values for step in steps))
                self.assertTrue(any("left height" in step.description for step in steps))
                self.assertEqual(steps[-1].root.value, 20)

    def test_planned_delete_shows_rebalance_and_preserves_original(self):
        tree = AVLTree()
        for value in (30, 20, 40, 10, 25):
            tree.insert(value)
        steps, planned = tree.plan_delete(40)
        self.assertEqual(tree.inorder(), [10, 20, 25, 30, 40])
        self.assertEqual(planned.inorder(), [10, 20, 25, 30])
        self.assertTrue(any(step.rotation_type == "LL" for step in steps))
        self.assertTrue(any("left height" in step.description for step in steps))
        self.assertEqual(steps[-1].root.value, planned.root.value)


if __name__ == "__main__":
    unittest.main()
