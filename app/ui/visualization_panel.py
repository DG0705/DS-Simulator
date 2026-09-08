from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSizePolicy
)
from PyQt6.QtCore import Qt

from app.core.constants import (
    VISUALIZATION_PANEL_STYLE,
    SELECT_DATA_STRUCTURE_TEXT,
    CHOOSE_DATA_STRUCTURE_TEXT,
    VISUALIZATION_PANEL_MIN_WIDTH
)


class VisualizationPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_data_structure = None
        self._setup_ui()

    def _setup_ui(self):
        self.setMinimumWidth(VISUALIZATION_PANEL_MIN_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(VISUALIZATION_PANEL_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._title_label = QLabel(SELECT_DATA_STRUCTURE_TEXT)
        self._title_label.setObjectName("titleLabel")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title_label.setWordWrap(True)

        self._subtitle_label = QLabel(CHOOSE_DATA_STRUCTURE_TEXT)
        self._subtitle_label.setObjectName("subtitleLabel")
        self._subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subtitle_label.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(self._title_label)
        layout.addWidget(self._subtitle_label)
        layout.addStretch()

    def set_data_structure(self, name):
        self._current_data_structure = name
        self._title_label.setText(name)
        self._subtitle_label.setText(f"{name} visualization will be implemented here.")
        self._title_label.setStyleSheet("font-size: 28px; font-weight: 300; color: #333333;")
        self._subtitle_label.setStyleSheet("font-size: 16px; font-weight: 400; color: #888888;")

    def reset(self):
        self._current_data_structure = None
        self._title_label.setText(SELECT_DATA_STRUCTURE_TEXT)
        self._subtitle_label.setText(CHOOSE_DATA_STRUCTURE_TEXT)
        self._title_label.setStyleSheet("font-size: 28px; font-weight: 300; color: #333333;")
        self._subtitle_label.setStyleSheet("font-size: 16px; font-weight: 400; color: #888888;")