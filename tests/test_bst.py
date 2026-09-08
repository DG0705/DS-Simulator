import unittest
from data_structures.bst import BinarySearchTree, TreeNode, BSTError, BSTEmptyError, BSTValueError


class TestBSTInsert(unittest.TestCase):
    def test_insert_into_empty(self):
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertEqual(bst.size(), 1)
        self.assertEqual(bst.root.value, 10)

    def test_insert_left(self):
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(5)
        self.assertEqual(bst.size(), 2)
        self.assertEqual(bst.root.left.value, 5)

    def test_insert_right(self):
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(15)
        self.assertEqual(bst.size(), 2)
        self.assertEqual(bst.root.right.value, 15)

    def test_insert_multiple(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(v)
        self.assertEqual(bst.size(), 7)

    def test_insert_duplicate_raises(self):
        bst = BinarySearchTree()
        bst.insert(10)
        with self.assertRaises(BSTValueError):
            bst.insert(10)

    def test_insert_preserves_bst_property(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(v)
        self.assertEqual(bst.inorder(), [20, 30, 40, 50, 60, 70, 80])


class TestBSTSearch(unittest.TestCase):
    def test_search_empty(self):
        bst = BinarySearchTree()
        self.assertIsNone(bst.search(10))

    def test_search_found(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        node = bst.search(30)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 30)

    def test_search_not_found(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        self.assertIsNone(bst.search(25))

    def test_search_path(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40]:
            bst.insert(v)
        path = bst.search_path(20)
        self.assertEqual([n.value for n in path], [50, 30, 20])

    def test_search_path_not_found(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        path = bst.search_path(25)
        self.assertEqual([n.value for n in path], [50, 30])


class TestBSTDelete(unittest.TestCase):
    def test_delete_empty_raises(self):
        bst = BinarySearchTree()
        with self.assertRaises(BSTEmptyError):
            bst.delete(10)

    def test_delete_not_found_raises(self):
        bst = BinarySearchTree()
        bst.insert(10)
        with self.assertRaises(BSTValueError):
            bst.delete(20)

    def test_delete_leaf(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(v)
        deleted = bst.delete(20)
        self.assertEqual(deleted, 20)
        self.assertEqual(bst.size(), 6)
        self.assertIsNone(bst.search(20))

    def test_delete_one_child_left(self):
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(5)
        deleted = bst.delete(10)
        self.assertEqual(deleted, 10)
        self.assertEqual(bst.root.value, 5)

    def test_delete_one_child_right(self):
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(15)
        deleted = bst.delete(10)
        self.assertEqual(deleted, 10)
        self.assertEqual(bst.root.value, 15)

    def test_delete_two_children(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(v)
        deleted = bst.delete(50)
        self.assertEqual(deleted, 50)
        self.assertEqual(bst.size(), 6)
        self.assertEqual(bst.inorder(), [20, 30, 40, 60, 70, 80])

    def test_delete_root_two_children(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        deleted = bst.delete(50)
        self.assertEqual(deleted, 50)
        self.assertEqual(bst.size(), 2)
        self.assertIn(bst.root.value, [30, 70])


class TestBSTTraversals(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(v)

    def test_inorder(self):
        self.assertEqual(self.bst.inorder(), [20, 30, 40, 50, 60, 70, 80])

    def test_preorder(self):
        self.assertEqual(self.bst.preorder(), [50, 30, 20, 40, 70, 60, 80])

    def test_postorder(self):
        self.assertEqual(self.bst.postorder(), [20, 40, 30, 60, 80, 70, 50])

    def test_level_order(self):
        self.assertEqual(self.bst.level_order(), [50, 30, 70, 20, 40, 60, 80])

    def test_empty_traversals(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.inorder(), [])
        self.assertEqual(bst.preorder(), [])
        self.assertEqual(bst.postorder(), [])
        self.assertEqual(bst.level_order(), [])


class TestBSTMinMax(unittest.TestCase):
    def test_min(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40]:
            bst.insert(v)
        self.assertEqual(bst.find_min(), 20)

    def test_max(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40]:
            bst.insert(v)
        self.assertEqual(bst.find_max(), 70)

    def test_min_empty_raises(self):
        bst = BinarySearchTree()
        with self.assertRaises(BSTEmptyError):
            bst.find_min()

    def test_max_empty_raises(self):
        bst = BinarySearchTree()
        with self.assertRaises(BSTEmptyError):
            bst.find_max()

    def test_min_single(self):
        bst = BinarySearchTree()
        bst.insert(42)
        self.assertEqual(bst.find_min(), 42)

    def test_max_single(self):
        bst = BinarySearchTree()
        bst.insert(42)
        self.assertEqual(bst.find_max(), 42)


class TestBSTHeight(unittest.TestCase):
    def test_empty(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.height(), 0)

    def test_single(self):
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertEqual(bst.height(), 1)

    def test_balanced(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        self.assertEqual(bst.height(), 2)

    def test_unbalanced(self):
        bst = BinarySearchTree()
        for v in [10, 20, 30, 40]:
            bst.insert(v)
        self.assertEqual(bst.height(), 4)


class TestBSTSizeIsEmpty(unittest.TestCase):
    def test_size_empty(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.size(), 0)
        self.assertEqual(len(bst), 0)

    def test_size_after_inserts(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        self.assertEqual(bst.size(), 3)

    def test_size_after_delete(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        bst.delete(30)
        self.assertEqual(bst.size(), 2)

    def test_is_empty(self):
        bst = BinarySearchTree()
        self.assertTrue(bst.is_empty())
        bst.insert(10)
        self.assertFalse(bst.is_empty())

    def test_clear(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70]:
            bst.insert(v)
        bst.clear()
        self.assertEqual(bst.size(), 0)
        self.assertTrue(bst.is_empty())
        self.assertIsNone(bst.root)


class TestBSTGetAllNodes(unittest.TestCase):
    def test_empty(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.get_all_nodes(), [])

    def test_nodes_level_order(self):
        bst = BinarySearchTree()
        for v in [50, 30, 70, 20, 40]:
            bst.insert(v)
        nodes = bst.get_all_nodes()
        self.assertEqual([n.value for n in nodes], [50, 30, 70, 20, 40])


class TestBSTRepr(unittest.TestCase):
    def test_empty_repr(self):
        bst = BinarySearchTree()
        self.assertEqual(repr(bst), "BST({})")

    def test_repr(self):
        bst = BinarySearchTree()
        for v in [30, 10, 50]:
            bst.insert(v)
        self.assertEqual(repr(bst), "BST({10, 30, 50})")


if __name__ == "__main__":
    unittest.main()
