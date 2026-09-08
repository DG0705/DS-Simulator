from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy, QHBoxLayout
)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QFontMetrics

from app.core.constants import (
    BG_SURFACE, TEXT_PRIMARY, TEXT_ON_ACCENT, ACCENT_PRIMARY,
    ACCENT_SUCCESS_LIGHT, BORDER_LIGHT, SCROLLBAR_STYLE, TEXT_MUTED
)


class HeapVisualizer(QWidget):
    """Visualizes a Max Heap with hierarchical tree and array representation."""

    NODE_RADIUS = 24
    LEVEL_HEIGHT = 70
    MIN_SPACING = 20
    PADDING = 40

    def __init__(self, parent=None):
        super().__init__(parent)
        self._heap_data = []
        self._highlighted_indices = set()
        self._new_index = None
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
        layout.addWidget(self._scroll_area, 1)

        self._property_label = QLabel("Max Heap: Every parent is greater than or equal to its children.")
        self._property_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._property_label.setStyleSheet(
            f"font-size: 12px; color: {TEXT_MUTED}; "
            f"padding: 4px; background-color: {BG_SURFACE}; "
            f"border-top: 1px solid {BORDER_LIGHT};"
        )
        self._property_label.setFixedHeight(28)
        layout.addWidget(self._property_label)

        self._array_label = QLabel("")
        self._array_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._array_label.setWordWrap(True)
        self._array_label.setStyleSheet(
            f"font-size: 13px; color: {TEXT_PRIMARY}; "
            f"padding: 6px 12px; background-color: {BG_SURFACE}; "
            f"border-top: 1px solid {BORDER_LIGHT};"
        )
        self._array_label.setMinimumHeight(36)
        layout.addWidget(self._array_label)

        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setStyleSheet(
            f"font-size: 13px; color: {TEXT_PRIMARY}; "
            f"padding: 8px; background-color: {BG_SURFACE}; "
            f"border-top: 1px solid {BORDER_LIGHT};"
        )
        self._feedback_label.setFixedHeight(36)
        layout.addWidget(self._feedback_label)

    def set_heap(self, heap_data, highlight_indices=None, new_index=None):
        self._heap_data = list(heap_data) if heap_data else []
        self._highlighted_indices = set(highlight_indices) if highlight_indices else set()
        self._new_index = new_index

        self._paint_area.update()
        self._update_canvas_size()
        self._update_array_label()

    def _update_canvas_size(self):
        if not self._heap_data:
            self._canvas.setMinimumSize(400, 200)
            return
        depth = 0
        n = len(self._heap_data)
        while (1 << depth) - 1 < n:
            depth += 1
        width = max(1, 1 << (depth - 1)) * (self.NODE_RADIUS * 2 + self.MIN_SPACING)
        height = self.PADDING * 2 + depth * self.LEVEL_HEIGHT + self.NODE_RADIUS
        self._canvas.setMinimumSize(int(width), int(height))

    def _update_array_label(self):
        if not self._heap_data:
            self._array_label.setText("Heap Array: []")
        else:
            vals = " → ".join(str(v) for v in self._heap_data)
            self._array_label.setText(f"Heap Array: [ {vals} ]")

    def set_feedback(self, message: str):
        self._feedback = message
        self._feedback_label.setText(message)

    def clear_highlights(self):
        self._highlighted_indices = set()
        self._new_index = None
        self._paint_area.update()


class _PaintArea(QWidget):
    """Custom widget for painting the Heap tree."""

    NODE_RADIUS = 24
    FONT_SIZE = 14
    LEVEL_HEIGHT = 70
    PADDING = 40

    def __init__(self, visualizer: HeapVisualizer):
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

        heap_data = self._visualizer._heap_data
        highlighted = self._visualizer._highlighted_indices
        new_index = self._visualizer._new_index

        if not heap_data:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("Segoe UI", 14))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Heap is empty")
            painter.end()
            return

        center_x = self.width() / 2
        positions = {}
        n = len(heap_data)
        depth = 0
        while (1 << depth) - 1 < n:
            depth += 1

        for i in range(n):
            level = 0
            temp = i + 1
            while temp > 1:
                temp = (temp + 1) // 2
                level += 1

            pos_in_level = i - ((1 << level) - 1)
            nodes_in_level = min(1 << level, n - ((1 << level) - 1))
            level_width = max(1, nodes_in_level) * (self.NODE_RADIUS * 2 + 20)
            total_level_width = (1 << level) * (self.NODE_RADIUS * 2 + 20)
            start_x = center_x - total_level_width / 2 + (self.NODE_RADIUS * 2 + 20) / 2
            x = start_x + pos_in_level * (self.NODE_RADIUS * 2 + 20)
            y = self.PADDING + level * self.LEVEL_HEIGHT
            positions[i] = (x, y)

        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            px, py = positions[i]
            if left < n:
                lx, ly = positions[left]
                painter.setPen(QPen(self._edge_color, 2))
                painter.drawLine(QPointF(px, py + self.NODE_RADIUS),
                                 QPointF(lx, ly - self.NODE_RADIUS))
            if right < n:
                rx, ry = positions[right]
                painter.setPen(QPen(self._edge_color, 2))
                painter.drawLine(QPointF(px, py + self.NODE_RADIUS),
                                 QPointF(rx, ry - self.NODE_RADIUS))

        for i in range(n):
            x, y = positions[i]
            is_highlighted = i in highlighted
            is_new = new_index is not None and i == new_index

            if is_new:
                fill_color = self._new_color
            elif is_highlighted:
                fill_color = self._highlight_color
            else:
                fill_color = self._normal_color

            painter.setPen(QPen(fill_color.darker(110), 2))
            painter.setBrush(QBrush(fill_color))
            painter.drawEllipse(QPointF(x, y), self.NODE_RADIUS, self.NODE_RADIUS)

            painter.setPen(self._text_color)
            font = QFont("Segoe UI", self.FONT_SIZE, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(QRectF(x - self.NODE_RADIUS, y - self.NODE_RADIUS,
                                   self.NODE_RADIUS * 2, self.NODE_RADIUS * 2),
                             Qt.AlignmentFlag.AlignCenter, str(heap_data[i]))

        if n > 0:
            rx, ry = positions[0]
            label_y = ry - self.NODE_RADIUS - 14
            painter.setPen(QColor("#6B7280"))
            label_font = QFont("Segoe UI", 10)
            painter.setFont(label_font)
            painter.drawText(QRectF(rx - 20, label_y - 14, 40, 14),
                             Qt.AlignmentFlag.AlignCenter, "ROOT")
            painter.setPen(QPen(QColor("#6B7280"), 1, Qt.PenStyle.DashLine))
            painter.drawLine(QPointF(rx, label_y + 2), QPointF(rx, ry - self.NODE_RADIUS))

        painter.end()
