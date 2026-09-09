import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush

from app.core.constants import (
    BG_SURFACE, TEXT_PRIMARY, TEXT_ON_ACCENT, ACCENT_PRIMARY,
    ACCENT_SUCCESS_LIGHT, BORDER_LIGHT, SCROLLBAR_STYLE, TEXT_MUTED
)


class GraphVisualizer(QWidget):
    """Visualizes an undirected graph with circular layout."""

    NODE_RADIUS = 24
    PADDING = 60
    MIN_SPACING = 80

    def __init__(self, parent=None):
        super().__init__(parent)
        self._vertices = []
        self._edges = []
        self._highlighted_vertices = set()
        self._highlighted_edges = set()
        self._new_vertex = None
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

        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setStyleSheet(
            f"font-size: 13px; color: {TEXT_PRIMARY}; "
            f"padding: 8px; background-color: {BG_SURFACE}; "
            f"border-top: 1px solid {BORDER_LIGHT};"
        )
        self._feedback_label.setFixedHeight(36)
        layout.addWidget(self._feedback_label)

    def set_graph(self, vertices, edges, highlight_vertices=None,
                  highlight_edges=None, new_vertex=None):
        self._vertices = list(vertices) if vertices else []
        self._edges = list(edges) if edges else []
        self._highlighted_vertices = set(highlight_vertices) if highlight_vertices else set()
        self._highlighted_edges = set(highlight_edges) if highlight_edges else set()
        self._new_vertex = new_vertex

        self._paint_area.update()
        self._update_canvas_size()

    def _update_canvas_size(self):
        n = len(self._vertices)
        if n == 0:
            self._canvas.setMinimumSize(400, 200)
            return
        diameter = 2 * self.NODE_RADIUS + self.MIN_SPACING
        size = max(400, n * diameter + 2 * self.PADDING)
        self._canvas.setMinimumSize(int(size), int(size))

    def set_feedback(self, message: str):
        self._feedback = message
        self._feedback_label.setText(message)

    def clear_highlights(self):
        self._highlighted_vertices = set()
        self._highlighted_edges = set()
        self._new_vertex = None
        self._paint_area.update()


class _PaintArea(QWidget):
    """Custom widget for painting the Graph."""

    NODE_RADIUS = 24
    FONT_SIZE = 14

    def __init__(self, visualizer: GraphVisualizer):
        super().__init__()
        self._visualizer = visualizer
        self.setMinimumSize(400, 300)

        self._normal_color = QColor(ACCENT_PRIMARY)
        self._highlight_color = QColor("#2563EB")
        self._new_color = QColor("#15803D")
        self._edge_color = QColor(BORDER_LIGHT)
        self._edge_highlight_color = QColor("#2563EB")
        self._text_color = QColor(TEXT_ON_ACCENT)
        self._bg_color = QColor(BG_SURFACE)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self._bg_color)

        vertices = self._visualizer._vertices
        edges = self._visualizer._edges
        highlighted_v = self._visualizer._highlighted_vertices
        highlighted_e = self._visualizer._highlighted_edges
        new_vertex = self._visualizer._new_vertex

        if not vertices:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("Segoe UI", 14))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Graph is empty")
            painter.end()
            return

        positions = self._compute_positions(vertices, painter)

        for v1, v2 in edges:
            if v1 in positions and v2 in positions:
                p1 = positions[v1]
                p2 = positions[v2]
                edge_key = (min(v1, v2), max(v1, v2))
                if edge_key in highlighted_e:
                    pen = QPen(self._edge_highlight_color, 3)
                else:
                    pen = QPen(self._edge_color, 2)
                painter.setPen(pen)
                painter.drawLine(p1, p2)

        for v in vertices:
            if v in positions:
                pos = positions[v]
                is_highlighted = v in highlighted_v
                is_new = new_vertex is not None and v == new_vertex

                if is_new:
                    fill_color = self._new_color
                elif is_highlighted:
                    fill_color = self._highlight_color
                else:
                    fill_color = self._normal_color

                painter.setPen(QPen(fill_color.darker(110), 2))
                painter.setBrush(QBrush(fill_color))
                painter.drawEllipse(pos, self.NODE_RADIUS, self.NODE_RADIUS)

                painter.setPen(self._text_color)
                font = QFont("Segoe UI", self.FONT_SIZE, QFont.Weight.Bold)
                painter.setFont(font)
                painter.drawText(QRectF(pos.x() - self.NODE_RADIUS, pos.y() - self.NODE_RADIUS,
                                       self.NODE_RADIUS * 2, self.NODE_RADIUS * 2),
                                 Qt.AlignmentFlag.AlignCenter, str(v))

        painter.end()

    def _compute_positions(self, vertices, painter):
        n = len(vertices)
        positions = {}
        center_x = self.width() / 2
        center_y = self.height() / 2

        if n == 1:
            positions[vertices[0]] = QPointF(center_x, center_y)
        elif n == 2:
            spacing = 120
            positions[vertices[0]] = QPointF(center_x - spacing / 2, center_y)
            positions[vertices[1]] = QPointF(center_x + spacing / 2, center_y)
        else:
            radius = max(100, min(center_x, center_y) - self.NODE_RADIUS - 20)
            for i, v in enumerate(vertices):
                angle = 2 * math.pi * i / n - math.pi / 2
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                positions[v] = QPointF(x, y)

        return positions
