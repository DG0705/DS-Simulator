from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal

from app.core.constants import (
    DATA_STRUCTURES,
    SORTING_ALGORITHMS,
    PLACEHOLDER_BUTTON_STYLE,
    SIDEBAR_STYLE,
    DATA_STRUCTURES_SECTION_TITLE,
    SIDEBAR_WIDTH,
    ENABLED_BUTTON_STYLE,
    SCROLLBAR_STYLE
)


class Sidebar(QWidget):
    data_structure_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_button = None
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedWidth(SIDEBAR_WIDTH)
        self.setStyleSheet(SIDEBAR_STYLE)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(SCROLLBAR_STYLE)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 16, 0, 16)
        scroll_layout.setSpacing(12)

        section_label = QLabel(DATA_STRUCTURES_SECTION_TITLE)
        section_label.setObjectName("sectionTitle")
        section_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        scroll_layout.addWidget(section_label)

        self._buttons = {}
        enabled_structures = {"Array", "Stack", "Queue", "Linked List", "Binary Search Tree", "AVL Tree", "Heap", "Graph"}
        for ds_name in DATA_STRUCTURES:
            if ds_name in enabled_structures:
                button = self._create_enabled_button(ds_name)
            else:
                button = self._create_placeholder_button(ds_name)
            self._buttons[ds_name] = button
            scroll_layout.addWidget(button)

        self._sorting_toggle = QPushButton("Sorting  ▸")
        self._sorting_toggle.setCheckable(True)
        self._sorting_toggle.setStyleSheet(ENABLED_BUTTON_STYLE)
        self._sorting_toggle.clicked.connect(self._toggle_sorting)
        scroll_layout.addWidget(self._sorting_toggle)

        self._sorting_menu = QWidget()
        sorting_layout = QVBoxLayout(self._sorting_menu)
        sorting_layout.setContentsMargins(16, 0, 0, 0)
        sorting_layout.setSpacing(8)
        for name in SORTING_ALGORITHMS:
            button = self._create_enabled_button(name)
            self._buttons[name] = button
            sorting_layout.addWidget(button)
        self._sorting_menu.hide()
        scroll_layout.addWidget(self._sorting_menu)

        scroll_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def _create_placeholder_button(self, name):
        button = QPushButton(f"{name}  (Coming Soon)")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(PLACEHOLDER_BUTTON_STYLE)
        button.setEnabled(False)
        button.setToolTip(f"{name} visualization - not yet implemented")
        button.clicked.connect(lambda checked, n=name: self._on_button_clicked(n))
        return button

    def _create_enabled_button(self, name):
        button = QPushButton(name)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(ENABLED_BUTTON_STYLE)
        button.setEnabled(True)
        button.setCheckable(True)
        button.setToolTip(f"{name} visualization")
        button.clicked.connect(lambda checked, n=name: self._on_button_clicked(n))
        return button

    def _on_button_clicked(self, name):
        if self._selected_button:
            if self._selected_button.text().endswith("(Coming Soon)"):
                self._selected_button.setStyleSheet(PLACEHOLDER_BUTTON_STYLE)
            else:
                self._selected_button.setStyleSheet(ENABLED_BUTTON_STYLE)
                self._selected_button.setChecked(False)
        self._selected_button = self._buttons[name]
        if not self._selected_button.text().endswith("(Coming Soon)"):
            self._selected_button.setChecked(True)
        self.data_structure_selected.emit(name)

    def _toggle_sorting(self, checked):
        self._sorting_menu.setVisible(checked)
        self._sorting_toggle.setText("Sorting  ▾" if checked else "Sorting  ▸")
