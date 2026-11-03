import unittest

from PyQt6.QtWidgets import QApplication

from visualization.heap_visualizer import HeapVisualizer


class TestHeapLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_complete_tree_levels_and_parent_alignment(self):
        view = HeapVisualizer()
        self.addCleanup(view.close)
        view.set_heap([78, 59, 67, 56, 34, 33, 66, 23])
        positions = view._paint_area._node_positions(8)
        for parent in range(3):
            left, right = positions[2 * parent + 1], positions[2 * parent + 2]
            self.assertEqual(left[1], right[1])
            self.assertEqual(left[1] - positions[parent][1], view.LEVEL_HEIGHT)
            self.assertAlmostEqual(positions[parent][0], (left[0] + right[0]) / 2)
        self.assertEqual(positions[7][1] - positions[3][1], view.LEVEL_HEIGHT)

    def test_nodes_stay_inside_canvas_after_resize(self):
        view = HeapVisualizer()
        self.addCleanup(view.close)
        view.show()
        for count in (1, 2, 8, 15, 32):
            view.set_heap(list(range(count)))
            for width in (600, 1000):
                view.resize(width, 650)
                self.app.processEvents()
                area = view._paint_area
                positions = area._node_positions(count)
                self.assertAlmostEqual(positions[0][0], area.width() / 2)
                self.assertGreaterEqual(positions[0][1] - area.NODE_RADIUS - 28, 0)
                for x, y in positions.values():
                    self.assertGreaterEqual(x - area.NODE_RADIUS, 0)
                    self.assertLessEqual(x + area.NODE_RADIUS, area.width())
                    self.assertLessEqual(y + area.NODE_RADIUS, area.height())
