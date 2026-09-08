from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QRect, QTimer
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
    ACCENT_ERROR,
    ACCENT_ERROR_LIGHT,
    ACCENT_WARNING_LIGHT,
    SCROLLBAR_BG,
    SCROLLBAR_HANDLE,
    SCROLLBAR_HANDLE_HOVER,
)

POP_ANIMATION_MS = 500


class StackVisualizer(QWidget):
    """Widget for visualizing a stack vertically (TOP at top)."""

    CELL_WIDTH = 180
    CELL_HEIGHT = 50
    CELL_SPACING = 6
    MARGIN = 30
    TOP_LABEL_HEIGHT = 30

    COLORS = {
        "cell_bg": QColor(BG_TERTIARY),
        "cell_border": QColor(BORDER_MEDIUM),
        "cell_border_highlight": QColor(ACCENT_PRIMARY),
        "cell_border_selected": QColor(ACCENT_SUCCESS),
        "cell_bg_highlight": QColor(ACCENT_PRIMARY_LIGHT),
        "cell_bg_selected": QColor(ACCENT_SUCCESS_LIGHT),
        "cell_bg_new": QColor(ACCENT_WARNING_LIGHT),
        "cell_bg_deleted": QColor(ACCENT_ERROR_LIGHT),
        "value_text": QColor(TEXT_PRIMARY),
        "value_text_highlight": QColor(ACCENT_PRIMARY),
        "index_text": QColor(TEXT_MUTED),
        "empty_text": QColor(TEXT_DISABLED),
        "top_text": QColor(ACCENT_PRIMARY),
        "bottom_text": QColor(TEXT_MUTED),
        "cell_bg_peek": QColor(ACCENT_PRIMARY_LIGHT),
        "cell_border_peek": QColor(ACCENT_PRIMARY),
        "value_text_peek": QColor(ACCENT_PRIMARY),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stack_data = []
        self._highlight_top = False
        self._new_index = -1
        self._popped_index = -1
        self._popped_value = None
        self._operation_feedback = ""
        self._pop_timer = QTimer(self)
        self._pop_timer.setSingleShot(True)
        self._pop_timer.timeout.connect(self._on_pop_timer_done)
        self._setup_ui()

    def _setup_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {SCROLLBAR_BG};
                width: 8px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {SCROLLBAR_HANDLE};
                border-radius: 4px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {SCROLLBAR_HANDLE_HOVER};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
        """)

        self._canvas = _StackCanvas(self)
        self._canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._canvas.setStyleSheet(f"background-color: {BG_SURFACE};")
        scroll_area.setWidget(self._canvas)

        layout.addWidget(scroll_area, 1)

        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setStyleSheet(f"font-size: 14px; color: {TEXT_PRIMARY}; padding: 8px;")
        self._feedback_label.setWordWrap(True)
        layout.addWidget(self._feedback_label)

    def set_stack(self, data: list, preserve_highlights: bool = False):
        """Set the stack data (expects TOP -> BOTTOM order from traverse)."""
        self._stack_data = data.copy() if data else []
        if not preserve_highlights:
            self._highlight_top = False
            self._new_index = -1
            self._popped_index = -1
            self._popped_value = None
        self._canvas.updateGeometry()
        self._canvas.update()

    def highlight_top(self):
        """Highlight the top element (for peek)."""
        self._highlight_top = True
        self._canvas.update()

    def mark_new_top(self):
        """Mark the current top as newly pushed."""
        self._new_index = 0
        self._canvas.update()

    def mark_popped(self, value):
        """Mark the top as popped, show animation, then remove after delay."""
        self._popped_index = 0
        self._popped_value = value
        self._stack_data = [v for v in self._stack_data if v is not self._popped_value]
        if not self._stack_data:
            self._stack_data = []
        self._canvas.updateGeometry()
        self._canvas.update()
        if self._pop_timer.isActive():
            self._pop_timer.stop()
        self._pop_timer.start(POP_ANIMATION_MS)

    def _on_pop_timer_done(self):
        """Clear pop highlight after animation completes."""
        self._popped_index = -1
        self._popped_value = None
        self._canvas.update()

    def clear_highlights(self):
        """Clear all highlights."""
        if self._pop_timer.isActive():
            self._pop_timer.stop()
        self._highlight_top = False
        self._new_index = -1
        self._popped_index = -1
        self._popped_value = None
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
        n = len(self._stack_data)
        height = self.TOP_LABEL_HEIGHT + n * (self.CELL_HEIGHT + self.CELL_SPACING) + self.MARGIN * 2 + 40
        width = self.CELL_WIDTH + self.MARGIN * 2
        return QSize(width, max(height, 200))


class _StackCanvas(QWidget):
    """Internal canvas widget that draws the stack vertically."""

    def __init__(self, visualizer: StackVisualizer):
        super().__init__(visualizer)
        self._visualizer = visualizer

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self._visualizer._stack_data and self._visualizer._popped_value is None:
            self._draw_empty_state(painter)
            return

        if not self._visualizer._stack_data and self._visualizer._popped_value is not None:
            self._draw_popped_only(painter)
            return

        self._draw_stack(painter)

    def _draw_empty_state(self, painter: QPainter):
        rect = self.rect()
        painter.setPen(QPen(QColor(TEXT_PRIMARY)))
        font = QFont("Segoe UI", 14)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Stack is empty\n\nUse Push to add elements")

    def _draw_popped_only(self, painter: QPainter):
        """Draw only the popped element (for the case where it was the last element)."""
        cell_w = self._visualizer.CELL_WIDTH
        cell_h = self._visualizer.CELL_HEIGHT
        margin = self._visualizer.MARGIN
        top_label_h = self._visualizer.TOP_LABEL_HEIGHT

        start_x = (self.width() - cell_w) // 2
        y = margin + top_label_h
        cell_rect = QRect(start_x, y, cell_w, cell_h)

        bg_color = self._visualizer.COLORS["cell_bg_deleted"]
        border_color = self._visualizer.COLORS["cell_border"]
        text_color = self._visualizer.COLORS["value_text"]

        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(border_color, 2))
        painter.drawRoundedRect(cell_rect, 6, 6)

        value_font = QFont("Segoe UI", 16, QFont.Weight.Medium)
        painter.setFont(value_font)
        painter.setPen(QPen(text_color))
        painter.drawText(cell_rect, Qt.AlignmentFlag.AlignCenter, str(self._visualizer._popped_value))

        top_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        top_label_y = y - top_label_h
        painter.setFont(top_font)
        painter.setPen(QPen(QColor(TEXT_MUTED)))
        top_rect = QRect(start_x - 40, top_label_y, cell_w + 80, top_label_h)
        painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, "TOP")

    def _draw_stack(self, painter: QPainter):
        data = self._visualizer._stack_data
        n = len(data)

        cell_w = self._visualizer.CELL_WIDTH
        cell_h = self._visualizer.CELL_HEIGHT
        spacing = self._visualizer.CELL_SPACING
        margin = self._visualizer.MARGIN
        top_label_h = self._visualizer.TOP_LABEL_HEIGHT

        total_height = n * cell_h + (n - 1) * spacing
        start_x = (self.width() - cell_w) // 2
        start_y = margin + top_label_h

        value_font = QFont("Segoe UI", 16, QFont.Weight.Medium)
        label_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        top_font = QFont("Segoe UI", 12, QFont.Weight.Bold)

        bottom_y = start_y + total_height + 8
        painter.setFont(label_font)
        painter.setPen(QPen(QColor(TEXT_PRIMARY)))
        bottom_rect = QRect(start_x - 40, bottom_y, cell_w + 80, 20)
        painter.drawText(bottom_rect, Qt.AlignmentFlag.AlignCenter, "BOTTOM")

        painter.setPen(QPen(QColor(BORDER_MEDIUM), 1))
        line_y = start_y + total_height + 4
        painter.drawLine(start_x, line_y, start_x + cell_w, line_y)

        for i, value in enumerate(data):
            x = start_x
            y = start_y + i * (cell_h + spacing)

            cell_rect = QRect(x, y, cell_w, cell_h)

            is_top = (i == 0)
            is_highlighted = is_top and self._visualizer._highlight_top
            is_new = (i == self._visualizer._new_index)

            if is_highlighted:
                bg_color = self._visualizer.COLORS["cell_bg_peek"]
                border_color = self._visualizer.COLORS["cell_border_peek"]
                text_color = self._visualizer.COLORS["value_text_peek"]
            elif is_new:
                bg_color = self._visualizer.COLORS["cell_bg_new"]
                border_color = self._visualizer.COLORS["cell_border"]
                text_color = self._visualizer.COLORS["value_text"]
            else:
                bg_color = self._visualizer.COLORS["cell_bg"]
                border_color = self._visualizer.COLORS["cell_border"]
                text_color = self._visualizer.COLORS["value_text"]

            painter.setBrush(QBrush(bg_color))
            thick = 2 if (is_highlighted or is_new) else 1
            painter.setPen(QPen(border_color, thick))
            painter.drawRoundedRect(cell_rect, 6, 6)

            painter.setFont(value_font)
            painter.setPen(QPen(text_color))
            painter.drawText(cell_rect, Qt.AlignmentFlag.AlignCenter, str(value))

            if is_top:
                top_label_y = y - top_label_h
                painter.setFont(top_font)
                painter.setPen(QPen(QColor(ACCENT_PRIMARY)))
                top_rect = QRect(start_x - 40, top_label_y, cell_w + 80, top_label_h)
                painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, "TOP")

                arrow_x = self.width() // 2
                arrow_y_start = top_label_y + top_label_h - 4
                arrow_y_end = y - 2
                painter.setPen(QPen(QColor(ACCENT_PRIMARY), 2))
                painter.drawLine(arrow_x, arrow_y_start, arrow_x, arrow_y_end)
                painter.drawLine(arrow_x, arrow_y_end, arrow_x - 5, arrow_y_end - 8)
                painter.drawLine(arrow_x, arrow_y_end, arrow_x + 5, arrow_y_end - 8)

    def sizeHint(self):
        return self._visualizer.sizeHint()
