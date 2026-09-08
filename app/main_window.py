from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QGroupBox,
    QStatusBar, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt

from app.core.constants import (
    APP_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CONTROL_PANEL_STYLE,
    STATUS_BAR_STYLE,
    MAIN_WINDOW_STYLE,
    OPERATION_LABEL,
    VALUE_LABEL,
    EXECUTE_BUTTON_TEXT,
    RESET_BUTTON_TEXT,
    NO_OPERATION_SELECTED
)
from app.ui.sidebar import Sidebar
from app.ui.visualization_panel import VisualizationPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_data_structure = None
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._sidebar = Sidebar()
        self._sidebar.data_structure_selected.connect(self._on_data_structure_selected)
        main_layout.addWidget(self._sidebar)

        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        self._visualization_panel = VisualizationPanel()
        center_layout.addWidget(self._visualization_panel, 1)

        self._control_panel = self._create_control_panel()
        center_layout.addWidget(self._control_panel)

        main_layout.addWidget(center_widget, 1)

        self._status_bar = QStatusBar()
        self._status_bar.setStyleSheet(STATUS_BAR_STYLE)
        self._status_bar.showMessage(NO_OPERATION_SELECTED)
        self.setStatusBar(self._status_bar)

    def _create_control_panel(self):
        panel = QWidget()
        panel.setStyleSheet(CONTROL_PANEL_STYLE)
        panel.setFixedHeight(140)
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(panel)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(20)

        operation_group = QGroupBox(OPERATION_LABEL)
        operation_layout = QVBoxLayout(operation_group)
        operation_layout.setContentsMargins(12, 20, 12, 12)
        operation_layout.setSpacing(8)

        self._operation_combo = QComboBox()
        self._operation_combo.addItems(["Select a data structure first"])
        self._operation_combo.setEnabled(False)
        operation_layout.addWidget(self._operation_combo)

        value_group = QGroupBox(VALUE_LABEL)
        value_layout = QVBoxLayout(value_group)
        value_layout.setContentsMargins(12, 20, 12, 12)
        value_layout.setSpacing(8)

        self._value_input = QLineEdit()
        self._value_input.setPlaceholderText("Enter value")
        self._value_input.setEnabled(False)
        value_layout.addWidget(self._value_input)

        button_group = QGroupBox()
        button_group.setStyleSheet("QGroupBox { border: none; margin-top: 0; padding-top: 20px; }")
        button_layout = QVBoxLayout(button_group)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        self._execute_button = QPushButton(EXECUTE_BUTTON_TEXT)
        self._execute_button.setObjectName("executeButton")
        self._execute_button.setEnabled(False)
        self._execute_button.setMinimumWidth(120)
        self._execute_button.clicked.connect(self._on_execute)

        self._reset_button = QPushButton(RESET_BUTTON_TEXT)
        self._reset_button.setObjectName("resetButton")
        self._reset_button.setEnabled(False)
        self._reset_button.setMinimumWidth(120)
        self._reset_button.clicked.connect(self._on_reset)

        button_layout.addWidget(self._execute_button)
        button_layout.addWidget(self._reset_button)
        button_layout.addStretch()

        layout.addWidget(operation_group, 2)
        layout.addWidget(value_group, 1)
        layout.addWidget(button_group, 1)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        return panel

    def _on_data_structure_selected(self, name):
        self._current_data_structure = name
        self._visualization_panel.set_data_structure(name)
        self._status_bar.showMessage(f"Selected: {name}")

        self._operation_combo.setEnabled(True)
        self._value_input.setEnabled(True)
        self._execute_button.setEnabled(True)
        self._reset_button.setEnabled(True)

        operations = self._get_operations_for_structure(name)
        self._operation_combo.clear()
        self._operation_combo.addItems(operations)

    def _get_operations_for_structure(self, name):
        operations_map = {
            "Array": ["Insert", "Delete", "Search", "Traverse"],
            "Stack": ["Push", "Pop", "Peek", "Is Empty"],
            "Queue": ["Enqueue", "Dequeue", "Front", "Is Empty"],
            "Linked List": ["Insert at Head", "Insert at Tail", "Delete", "Search"],
            "Binary Search Tree": ["Insert", "Delete", "Search", "Inorder Traversal"],
            "Heap": ["Insert", "Extract Max/Min", "Peek", "Heapify"],
            "Graph": ["Add Vertex", "Add Edge", "BFS", "DFS"]
        }
        return operations_map.get(name, ["No operations available"])

    def _on_execute(self):
        operation = self._operation_combo.currentText()
        value = self._value_input.text()
        if self._current_data_structure:
            msg = f"Executing: {operation}"
            if value:
                msg += f" with value: {value}"
            self._status_bar.showMessage(msg)

    def _on_reset(self):
        self._visualization_panel.reset()
        self._current_data_structure = None
        self._operation_combo.clear()
        self._operation_combo.addItem("Select a data structure first")
        self._operation_combo.setEnabled(False)
        self._value_input.clear()
        self._value_input.setEnabled(False)
        self._execute_button.setEnabled(False)
        self._reset_button.setEnabled(False)
        self._status_bar.showMessage(NO_OPERATION_SELECTED)