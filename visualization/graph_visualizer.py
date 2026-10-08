import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy
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

    def __init__(self, parent=None):
        super().__init__(parent)
        self._vertices = []
        self._edges = []
        self._highlighted_vertices = set()
        self._highlighted_edges = set()
        self._new_vertex = None
        self._feedback = ""
        self._traversal_visited = set()
        self._traversal_current = None
        self._traversal_queued = set()
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

        controls = QHBoxLayout()
        controls.setContentsMargins(12, 6, 12, 8)
        self.progress_label = QLabel("")
        controls.addWidget(self.progress_label, 1)
        self.step_button = QPushButton("Step")
        self.step_button.setEnabled(False)
        controls.addWidget(self.step_button)
        layout.addLayout(controls)

    def set_graph(self, vertices, edges, highlight_vertices=None,
                  highlight_edges=None, new_vertex=None):
        self._vertices = list(vertices) if vertices else []
        self._edges = list(edges) if edges else []
        self._highlighted_vertices = set(highlight_vertices) if highlight_vertices else set()
        self._highlighted_edges = set(highlight_edges) if highlight_edges else set()
        self._new_vertex = new_vertex
        self._traversal_visited = set()
        self._traversal_current = None
        self._traversal_queued = set()

        self._paint_area.update()

    def set_feedback(self, message: str):
        self._feedback = message
        self._feedback_label.setText(message)

    def clear_highlights(self):
        self._highlighted_vertices = set()
        self._highlighted_edges = set()
        self._new_vertex = None
        self._traversal_visited = set()
        self._traversal_current = None
        self._traversal_queued = set()
        self._paint_area.update()

    def set_traversal_state(self, visited=None, current=None, queued=None):
        self._traversal_visited = set(visited) if visited else set()
        self._traversal_current = current
        self._traversal_queued = set(queued) if queued else set()
        self._paint_area.update()


class _PaintArea(QWidget):
    """Custom widget for painting the Graph."""

    NODE_RADIUS = 24
    FONT_SIZE = 14

    def __init__(self, visualizer: GraphVisualizer):
        super().__init__()
        self._visualizer = visualizer

        self._normal_color = QColor(ACCENT_PRIMARY)
        self._highlight_color = QColor("#2563EB")
        self._new_color = QColor("#15803D")
        self._visited_color = QColor("#7C3AED")
        self._current_color = QColor("#DC2626")
        self._queued_color = QColor("#F59E0B")
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
        visited = self._visualizer._traversal_visited
        current = self._visualizer._traversal_current
        queued = self._visualizer._traversal_queued

        if not vertices:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("Segoe UI", 14))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Graph is empty")
            painter.end()
            return

        positions, node_radius = self._compute_positions(vertices)

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
                is_visited = v in visited
                is_current = v == current
                is_queued = v in queued

                if is_current:
                    fill_color = self._current_color
                elif is_visited:
                    fill_color = self._visited_color
                elif is_queued:
                    fill_color = self._queued_color
                elif is_new:
                    fill_color = self._new_color
                elif is_highlighted:
                    fill_color = self._highlight_color
                else:
                    fill_color = self._normal_color

                painter.setPen(QPen(fill_color.darker(110), 2))
                painter.setBrush(QBrush(fill_color))
                painter.drawEllipse(pos, node_radius, node_radius)

                painter.setPen(self._text_color)
                font_size = max(6, round(self.FONT_SIZE * node_radius / self.NODE_RADIUS))
                font = QFont("Segoe UI", font_size, QFont.Weight.Bold)
                painter.setFont(font)
                painter.drawText(QRectF(pos.x() - node_radius, pos.y() - node_radius,
                                       node_radius * 2, node_radius * 2),
                                 Qt.AlignmentFlag.AlignCenter, str(v))

        painter.end()

    def _compute_positions(self, vertices):
        n = len(vertices)
        positions = {}
        center_x = self.width() / 2
        center_y = self.height() / 2
        margin = 12
        node_radius = min(self.NODE_RADIUS, max(2, min(center_x, center_y) - margin))

        if n == 1:
            positions[vertices[0]] = QPointF(center_x, center_y)
        elif n == 2:
            spacing = min(120, max(0, self.width() - 2 * (node_radius + margin)))
            positions[vertices[0]] = QPointF(center_x - spacing / 2, center_y)
            positions[vertices[1]] = QPointF(center_x + spacing / 2, center_y)
        elif n > 2:
            available_radius = max(0, min(center_x, center_y) - node_radius - margin)
            node_radius = min(node_radius, max(2, available_radius * math.sin(math.pi / n) - 3))
            radius = max(0, min(center_x, center_y) - node_radius - margin)
            for i, v in enumerate(vertices):
                angle = 2 * math.pi * i / n - math.pi / 2
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                positions[v] = QPointF(x, y)

        return positions, node_radius
