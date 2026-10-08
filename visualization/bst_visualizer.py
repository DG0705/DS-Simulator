from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy
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
        self._root = None
        self._positions = {}
        self._highlighted = set()
        self._new_node = None
        self._show_balance = False
        self._focus_values = set()
        self._rotation_values = set()
        self._animation_origin = {}
        self._animation_progress = 1.0
        self._traversal_visited = set()
        self._traversal_current = None
        self._feedback = ""
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet(f"background-color: {BG_SURFACE};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setStyleSheet(SCROLLBAR_STYLE)

        self._canvas = QWidget()
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

        controls = QHBoxLayout()
        controls.setContentsMargins(12, 6, 12, 8)
        self.progress_label = QLabel("")
        controls.addWidget(self.progress_label, 1)
        self.step_button = QPushButton("Step")
        self.step_button.setEnabled(False)
        controls.addWidget(self.step_button)
        layout.addLayout(controls)

    def set_traversal_state(self, visited=(), current=None):
        self._traversal_visited = set(visited)
        self._traversal_current = current
        self._paint_area.update()

    def set_tree(self, bst_root, highlight_path=None, new_value=None):
        self._nodes = []
        self._root = bst_root
        self._highlighted = set()
        self._new_node = new_value
        self._focus_values = set()
        self._rotation_values = set()
        self._traversal_visited = set()
        self._traversal_current = None

        if highlight_path:
            self._highlighted = {id(n) for n in highlight_path}

        if bst_root:
            self._compute_positions(bst_root)
        else:
            self._positions = {}

        self._paint_area.update()

    def _compute_positions(self, root):
        if root is None:
            self._positions = {}
            return

        # Inorder ranks keep the layout proportional to the number of nodes,
        # including trees that grow in a single direction.
        positions = {}
        stack = []
        node = root
        depth = 0
        rank = 0
        spacing = self.NODE_RADIUS * 2 + self.MIN_SPACING
        while stack or node:
            while node:
                stack.append((node, depth))
                node = node.left
                depth += 1
            node, depth = stack.pop()
            positions[id(node)] = (rank * spacing, depth * self.LEVEL_HEIGHT, node.value, node)
            rank += 1
            node = node.right
            depth += 1
        self._positions = positions

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
        focus_values = self._visualizer._focus_values
        rotation_values = self._visualizer._rotation_values
        height_cache = {}

        if not positions:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("Segoe UI", 14))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Tree is empty")
            painter.end()
            return

        scale, offset_x, offset_y = self._fit_transform()
        painter.translate(offset_x, offset_y)
        painter.scale(scale, scale)
        display_positions = self._display_positions(scale, offset_x, offset_y)

        if self._visualizer._animation_origin and self._visualizer._animation_progress < 1.0:
            painter.save()
            painter.setOpacity(0.45 * (1.0 - self._visualizer._animation_progress))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor("#D97706"), 2, Qt.PenStyle.DashLine))
            for node_id, (_, _, value, _) in positions.items():
                if value not in rotation_values or value not in self._visualizer._animation_origin:
                    continue
                screen_x, screen_y = self._visualizer._animation_origin[value]
                old_x = (screen_x - offset_x) / scale
                old_y = (screen_y - offset_y) / scale
                current_x, current_y = display_positions[node_id]
                painter.drawEllipse(QPointF(old_x, old_y), self.NODE_RADIUS, self.NODE_RADIUS)
                painter.drawLine(QPointF(old_x, old_y), QPointF(current_x, current_y))
            painter.restore()

        for node_id, (x, y, value, node) in positions.items():
            px, py = display_positions[node_id]

            if node.left:
                left_data = positions.get(id(node.left))
                if left_data:
                    lpx, lpy = display_positions[id(node.left)]
                    painter.setPen(QPen(self._edge_color, 2))
                    painter.drawLine(QPointF(px, py + self.NODE_RADIUS),
                                     QPointF(lpx, lpy - self.NODE_RADIUS))

            if node.right:
                right_data = positions.get(id(node.right))
                if right_data:
                    rpx, rpy = display_positions[id(node.right)]
                    painter.setPen(QPen(self._edge_color, 2))
                    painter.drawLine(QPointF(px, py + self.NODE_RADIUS),
                                     QPointF(rpx, rpy - self.NODE_RADIUS))

        for node_id, (x, y, value, node) in positions.items():
            px, py = display_positions[node_id]
            is_highlighted = node_id in highlighted
            is_new = new_node is not None and value == new_node

            if value == self._visualizer._traversal_current:
                fill_color = QColor("#D97706")
            elif value in self._visualizer._traversal_visited:
                fill_color = QColor("#15803D")
            elif value in rotation_values:
                fill_color = QColor("#D97706")
            elif is_new:
                fill_color = self._new_color
            elif is_highlighted or value in focus_values:
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

            if self._visualizer._show_balance:
                left_height = self._actual_height(node.left, height_cache)
                right_height = self._actual_height(node.right, height_cache)
                balance = left_height - right_height
                painter.setPen(QColor("#92400E") if value in rotation_values else QColor("#4B5563"))
                painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                painter.drawText(
                    QRectF(px - 55, py - self.NODE_RADIUS - 28, 110, 20),
                    Qt.AlignmentFlag.AlignCenter,
                    f"BF: {left_height} - {right_height} = {balance:+d}",
                )
            elif node is self._visualizer._root:
                label_y = py - self.NODE_RADIUS - 12
                painter.setPen(QColor("#6B7280"))
                label_font = QFont("Segoe UI", self.LABEL_FONT_SIZE)
                painter.setFont(label_font)
                painter.drawText(QRectF(px - 20, label_y, 40, 16),
                                 Qt.AlignmentFlag.AlignCenter, "ROOT")

        painter.end()

    def _display_positions(self, scale=None, offset_x=None, offset_y=None):
        if scale is None:
            scale, offset_x, offset_y = self._fit_transform()
        origin = self._visualizer._animation_origin
        progress = self._visualizer._animation_progress
        result = {}
        for node_id, (x, y, value, _) in self._visualizer._positions.items():
            if value in origin and progress < 1.0:
                old_screen_x, old_screen_y = origin[value]
                old_x = (old_screen_x - offset_x) / scale
                old_y = (old_screen_y - offset_y) / scale
                x = old_x + (x - old_x) * progress
                y = old_y + (y - old_y) * progress
            result[node_id] = (x, y)
        return result

    def _actual_height(self, node, cache):
        if node is None:
            return 0
        node_id = id(node)
        if node_id not in cache:
            cache[node_id] = 1 + max(
                self._actual_height(node.left, cache),
                self._actual_height(node.right, cache),
            )
        return cache[node_id]

    def _fit_transform(self):
        positions = self._visualizer._positions
        radius = self.NODE_RADIUS
        scene_width = max(p[0] for p in positions.values()) + 2 * radius
        scene_height = max(p[1] for p in positions.values()) + 2 * radius
        padding = self._visualizer.PADDING
        scale = min(
            1.0,
            max(1, self.width() - 2 * padding) / scene_width,
            max(1, self.height() - 2 * padding) / scene_height,
        )
        offset_x = (self.width() - scene_width * scale) / 2 + radius * scale
        offset_y = padding + radius * scale
        return scale, offset_x, offset_y
