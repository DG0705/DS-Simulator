from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QGroupBox,
    QStatusBar, QSizePolicy, QSpacerItem, QMessageBox
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
from data_structures.array import Array, ArrayError, ArrayIndexError, ArrayValueError, ArrayEmptyError
from visualization.array_visualizer import ArrayVisualizer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_data_structure = None
        self._array = None
        self._array_visualizer = None
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
        self._operation_combo.currentTextChanged.connect(self._on_operation_changed)
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

        if name == "Array":
            self._setup_array()
        else:
            self._visualization_panel.set_data_structure(name)
            self._status_bar.showMessage(f"Selected: {name}")
            self._enable_controls()
            operations = self._get_operations_for_structure(name)
            self._operation_combo.clear()
            self._operation_combo.addItems(operations)

    def _setup_array(self):
        self._array = Array()
        self._create_array_visualizer()
        self._status_bar.showMessage("Selected: Array")
        self._enable_controls()

        operations = [
            "Append",
            "Insert",
            "Delete",
            "Search",
            "Update",
            "Get",
            "Traverse",
            "Clear"
        ]
        self._operation_combo.clear()
        self._operation_combo.addItems(operations)
        self._on_operation_changed(operations[0])

    def _create_array_visualizer(self):
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                center_layout.removeWidget(self._visualization_panel)
                self._visualization_panel.hide()

        self._array_visualizer = ArrayVisualizer()
        self._array_visualizer.set_array(self._array.traverse())

        if center_widget and center_layout:
            center_layout.insertWidget(0, self._array_visualizer, 1)

    def _enable_controls(self):
        self._operation_combo.setEnabled(True)
        self._value_input.setEnabled(True)
        self._execute_button.setEnabled(True)
        self._reset_button.setEnabled(True)

    def _on_operation_changed(self, operation: str):
        placeholders = {
            "Append": "Enter value (e.g., 50)",
            "Insert": "Enter index,value (e.g., 2,50)",
            "Delete": "Enter index (e.g., 2)",
            "Search": "Enter value to search (e.g., 50)",
            "Update": "Enter index,value (e.g., 2,50)",
            "Get": "Enter index (e.g., 2)",
            "Traverse": "No input required",
            "Clear": "No input required",
        }
        placeholder = placeholders.get(operation, "Enter value")
        self._value_input.setPlaceholderText(placeholder)

        if operation in ["Traverse", "Clear"]:
            self._value_input.setEnabled(False)
        else:
            self._value_input.setEnabled(True)

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
        if not self._current_data_structure:
            return

        operation = self._operation_combo.currentText()
        value_text = self._value_input.text().strip()

        if self._current_data_structure == "Array":
            self._execute_array_operation(operation, value_text)
        else:
            msg = f"Executing: {operation}"
            if value_text:
                msg += f" with value: {value_text}"
            self._status_bar.showMessage(msg)

    def _execute_array_operation(self, operation: str, value_text: str):
        try:
            if operation == "Append":
                self._execute_append(value_text)
            elif operation == "Insert":
                self._execute_insert(value_text)
            elif operation == "Delete":
                self._execute_delete(value_text)
            elif operation == "Search":
                self._execute_search(value_text)
            elif operation == "Update":
                self._execute_update(value_text)
            elif operation == "Get":
                self._execute_get(value_text)
            elif operation == "Traverse":
                self._execute_traverse()
            elif operation == "Clear":
                self._execute_clear()
        except ArrayError as e:
            self._show_error(str(e))
            self._status_bar.showMessage(f"Error: {e}")

    def _parse_index_value(self, text: str) -> tuple:
        parts = [p.strip() for p in text.split(",")]
        if len(parts) != 2:
            raise ArrayValueError("Invalid format. Use: index,value (e.g., 2,50)")
        try:
            index = int(parts[0])
            value = int(parts[1])
        except ValueError:
            raise ArrayValueError("Index and value must be integers")
        return index, value

    def _parse_index(self, text: str) -> int:
        try:
            return int(text.strip())
        except ValueError:
            raise ArrayValueError("Index must be an integer")

    def _parse_value(self, text: str) -> int:
        try:
            return int(text.strip())
        except ValueError:
            raise ArrayValueError("Value must be an integer")

    def _execute_append(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Value required for Append")
        value = self._parse_value(value_text)
        self._array.append(value)
        self._array_visualizer.set_array(self._array.traverse())
        self._array_visualizer.mark_new(self._array.size() - 1)
        self._array_visualizer.set_feedback(f"Appended {value} to the array.")
        self._update_status("Append", "O(1) amortized", "O(1) auxiliary")

    def _execute_insert(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index and value required for Insert (format: index,value)")
        index, value = self._parse_index_value(value_text)
        self._array.insert(index, value)
        self._array_visualizer.set_array(self._array.traverse())
        self._array_visualizer.mark_new(index)
        self._array_visualizer.set_feedback(f"Inserted {value} at index {index}.")
        self._update_status("Insert", "O(n)", "O(1) auxiliary")

    def _execute_delete(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index required for Delete")
        index = self._parse_index(value_text)
        deleted_value = self._array.delete(index)
        self._array_visualizer.set_array(self._array.traverse())
        self._array_visualizer.mark_deleted(index, deleted_value)
        self._array_visualizer.set_feedback(f"Deleted element {deleted_value} from index {index}.")
        self._update_status("Delete", "O(n)", "O(1) auxiliary")

    def _execute_search(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Value required for Search")
        value = self._parse_value(value_text)
        index = self._array.search(value)
        self._array_visualizer.highlight_index(index)
        self._array_visualizer.set_feedback(f"Value {value} found at index {index}.")
        self._update_status("Search", "O(n)", "O(1) auxiliary")

    def _execute_update(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index and value required for Update (format: index,value)")
        index, value = self._parse_index_value(value_text)
        old_value = self._array.update(index, value)
        self._array_visualizer.set_array(self._array.traverse())
        self._array_visualizer.select_index(index)
        self._array_visualizer.set_feedback(f"Updated index {index} from {old_value} to {value}.")
        self._update_status("Update", "O(1)", "O(1)")

    def _execute_get(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index required for Get")
        index = self._parse_index(value_text)
        value = self._array.get(index)
        self._array_visualizer.highlight_index(index)
        self._array_visualizer.set_feedback(f"arr[{index}] = {value}.")
        self._update_status("Get", "O(1)", "O(1)")

    def _execute_traverse(self):
        elements = self._array.traverse()
        if not elements:
            self._array_visualizer.set_feedback("Array is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in elements)
            self._array_visualizer.set_feedback(f"Traversal: {traversal_str}")
        self._update_status("Traverse", "O(n)", "O(1) auxiliary")

    def _execute_clear(self):
        self._array.clear()
        self._array_visualizer.set_array([])
        self._array_visualizer.clear_highlights()
        self._array_visualizer.set_feedback("Array cleared.")
        self._update_status("Clear", "O(n)", "O(1) auxiliary")

    def _update_status(self, operation: str, time_complexity: str, space_complexity: str):
        self._status_bar.showMessage(
            f"Operation: {operation} | Time: {time_complexity} | Space: {space_complexity}"
        )

    def _show_error(self, message: str):
        QMessageBox.warning(self, "Error", message)

    def _on_reset(self):
        if self._array_visualizer:
            center_widget = self._visualization_panel.parent()
            if center_widget:
                center_layout = center_widget.layout()
                if center_layout:
                    center_layout.removeWidget(self._array_visualizer)
                    self._array_visualizer.deleteLater()
                    self._array_visualizer = None

        self._visualization_panel.show()
        if center_widget and center_layout:
            center_layout.insertWidget(0, self._visualization_panel, 1)

        self._array = None
        self._current_data_structure = None
        self._visualization_panel.reset()
        self._operation_combo.clear()
        self._operation_combo.addItem("Select a data structure first")
        self._operation_combo.setEnabled(False)
        self._value_input.clear()
        self._value_input.setEnabled(False)
        self._execute_button.setEnabled(False)
        self._reset_button.setEnabled(False)
        self._status_bar.showMessage(NO_OPERATION_SELECTED)