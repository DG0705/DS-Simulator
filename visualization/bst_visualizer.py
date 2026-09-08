from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QFontMetrics

from app.core.constants import (
    BG_SURFACE, TEXT_PRIMARY, TEXT_ON_ACCENT, ACCENT_PRIMARY,
    ACCENT_PRIMARY_LIGHT, ACCENT_SUCCESS_LIGHT, ACCENT_WARNING_LIGHT,
    BORDER_LIGHT, SCROLLBAR_STYLE
)


class BSTVisualizer(QWidget):
    """Visualizes a Binary Search Tree with hierarchical layout."""

    NODE_RADIUS = 24
    LEVEL_HEIGHT = 70
    MIN_SPACING = 20
    PADDING = 40

    def __init__(self, parent=None):
        super().__init__(parent)
        self._nodes = []
        self._positions = {}
        self._highlighted = set()
        self._new_node = None
        self._feedback = ""
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(f"background-color: {BG_SURFACE};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll_area.setStyleSheet(SCROLLBAR_STYLE)

        self._canvas = QWidget()
        self._canvas.setMinimumSize(400, 300)
        self._paint_area = _PaintArea(self)
        self._paint_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        canvas_layout = QVBoxLayout(self._canvas)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.addWidget(self._paint_area)
        self._scroll_area.setWidget(self._canvas)
        layout.addWidget(self._scroll_area)

        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setStyleSheet(
            f"font-size: 13px; color: {TEXT_PRIMARY}; "
            f"padding: 8px; background-color: {BG_SURFACE}; "
            f"border-top: 1px solid {BORDER_LIGHT};"
        )
        self._feedback_label.setFixedHeight(36)
        layout.addWidget(self._feedback_label)

    def set_tree(self, bst_root, highlight_path=None, new_value=None):
        self._nodes = []
        self._highlighted = set()
        self._new_node = new_value

        if highlight_path:
            self._highlighted = {id(n) for n in highlight_path}

        if bst_root:
            self._compute_positions(bst_root)
        else:
            self._positions = {}

        self._paint_area.update()
        self._update_canvas_size()

    def _compute_positions(self, root):
        if root is None:
            self._positions = {}
            return

        positions = {}
        min_x = [0]

        def assign_positions(node, depth, x_min, x_max):
            if node is None:
                return
            x = (x_min + x_max) / 2
            y = self.PADDING + depth * self.LEVEL_HEIGHT
            positions[id(node)] = (x, y, node.value, node)
            min_x[0] = min(min_x[0], x - self.NODE_RADIUS)
            assign_positions(node.left, depth + 1, x_min, x)
            assign_positions(node.right, depth + 1, x, x_max)

        import math
        depth = self._get_depth(root)
        width = max(1, 2 ** (depth - 1)) * (self.NODE_RADIUS * 2 + self.MIN_SPACING)
        assign_positions(root, 0, -width / 2, width / 2)
        self._positions = positions

    def _get_depth(self, node):
        if node is None:
            return 0
        return 1 + max(self._get_depth(node.left), self._get_depth(node.right))

    def _update_canvas_size(self):
        if not self._positions:
            self._canvas.setMinimumSize(400, 200)
            return
        max_x = max(p[0] for p in self._positions.values()) + self.NODE_RADIUS + self.PADDING
        min_x = min(p[0] for p in self._positions.values()) - self.NODE_RADIUS - self.PADDING
        max_y = max(p[1] for p in self._positions.values()) + self.NODE_RADIUS + self.PADDING
        self._canvas.setMinimumSize(int(max_x - min_x), int(max_y))

    def set_feedback(self, message: str):
        self._feedback = message
        self._feedback_label.setText(message)

    def clear_highlights(self):
        self._highlighted = set()
        self._new_node = None
        self._paint_area.update()

    def highlight_search_path(self, path_nodes):
        self._highlighted = {id(n) for n in path_nodes}
        self._paint_area.update()


class _PaintArea(QWidget):
    """Custom widget for painting the BST."""

    NODE_RADIUS = 24
    FONT_SIZE = 14
    LABEL_FONT_SIZE = 10

    def __init__(self, visualizer: BSTVisualizer):
        super().__init__()
        self._visualizer = visualizer
        self.setMinimumSize(400, 300)

        self._normal_color = QColor(ACCENT_PRIMARY)
        self._highlight_color = QColor("#2563EB")
        self._new_color = QColor("#15803D")
        self._text_color = QColor(TEXT_ON_ACCENT)
        self._edge_color = QColor(BORDER_LIGHT)
        self._bg_color = QColor(BG_SURFACE)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self._bg_color)

        positions = self._visualizer._positions
        highlighted = self._visualizer._highlighted
        new_node = self._visualizer._new_node

        if not positions:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("Segoe UI", 14))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Tree is empty")
            painter.end()
            return

        center_x = self.width() / 2
        offset_x = center_x

        for node_id, (x, y, value, node) in positions.items():
            px = x + offset_x
            py = y

            if node.left:
                left_data = positions.get(id(node.left))
                if left_data:
                    lpx = left_data[0] + offset_x
                    lpy = left_data[1]
                    painter.setPen(QPen(self._edge_color, 2))
                    painter.drawLine(QPointF(px, py + self.NODE_RADIUS),
                                     QPointF(lpx, lpy - self.NODE_RADIUS))

            if node.right:
                right_data = positions.get(id(node.right))
                if right_data:
                    rpx = right_data[0] + offset_x
                    rpy = right_data[1]
                    painter.setPen(QPen(self._edge_color, 2))
                    painter.drawLine(QPointF(px, py + self.NODE_RADIUS),
                                     QPointF(rpx, rpy - self.NODE_RADIUS))

        for node_id, (x, y, value, node) in positions.items():
            px = x + offset_x
            py = y
            is_highlighted = node_id in highlighted
            is_new = new_node is not None and value == new_node

            if is_new:
                fill_color = self._new_color
            elif is_highlighted:
                fill_color = self._highlight_color
            else:
                fill_color = self._normal_color

            painter.setPen(QPen(fill_color.darker(110), 2))
            painter.setBrush(QBrush(fill_color))
            painter.drawEllipse(QPointF(px, py), self.NODE_RADIUS, self.NODE_RADIUS)

            painter.setPen(self._text_color)
            font = QFont("Segoe UI", self.FONT_SIZE, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(QRectF(px - self.NODE_RADIUS, py - self.NODE_RADIUS,
                                   self.NODE_RADIUS * 2, self.NODE_RADIUS * 2),
                             Qt.AlignmentFlag.AlignCenter, str(value))

            if node is positions.get(list(positions.keys())[0]) and len(positions) > 0:
                label_y = py - self.NODE_RADIUS - 12
                painter.setPen(QColor("#6B7280"))
                label_font = QFont("Segoe UI", self.LABEL_FONT_SIZE)
                painter.setFont(label_font)
                painter.drawText(QRectF(px - 20, label_y, 40, 16),
                                 Qt.AlignmentFlag.AlignCenter, "ROOT")

        painter.end()
