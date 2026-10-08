from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QRect, QEasingCurve, QVariantAnimation
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

QUEUE_ANIMATION_MS = 800


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
        self._animation_kind = None
        self._animation_value = None
        self._animation_progress = 1.0
        self._pending_animations = []
        self._operation_feedback = ""
        self._animation = QVariantAnimation(self)
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.setDuration(QUEUE_ANIMATION_MS)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._animation.valueChanged.connect(self._on_animation_frame)
        self._animation.finished.connect(self._on_animation_finished)
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
            self._animation.stop()
            self._pending_animations.clear()
            self._highlight_front = False
            self._highlight_rear = False
            self._new_rear_index = -1
            self._animation_kind = None
            self._animation_value = None
            self._animation_progress = 1.0
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

    def animate_enqueue(self, value, final_data):
        """Animate a value from outside the queue into the rear."""
        self._queue_animation("enqueue", value, final_data)

    def animate_dequeue(self, value, remaining):
        """Animate the former front out of the queue."""
        self._queue_animation("dequeue", value, remaining)

    def _queue_animation(self, kind, value, data):
        request = (kind, value, list(data))
        if self._animation_kind is not None:
            self._pending_animations.append(request)
            return
        self._start_animation(*request)

    def _start_animation(self, kind, value, data):
        self._animation.stop()
        self._queue_data = list(data)
        self._highlight_front = False
        self._highlight_rear = False
        self._new_rear_index = -1
        self._animation_kind = kind
        self._animation_value = value
        self._animation_progress = 0.0
        self._canvas.updateGeometry()
        self._canvas.update()
        self._animation.start()

    def _on_animation_frame(self, value):
        self._animation_progress = float(value)
        self._canvas.update()

    def _on_animation_finished(self):
        completed_kind = self._animation_kind
        self._animation_progress = 1.0
        self._new_rear_index = len(self._queue_data) - 1 if completed_kind == "enqueue" else -1
        self._animation_kind = None
        self._animation_value = None
        self._canvas.updateGeometry()
        self._canvas.update()
        if self._pending_animations:
            self._start_animation(*self._pending_animations.pop(0))

    def clear_highlights(self):
        """Clear all highlights."""
        self._animation.stop()
        self._pending_animations.clear()
        self._highlight_front = False
        self._highlight_rear = False
        self._new_rear_index = -1
        self._animation_kind = None
        self._animation_value = None
        self._animation_progress = 1.0
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
        n = len(self._queue_data) + (1 if self._animation_kind == "dequeue" else 0)
        # Leave room beside the cells for the enqueue/dequeue direction labels.
        width = n * self.CELL_WIDTH + max(0, n - 1) * self.CELL_SPACING + 240
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

        if not self._visualizer._queue_data and self._visualizer._animation_kind is None:
            self._draw_empty_state(painter)
            return

        self._draw_queue(painter)

    def _draw_empty_state(self, painter: QPainter):
        rect = self.rect()
        painter.setPen(QPen(QColor(TEXT_PRIMARY)))
        font = QFont("Segoe UI", 14)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Queue is empty\n\nUse Enqueue to add elements")

    def _draw_queue(self, painter: QPainter):
        data = self._visualizer._queue_data
        n = len(data)
        kind = self._visualizer._animation_kind
        progress = self._visualizer._animation_progress

        cell_w = self._visualizer.CELL_WIDTH
        cell_h = self._visualizer.CELL_HEIGHT
        spacing = self._visualizer.CELL_SPACING
        margin = self._visualizer.MARGIN
        label_h = self._visualizer.LABEL_HEIGHT
        arrow_area = self._visualizer.ARROW_AREA_HEIGHT

        total_width = n * cell_w + max(0, n - 1) * spacing
        start_x = max(margin, (self.width() - total_width) // 2)
        old_n = n - 1 if kind == "enqueue" else n + 1 if kind == "dequeue" else n
        old_total_width = old_n * cell_w + max(0, old_n - 1) * spacing
        old_start_x = max(margin, (self.width() - old_total_width) // 2)
        cell_y = margin + label_h + arrow_area

        value_font = QFont("Segoe UI", 16, QFont.Weight.Medium)
        label_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        dir_font = QFont("Segoe UI", 9)

        front_index = 0
        rear_index = n - 1

        front_x = start_x + cell_w // 2
        rear_x = start_x + max(0, rear_index) * (cell_w + spacing) + cell_w // 2

        painter.setFont(label_font)

        if n == 1:
            painter.setPen(QPen(QColor(TEXT_PRIMARY)))
            painter.drawText(QRect(front_x - 80, margin - 4, 160, label_h),
                             Qt.AlignmentFlag.AlignCenter, "FRONT / REAR")
        elif n > 1:
            painter.setPen(QPen(QColor(ACCENT_PRIMARY)))
            painter.drawText(QRect(front_x - 50, margin - 4, 100, label_h),
                             Qt.AlignmentFlag.AlignCenter, "FRONT")
            painter.setPen(QPen(QColor(ACCENT_SUCCESS)))
            painter.drawText(QRect(rear_x - 50, margin - 4, 100, label_h),
                             Qt.AlignmentFlag.AlignCenter, "REAR")

        painter.setFont(dir_font)
        painter.setPen(QPen(QColor(TEXT_MUTED)))

        direction_y = cell_y + (cell_h - 24) // 2
        painter.drawText(QRect(start_x - 120, direction_y, 110, 24),
                         Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                         "DEQUEUE ←")
        painter.drawText(QRect(start_x + total_width + 10, direction_y, 110, 24),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         "→ ENQUEUE")

        for i, value in enumerate(data):
            if kind == "enqueue" and i == n - 1:
                continue
            x = start_x + i * (cell_w + spacing)
            if kind == "enqueue":
                old_x = old_start_x + i * (cell_w + spacing)
                x = round(old_x + (x - old_x) * progress)
            elif kind == "dequeue":
                old_x = old_start_x + (i + 1) * (cell_w + spacing)
                x = round(old_x + (x - old_x) * progress)
            y = cell_y

            cell_rect = QRect(x, y, cell_w, cell_h)

            is_front = (i == front_index and kind is None)
            is_rear = (i == rear_index and kind is None)
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

        if kind is not None:
            if kind == "enqueue":
                target_x = start_x + (n - 1) * (cell_w + spacing)
                outside_x = target_x + cell_w + 70
                x = round(outside_x + (target_x - outside_x) * progress)
                color = self._visualizer.COLORS["cell_bg_new"]
            else:
                source_x = old_start_x
                outside_x = source_x - cell_w - 70
                x = round(source_x + (outside_x - source_x) * progress)
                color = self._visualizer.COLORS["cell_bg_deleted"]
            moving_rect = QRect(x, cell_y, cell_w, cell_h)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(self._visualizer.COLORS["cell_border"], 2))
            painter.drawRoundedRect(moving_rect, 6, 6)
            painter.setFont(value_font)
            painter.setPen(QPen(self._visualizer.COLORS["value_text"]))
            painter.drawText(
                moving_rect, Qt.AlignmentFlag.AlignCenter,
                str(self._visualizer._animation_value),
            )

    def sizeHint(self):
        return self._visualizer.sizeHint()
