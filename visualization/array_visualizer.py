from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QFontMetrics


class ArrayVisualizer(QWidget):
    """Widget for visualizing an array as indexed cells."""

    CELL_WIDTH = 70
    CELL_HEIGHT = 70
    INDEX_HEIGHT = 25
    HORIZONTAL_SPACING = 4
    VERTICAL_MARGIN = 20

    COLORS = {
        "background": QColor("#ffffff"),
        "cell_bg": QColor("#f0f0f0"),
        "cell_border": QColor("#b0b0b0"),
        "cell_border_highlight": QColor("#0078d4"),
        "cell_border_selected": QColor("#107c10"),
        "cell_bg_highlight": QColor("#d6eaff"),
        "cell_bg_selected": QColor("#d6f5d6"),
        "cell_bg_new": QColor("#fff8e1"),
        "cell_bg_deleted": QColor("#ffeaea"),
        "index_text": QColor("#666666"),
        "value_text": QColor("#1a1a1a"),
        "value_text_highlight": QColor("#005a9e"),
        "empty_text": QColor("#999999"),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._array_data = []
        self._highlighted_index = -1
        self._selected_index = -1
        self._new_index = -1
        self._deleted_index = -1
        self._deleted_value = None
        self._operation_feedback = ""
        self._setup_ui()

    def _setup_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                background-color: #f0f0f0;
                height: 8px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #cccccc;
                border-radius: 4px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #bbbbbb;
            }
        """)

        self._canvas = _ArrayCanvas(self)
        self._canvas.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._canvas.setStyleSheet("background-color: #ffffff;")
        scroll_area.setWidget(self._canvas)

        layout.addWidget(scroll_area, 1)

        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setStyleSheet("font-size: 14px; color: #666666; padding: 8px;")
        self._feedback_label.setWordWrap(True)
        layout.addWidget(self._feedback_label)

    def set_array(self, data: list):
        """Set the array data to visualize."""
        self._array_data = data.copy() if data else []
        self._highlighted_index = -1
        self._selected_index = -1
        self._new_index = -1
        self._deleted_index = -1
        self._deleted_value = None
        self._canvas.updateGeometry()
        self._canvas.update()

    def highlight_index(self, index: int):
        """Highlight a specific index (for search, get operations)."""
        self._highlighted_index = index
        self._canvas.update()

    def select_index(self, index: int):
        """Select a specific index (for update, insert operations)."""
        self._selected_index = index
        self._canvas.update()

    def mark_new(self, index: int):
        """Mark an index as newly inserted."""
        self._new_index = index
        self._canvas.update()

    def mark_deleted(self, index: int, value: any):
        """Mark an index as deleted (shows deleted value before removal)."""
        self._deleted_index = index
        self._deleted_value = value
        self._canvas.update()

    def clear_highlights(self):
        """Clear all highlights."""
        self._highlighted_index = -1
        self._selected_index = -1
        self._new_index = -1
        self._deleted_index = -1
        self._deleted_value = None
        self._canvas.update()

    def set_feedback(self, message: str):
        """Set the operation feedback message."""
        self._operation_feedback = message
        self._feedback_label.setText(message)

    def clear_feedback(self):
        """Clear the feedback message."""
        self._operation_feedback = ""
        self._feedback_label.setText("")

    def sizeHint(self):
        from PyQt6.QtCore import QSize
        width = max(400, len(self._array_data) * (self.CELL_WIDTH + self.HORIZONTAL_SPACING) + 40)
        return QSize(width, self.CELL_HEIGHT + self.INDEX_HEIGHT + self.VERTICAL_MARGIN * 2 + 60)


class _ArrayCanvas(QWidget):
    """Internal canvas widget that draws the array."""

    def __init__(self, visualizer: ArrayVisualizer):
        super().__init__(visualizer)
        self._visualizer = visualizer

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self._visualizer._array_data:
            self._draw_empty_state(painter)
            return

        self._draw_array(painter)

    def _draw_empty_state(self, painter: QPainter):
        rect = self.rect()
        painter.setPen(QPen(self._visualizer.COLORS["empty_text"]))
        font = QFont("Segoe UI", 14)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Array is empty\n\nUse Append or Insert to add elements")

    def _draw_array(self, painter: QPainter):
        data = self._visualizer._array_data
        n = len(data)

        cell_w = self._visualizer.CELL_WIDTH
        cell_h = self._visualizer.CELL_HEIGHT
        index_h = self._visualizer.INDEX_HEIGHT
        spacing = self._visualizer.HORIZONTAL_SPACING
        v_margin = self._visualizer.VERTICAL_MARGIN

        total_width = n * cell_w + (n - 1) * spacing
        start_x = (self.width() - total_width) // 2
        start_y = v_margin

        index_font = QFont("Segoe UI", 10)
        value_font = QFont("Segoe UI", 16, QFont.Weight.Medium)

        for i, value in enumerate(data):
            x = start_x + i * (cell_w + spacing)
            y = start_y

            index_rect = QRect(x, y, cell_w, index_h)
            cell_rect = QRect(x, y + index_h, cell_w, cell_h)

            is_highlighted = (i == self._visualizer._highlighted_index)
            is_selected = (i == self._visualizer._selected_index)
            is_new = (i == self._visualizer._new_index)
            is_deleted = (i == self._visualizer._deleted_index)

            # Draw index label
            painter.setFont(index_font)
            painter.setPen(QPen(self._visualizer.COLORS["index_text"]))
            painter.drawText(index_rect, Qt.AlignmentFlag.AlignCenter, str(i))

            # Determine cell colors
            if is_deleted:
                bg_color = self._visualizer.COLORS["cell_bg_deleted"]
                border_color = self._visualizer.COLORS["cell_border"]
                text_color = self._visualizer.COLORS["value_text"]
            elif is_new:
                bg_color = self._visualizer.COLORS["cell_bg_new"]
                border_color = self._visualizer.COLORS["cell_border"]
                text_color = self._visualizer.COLORS["value_text"]
            elif is_highlighted:
                bg_color = self._visualizer.COLORS["cell_bg_highlight"]
                border_color = self._visualizer.COLORS["cell_border_highlight"]
                text_color = self._visualizer.COLORS["value_text_highlight"]
            elif is_selected:
                bg_color = self._visualizer.COLORS["cell_bg_selected"]
                border_color = self._visualizer.COLORS["cell_border_selected"]
                text_color = self._visualizer.COLORS["value_text"]
            else:
                bg_color = self._visualizer.COLORS["cell_bg"]
                border_color = self._visualizer.COLORS["cell_border"]
                text_color = self._visualizer.COLORS["value_text"]

            # Draw cell background
            painter.setBrush(QBrush(bg_color))
            painter.setPen(QPen(border_color, 2 if (is_highlighted or is_selected or is_new or is_deleted) else 1))
            painter.drawRoundedRect(cell_rect, 6, 6)

            # Draw value
            painter.setFont(value_font)
            painter.setPen(QPen(text_color))
            value_text = str(self._visualizer._deleted_value) if is_deleted else str(value)
            painter.drawText(cell_rect, Qt.AlignmentFlag.AlignCenter, value_text)

    def sizeHint(self):
        return self._visualizer.sizeHint()