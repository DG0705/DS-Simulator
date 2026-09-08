from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush

from app.core.constants import (
    BG_SURFACE,
    BG_TERTIARY,
    TEXT_PRIMARY,
    TEXT_MUTED,
    TEXT_DISABLED,
    BORDER_MEDIUM,
    ACCENT_PRIMARY,
    ACCENT_PRIMARY_LIGHT,
    ACCENT_SUCCESS,
    ACCENT_SUCCESS_LIGHT,
    ACCENT_ERROR_LIGHT,
    ACCENT_WARNING_LIGHT,
    SCROLLBAR_BG,
    SCROLLBAR_HANDLE,
    SCROLLBAR_HANDLE_HOVER,
)


class LinkedListVisualizer(QWidget):
    """Widget for visualizing a singly linked list horizontally."""

    NODE_WIDTH = 100
    NODE_HEIGHT = 50
    ARROW_LENGTH = 40
    MARGIN = 50
    LABEL_HEIGHT = 28

    COLORS = {
        "node_bg": QColor(BG_TERTIARY),
        "node_border": QColor(BORDER_MEDIUM),
        "node_data_bg": QColor(BG_TERTIARY),
        "node_next_bg": QColor("#D6E0EA"),
        "node_border_highlight": QColor(ACCENT_PRIMARY),
        "node_bg_highlight": QColor(ACCENT_PRIMARY_LIGHT),
        "node_border_new": QColor(ACCENT_SUCCESS),
        "node_bg_new": QColor(ACCENT_SUCCESS_LIGHT),
        "node_bg_deleted": QColor(ACCENT_ERROR_LIGHT),
        "node_bg_search": QColor(ACCENT_PRIMARY_LIGHT),
        "value_text": QColor(TEXT_PRIMARY),
        "value_text_highlight": QColor(ACCENT_PRIMARY),
        "label_text": QColor(TEXT_PRIMARY),
        "arrow_color": QColor(BORDER_MEDIUM),
        "arrow_highlight": QColor(ACCENT_PRIMARY),
        "null_text": QColor(TEXT_MUTED),
        "head_text": QColor(ACCENT_PRIMARY),
        "tail_text": QColor(ACCENT_SUCCESS),
        "empty_text": QColor(TEXT_DISABLED),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._list_data = []
        self._highlight_index = -1
        self._new_index = -1
        self._deleted_index = -1
        self._deleted_value = None
        self._operation_feedback = ""
        self._setup_ui()

    def _setup_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:horizontal {{
                background-color: {SCROLLBAR_BG};
                height: 8px;
                border: none;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-width: 30px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {SCROLLBAR_HANDLE_HOVER};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0;
            }}
        """)

        self._canvas = _LinkedListCanvas(self)
        self._canvas.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._canvas.setStyleSheet(f"background-color: {BG_SURFACE};")
        scroll_area.setWidget(self._canvas)

        layout.addWidget(scroll_area, 1)

        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setStyleSheet(f"font-size: 14px; color: {TEXT_PRIMARY}; padding: 8px;")
        self._feedback_label.setWordWrap(True)
        layout.addWidget(self._feedback_label)

    def set_list(self, data: list, preserve_highlights: bool = False):
        """Set the linked list data (HEAD -> TAIL order)."""
        self._list_data = data.copy() if data else []
        if not preserve_highlights:
            self._highlight_index = -1
            self._new_index = -1
            self._deleted_index = -1
            self._deleted_value = None
        self._canvas.updateGeometry()
        self._canvas.update()

    def highlight_index(self, index: int):
        """Highlight a specific node."""
        self._highlight_index = index
        self._canvas.update()

    def mark_new(self, index: int):
        """Mark a node as newly inserted."""
        self._new_index = index
        self._canvas.update()

    def mark_deleted(self, index: int, value):
        """Mark a node as deleted."""
        self._deleted_index = index
        self._deleted_value = value
        self._canvas.update()

    def clear_highlights(self):
        """Clear all highlights."""
        self._highlight_index = -1
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
        n = len(self._list_data)
        node_total = self.NODE_WIDTH + self.ARROW_LENGTH
        width = self.MARGIN * 2 + n * node_total + 80
        height = self.LABEL_HEIGHT * 2 + self.NODE_HEIGHT + self.LABEL_HEIGHT + self.MARGIN * 2
        return QSize(max(width, 400), max(height, 200))


class _LinkedListCanvas(QWidget):
    """Internal canvas widget that draws the linked list horizontally."""

    def __init__(self, visualizer: LinkedListVisualizer):
        super().__init__(visualizer)
        self._visualizer = visualizer

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self._visualizer._list_data and self._visualizer._deleted_value is None:
            self._draw_empty_state(painter)
            return

        if not self._visualizer._list_data and self._visualizer._deleted_value is not None:
            self._draw_deleted_only(painter)
            return

        self._draw_list(painter)

    def _draw_empty_state(self, painter: QPainter):
        rect = self.rect()
        painter.setPen(QPen(QColor(TEXT_PRIMARY)))
        font = QFont("Segoe UI", 12)
        painter.setFont(font)

        head_font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        painter.setFont(head_font)
        painter.setPen(QPen(QColor(ACCENT_PRIMARY)))
        center_x = self.width() // 2
        painter.drawText(center_x - 30, 40, "HEAD")
        painter.drawText(center_x + 10, 40, "↓")

        painter.setPen(QPen(QColor(TEXT_PRIMARY)))
        font = QFont("Segoe UI", 14)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "NULL")

    def _draw_deleted_only(self, painter: QPainter):
        """Draw only the deleted element."""
        node_w = self._visualizer.NODE_WIDTH
        node_h = self._visualizer.NODE_HEIGHT
        center_x = self.width() // 2
        y = 60
        x = center_x - node_w // 2

        self._draw_node(painter, x, y, self._visualizer._deleted_value, is_deleted=True)

    def _draw_list(self, painter: QPainter):
        data = self._visualizer._list_data
        n = len(data)

        node_w = self._visualizer.NODE_WIDTH
        node_h = self._visualizer.NODE_HEIGHT
        arrow_len = self._visualizer.ARROW_LENGTH
        margin = self._visualizer.MARGIN
        label_h = self._visualizer.LABEL_HEIGHT

        total_width = n * node_w + (n - 1) * arrow_len
        start_x = max(margin, (self.width() - total_width) // 2)
        cell_y = margin + label_h + label_h

        head_font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        null_font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        label_font = QFont("Segoe UI", 9)

        head_x = start_x + node_w // 2
        painter.setFont(head_font)
        painter.setPen(QPen(QColor(ACCENT_PRIMARY)))
        painter.drawText(head_x - 20, margin + label_h - 4, "HEAD")
        painter.setPen(QPen(QColor(ACCENT_PRIMARY), 2))
        painter.drawLine(head_x, margin + label_h, head_x, cell_y - 2)
        painter.drawLine(head_x, cell_y - 2, head_x - 4, cell_y - 8)
        painter.drawLine(head_x, cell_y - 2, head_x + 4, cell_y - 8)

        for i, value in enumerate(data):
            x = start_x + i * (node_w + arrow_len)
            y = cell_y

            is_highlighted = (i == self._visualizer._highlight_index)
            is_new = (i == self._visualizer._new_index)
            is_last = (i == n - 1)

            self._draw_node(painter, x, y, value,
                            is_highlighted=is_highlighted,
                            is_new=is_new)

            if is_last:
                arrow_end_x = x + node_w + arrow_len
                arrow_mid_y = y + node_h // 2
                painter.setPen(QPen(QColor(TEXT_MUTED), 2))
                painter.drawLine(x + node_w + 4, arrow_mid_y, arrow_end_x - 4, arrow_mid_y)
                painter.drawLine(arrow_end_x - 4, arrow_mid_y, arrow_end_x - 10, arrow_mid_y - 4)
                painter.drawLine(arrow_end_x - 4, arrow_mid_y, arrow_end_x - 10, arrow_mid_y + 4)

                null_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
                painter.setFont(null_font)
                painter.setPen(QPen(QColor(TEXT_MUTED)))
                painter.drawText(arrow_end_x - 2, arrow_mid_y - 12, "NULL")
            else:
                arrow_start_x = x + node_w
                arrow_end_x = x + node_w + arrow_len
                arrow_mid_y = y + node_h // 2

                painter.setPen(QPen(QColor(ACCENT_PRIMARY), 2))
                painter.drawLine(arrow_start_x + 2, arrow_mid_y, arrow_end_x - 8, arrow_mid_y)
                painter.drawLine(arrow_end_x - 8, arrow_mid_y, arrow_end_x - 14, arrow_mid_y - 5)
                painter.drawLine(arrow_end_x - 8, arrow_mid_y, arrow_end_x - 14, arrow_mid_y + 5)

        if n > 0:
            last_x = start_x + (n - 1) * (node_w + arrow_len) + node_w // 2
            tail_y = cell_y + node_h + label_h + 4
            painter.setFont(head_font)
            painter.setPen(QPen(QColor(ACCENT_SUCCESS)))
            painter.drawText(last_x - 18, tail_y, "TAIL")
            painter.setPen(QPen(QColor(ACCENT_SUCCESS), 2))
            painter.drawLine(last_x, cell_y + node_h + 2, last_x, tail_y - 2)
            painter.drawLine(last_x, tail_y - 2, last_x - 4, tail_y - 8)
            painter.drawLine(last_x, tail_y - 2, last_x + 4, tail_y - 8)

    def _draw_node(self, painter: QPainter, x: int, y: int, value,
                   is_highlighted=False, is_new=False, is_deleted=False):
        node_w = self._visualizer.NODE_WIDTH
        node_h = self._visualizer.NODE_HEIGHT
        data_w = int(node_w * 0.65)
        next_w = node_w - data_w

        if is_deleted:
            bg = self._visualizer.COLORS["node_bg_deleted"]
            border = self._visualizer.COLORS["node_border"]
            text_color = self._visualizer.COLORS["value_text"]
        elif is_highlighted:
            bg = self._visualizer.COLORS["node_bg_highlight"]
            border = self._visualizer.COLORS["node_border_highlight"]
            text_color = self._visualizer.COLORS["value_text_highlight"]
        elif is_new:
            bg = self._visualizer.COLORS["node_bg_new"]
            border = self._visualizer.COLORS["node_border_new"]
            text_color = self._visualizer.COLORS["value_text"]
        else:
            bg = self._visualizer.COLORS["node_data_bg"]
            border = self._visualizer.COLORS["node_border"]
            text_color = self._visualizer.COLORS["value_text"]

        data_rect = QRect(x, y, data_w, node_h)
        painter.setBrush(QBrush(bg))
        thick = 2 if (is_highlighted or is_new or is_deleted) else 1
        painter.setPen(QPen(border, thick))
        painter.drawRoundedRect(data_rect, 6, 0)

        next_bg = self._visualizer.COLORS["node_next_bg"]
        next_rect = QRect(x + data_w, y, next_w, node_h)
        painter.setBrush(QBrush(next_bg))
        painter.setPen(QPen(border, thick))
        painter.drawRoundedRect(next_rect, 0, 6)

        painter.setPen(QPen(border, 1))
        painter.drawLine(x + data_w, y, x + data_w, y + node_h)

        value_font = QFont("Segoe UI", 14, QFont.Weight.Medium)
        painter.setFont(value_font)
        painter.setPen(QPen(text_color))
        painter.drawText(data_rect, Qt.AlignmentFlag.AlignCenter, str(value))

        ptr_font = QFont("Segoe UI", 10)
        painter.setFont(ptr_font)
        painter.setPen(QPen(QColor(TEXT_MUTED)))
        painter.drawText(next_rect, Qt.AlignmentFlag.AlignCenter, "→")

    def sizeHint(self):
        return self._visualizer.sizeHint()
