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

DEQUEUE_ANIMATION_MS = 500


class QueueVisualizer(QWidget):
    """Widget for visualizing a queue horizontally (FRONT left, REAR right)."""

    CELL_WIDTH = 80
    CELL_HEIGHT = 60
    CELL_SPACING = 6
    MARGIN = 40
    LABEL_HEIGHT = 30
    ARROW_AREA_HEIGHT = 36

    COLORS = {
        "cell_bg": QColor(BG_TERTIARY),
        "cell_border": QColor(BORDER_MEDIUM),
        "cell_border_front": QColor(ACCENT_PRIMARY),
        "cell_bg_front": QColor(ACCENT_PRIMARY_LIGHT),
        "cell_border_rear": QColor(ACCENT_SUCCESS),
        "cell_bg_rear": QColor(ACCENT_SUCCESS_LIGHT),
        "cell_bg_new": QColor(ACCENT_WARNING_LIGHT),
        "cell_bg_deleted": QColor(ACCENT_ERROR_LIGHT),
        "value_text": QColor(TEXT_PRIMARY),
        "value_text_front": QColor(ACCENT_PRIMARY),
        "label_text": QColor(TEXT_PRIMARY),
        "arrow_text": QColor(TEXT_MUTED),
        "empty_text": QColor(TEXT_DISABLED),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._queue_data = []
        self._highlight_front = False
        self._highlight_rear = False
        self._new_rear_index = -1
        self._dequeued_index = -1
        self._dequeued_value = None
        self._operation_feedback = ""
        self._dequeue_timer = QTimer(self)
        self._dequeue_timer.setSingleShot(True)
        self._dequeue_timer.timeout.connect(self._on_dequeue_timer_done)
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

        self._canvas = _QueueCanvas(self)
        self._canvas.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self._canvas.setStyleSheet(f"background-color: {BG_SURFACE};")
        scroll_area.setWidget(self._canvas)

        layout.addWidget(scroll_area, 1)

        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setStyleSheet(f"font-size: 14px; color: {TEXT_PRIMARY}; padding: 8px;")
        self._feedback_label.setWordWrap(True)
        layout.addWidget(self._feedback_label)

    def set_queue(self, data: list, preserve_highlights: bool = False):
        """Set the queue data (expects FRONT -> REAR order from traverse)."""
        self._queue_data = data.copy() if data else []
        if not preserve_highlights:
            self._highlight_front = False
            self._highlight_rear = False
            self._new_rear_index = -1
            self._dequeued_index = -1
            self._dequeued_value = None
        self._canvas.updateGeometry()
        self._canvas.update()

    def highlight_front(self):
        """Highlight the front element."""
        self._highlight_front = True
        self._canvas.update()

    def highlight_rear(self):
        """Highlight the rear element."""
        self._highlight_rear = True
        self._canvas.update()

    def mark_new_rear(self):
        """Mark the current rear as newly enqueued."""
        if self._queue_data:
            self._new_rear_index = len(self._queue_data) - 1
        self._canvas.update()

    def mark_dequeued(self, value):
        """Mark the front as dequeued, show animation, then remove after delay."""
        self._dequeued_index = 0
        self._dequeued_value = value
        if self._queue_data:
            self._queue_data = self._queue_data[1:]
        self._canvas.updateGeometry()
        self._canvas.update()
        if self._dequeue_timer.isActive():
            self._dequeue_timer.stop()
        self._dequeue_timer.start(DEQUEUE_ANIMATION_MS)

    def _on_dequeue_timer_done(self):
        """Clear dequeue highlight after animation completes."""
        self._dequeued_index = -1
        self._dequeued_value = None
        self._canvas.update()

    def clear_highlights(self):
        """Clear all highlights."""
        if self._dequeue_timer.isActive():
            self._dequeue_timer.stop()
        self._highlight_front = False
        self._highlight_rear = False
        self._new_rear_index = -1
        self._dequeued_index = -1
        self._dequeued_value = None
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
        n = len(self._queue_data)
        width = self.MARGIN * 2 + n * (self.CELL_WIDTH + self.CELL_SPACING)
        height = self.LABEL_HEIGHT + self.ARROW_AREA_HEIGHT + self.CELL_HEIGHT + self.LABEL_HEIGHT + self.MARGIN * 2
        return QSize(max(width, 400), max(height, 200))


class _QueueCanvas(QWidget):
    """Internal canvas widget that draws the queue horizontally."""

    def __init__(self, visualizer: QueueVisualizer):
        super().__init__(visualizer)
        self._visualizer = visualizer

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self._visualizer._queue_data and self._visualizer._dequeued_value is None:
            self._draw_empty_state(painter)
            return

        if not self._visualizer._queue_data and self._visualizer._dequeued_value is not None:
            self._draw_dequeued_only(painter)
            return

        self._draw_queue(painter)

    def _draw_empty_state(self, painter: QPainter):
        rect = self.rect()
        painter.setPen(QPen(QColor(TEXT_PRIMARY)))
        font = QFont("Segoe UI", 14)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Queue is empty\n\nUse Enqueue to add elements")

    def _draw_dequeued_only(self, painter: QPainter):
        """Draw only the dequeued element (for the case where it was the last element)."""
        cell_w = self._visualizer.CELL_WIDTH
        cell_h = self._visualizer.CELL_HEIGHT
        margin = self._visualizer.MARGIN
        label_h = self._visualizer.LABEL_HEIGHT

        start_x = (self.width() - cell_w) // 2
        y = margin + label_h
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
        painter.drawText(cell_rect, Qt.AlignmentFlag.AlignCenter, str(self._visualizer._dequeued_value))

    def _draw_queue(self, painter: QPainter):
        data = self._visualizer._queue_data
        n = len(data)

        cell_w = self._visualizer.CELL_WIDTH
        cell_h = self._visualizer.CELL_HEIGHT
        spacing = self._visualizer.CELL_SPACING
        margin = self._visualizer.MARGIN
        label_h = self._visualizer.LABEL_HEIGHT
        arrow_area = self._visualizer.ARROW_AREA_HEIGHT

        total_width = n * cell_w + (n - 1) * spacing
        start_x = max(margin, (self.width() - total_width) // 2)
        cell_y = margin + label_h + arrow_area

        value_font = QFont("Segoe UI", 16, QFont.Weight.Medium)
        label_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        dir_font = QFont("Segoe UI", 9)

        front_index = 0
        rear_index = n - 1

        front_x = start_x + front_index * (cell_w + spacing) + cell_w // 2
        rear_x = start_x + rear_index * (cell_w + spacing) + cell_w // 2

        painter.setFont(label_font)

        painter.setPen(QPen(QColor(ACCENT_PRIMARY)))
        front_label_rect = QRect(front_x - 50, margin - 4, 100, label_h)
        painter.drawText(front_label_rect, Qt.AlignmentFlag.AlignCenter, "FRONT")

        painter.setPen(QPen(QColor(ACCENT_SUCCESS)))
        rear_label_rect = QRect(rear_x - 50, margin - 4, 100, label_h)
        painter.drawText(rear_label_rect, Qt.AlignmentFlag.AlignCenter, "REAR")

        arrow_y = cell_y - 4
        painter.setPen(QPen(QColor(TEXT_MUTED), 2))
        painter.drawLine(margin, arrow_y, start_x + total_width + margin, arrow_y)

        deq_x = start_x - 2
        painter.drawLine(deq_x, arrow_y - 6, deq_x, arrow_y + 6)
        painter.drawLine(deq_x, arrow_y - 6, deq_x + 8, arrow_y - 6)
        painter.drawLine(deq_x, arrow_y + 6, deq_x + 8, arrow_y + 6)

        enq_x = start_x + total_width + 2
        painter.drawLine(enq_x, arrow_y - 6, enq_x, arrow_y + 6)
        painter.drawLine(enq_x, arrow_y - 6, enq_x - 8, arrow_y - 6)
        painter.drawLine(enq_x, arrow_y + 6, enq_x - 8, arrow_y + 6)

        painter.setFont(dir_font)
        painter.setPen(QPen(QColor(TEXT_MUTED)))

        deq_text_rect = QRect(deq_x - 50, arrow_y + 8, 70, 18)
        painter.drawText(deq_text_rect, Qt.AlignmentFlag.AlignCenter, "DEQUEUE")

        enq_text_rect = QRect(enq_x - 20, arrow_y + 8, 70, 18)
        painter.drawText(enq_text_rect, Qt.AlignmentFlag.AlignCenter, "ENQUEUE")

        for i, value in enumerate(data):
            x = start_x + i * (cell_w + spacing)
            y = cell_y

            cell_rect = QRect(x, y, cell_w, cell_h)

            is_front = (i == front_index)
            is_rear = (i == rear_index)
            is_highlighted_front = is_front and self._visualizer._highlight_front
            is_highlighted_rear = is_rear and self._visualizer._highlight_rear
            is_new = (i == self._visualizer._new_rear_index)

            if is_highlighted_front:
                bg_color = self._visualizer.COLORS["cell_bg_front"]
                border_color = self._visualizer.COLORS["cell_border_front"]
                text_color = self._visualizer.COLORS["value_text_front"]
            elif is_highlighted_rear:
                bg_color = self._visualizer.COLORS["cell_bg_rear"]
                border_color = self._visualizer.COLORS["cell_border_rear"]
                text_color = self._visualizer.COLORS["value_text"]
            elif is_new:
                bg_color = self._visualizer.COLORS["cell_bg_new"]
                border_color = self._visualizer.COLORS["cell_border"]
                text_color = self._visualizer.COLORS["value_text"]
            else:
                bg_color = self._visualizer.COLORS["cell_bg"]
                border_color = self._visualizer.COLORS["cell_border"]
                text_color = self._visualizer.COLORS["value_text"]

            painter.setBrush(QBrush(bg_color))
            thick = 2 if (is_highlighted_front or is_highlighted_rear or is_new) else 1
            painter.setPen(QPen(border_color, thick))
            painter.drawRoundedRect(cell_rect, 6, 6)

            painter.setFont(value_font)
            painter.setPen(QPen(text_color))
            painter.drawText(cell_rect, Qt.AlignmentFlag.AlignCenter, str(value))

        bottom_y = cell_y + cell_h + 8
        painter.setFont(label_font)

        painter.setPen(QPen(QColor(ACCENT_PRIMARY)))
        fl = QRect(start_x + front_index * (cell_w + spacing) - 10, bottom_y, cell_w + 20, 20)
        painter.drawText(fl, Qt.AlignmentFlag.AlignCenter, "FRONT")

        painter.setPen(QPen(QColor(ACCENT_SUCCESS)))
        rl = QRect(start_x + rear_index * (cell_w + spacing) - 10, bottom_y, cell_w + 20, 20)
        painter.drawText(rl, Qt.AlignmentFlag.AlignCenter, "REAR")

    def sizeHint(self):
        return self._visualizer.sizeHint()
