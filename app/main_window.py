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
    NO_OPERATION_SELECTED,
    ARRAY_OPERATIONS,
    ARRAY_OPERATION_NAMES,
    STACK_OPERATIONS,
    STACK_OPERATION_NAMES,
    QUEUE_OPERATIONS,
    QUEUE_OPERATION_NAMES,
    LINKED_LIST_OPERATIONS,
    LINKED_LIST_OPERATION_NAMES,
    BST_OPERATIONS,
    BST_OPERATION_NAMES,
    HEAP_OPERATIONS,
    HEAP_OPERATION_NAMES,
    DATA_STRUCTURE_OPERATIONS,
)
from app.ui.sidebar import Sidebar
from app.ui.visualization_panel import VisualizationPanel
from data_structures.array import Array, ArrayError, ArrayIndexError, ArrayValueError, ArrayEmptyError
from data_structures.stack import Stack, StackError, StackEmptyError, StackValueError
from data_structures.queue import Queue, QueueError, QueueEmptyError, QueueValueError
from data_structures.linked_list import (
    SinglyLinkedList, LinkedListError, LinkedListEmptyError,
    LinkedListIndexError, LinkedListValueError,
)
from data_structures.bst import BinarySearchTree, BSTError, BSTEmptyError, BSTValueError
from data_structures.heap import MaxHeap, HeapError, HeapEmptyError, HeapValueError
from visualization.array_visualizer import ArrayVisualizer
from visualization.stack_visualizer import StackVisualizer
from visualization.queue_visualizer import QueueVisualizer
from visualization.linked_list_visualizer import LinkedListVisualizer
from visualization.bst_visualizer import BSTVisualizer
from visualization.heap_visualizer import HeapVisualizer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_data_structure = None
        self._array = None
        self._array_visualizer = None
        self._stack = None
        self._stack_visualizer = None
        self._queue = None
        self._queue_visualizer = None
        self._linked_list = None
        self._linked_list_visualizer = None
        self._bst = None
        self._bst_visualizer = None
        self._heap = None
        self._heap_visualizer = None
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
        panel.setFixedHeight(160)
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

        self._operation_description = QLabel("")
        self._operation_description.setStyleSheet("font-size: 11px; color: #6B7280; padding: 2px 4px;")
        self._operation_description.setWordWrap(True)
        self._operation_description.setMinimumHeight(24)
        operation_layout.addWidget(self._operation_description)

        self._value_group = QGroupBox(VALUE_LABEL)
        self._value_group.setMinimumWidth(180)
        value_layout = QVBoxLayout(self._value_group)
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
        layout.addWidget(self._value_group, 1)
        layout.addWidget(button_group, 1)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        return panel

    def _on_data_structure_selected(self, name):
        self._current_data_structure = name

        if name == "Array":
            self._setup_array()
        elif name == "Stack":
            self._setup_stack()
        elif name == "Queue":
            self._setup_queue()
        elif name == "Linked List":
            self._setup_linked_list()
        elif name == "Binary Search Tree":
            self._setup_bst()
        elif name == "Heap":
            self._setup_heap()
        else:
            self._visualization_panel.set_data_structure(name)
            self._status_bar.showMessage(f"Selected: {name}")
            self._enable_controls()
            operations = self._get_operations_for_structure(name)
            self._operation_combo.clear()
            self._operation_combo.addItems(operations)
            self._value_group.setTitle(VALUE_LABEL)
            self._value_input.setPlaceholderText("Enter value")
            self._operation_description.setText("")

    def _setup_array(self):
        self._array = Array()
        self._create_array_visualizer()
        self._status_bar.showMessage("Selected: Array")
        self._enable_controls()

        self._operation_combo.clear()
        self._operation_combo.addItems(ARRAY_OPERATION_NAMES)
        self._on_operation_changed(ARRAY_OPERATION_NAMES[0])

    def _setup_stack(self):
        self._stack = Stack()
        self._create_stack_visualizer()
        self._status_bar.showMessage("Selected: Stack")
        self._enable_controls()

        self._operation_combo.clear()
        self._operation_combo.addItems(STACK_OPERATION_NAMES)
        self._on_operation_changed(STACK_OPERATION_NAMES[0])

    def _setup_queue(self):
        self._queue = Queue()
        self._create_queue_visualizer()
        self._status_bar.showMessage("Selected: Queue")
        self._enable_controls()

        self._operation_combo.clear()
        self._operation_combo.addItems(QUEUE_OPERATION_NAMES)
        self._on_operation_changed(QUEUE_OPERATION_NAMES[0])

    def _setup_linked_list(self):
        self._linked_list = SinglyLinkedList()
        self._create_linked_list_visualizer()
        self._status_bar.showMessage("Selected: Linked List")
        self._enable_controls()

        self._operation_combo.clear()
        self._operation_combo.addItems(LINKED_LIST_OPERATION_NAMES)
        self._on_operation_changed(LINKED_LIST_OPERATION_NAMES[0])

    def _setup_bst(self):
        self._bst = BinarySearchTree()
        self._create_bst_visualizer()
        self._status_bar.showMessage("Selected: Binary Search Tree")
        self._enable_controls()

        self._operation_combo.clear()
        self._operation_combo.addItems(BST_OPERATION_NAMES)
        self._on_operation_changed(BST_OPERATION_NAMES[0])

    def _setup_heap(self):
        self._heap = MaxHeap()
        self._create_heap_visualizer()
        self._status_bar.showMessage("Selected: Heap")
        self._enable_controls()

        self._operation_combo.clear()
        self._operation_combo.addItems(HEAP_OPERATION_NAMES)
        self._on_operation_changed(HEAP_OPERATION_NAMES[0])

    def _create_array_visualizer(self):
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                self._remove_current_visualizer(center_layout)
                center_layout.removeWidget(self._visualization_panel)
                self._visualization_panel.hide()

        self._array_visualizer = ArrayVisualizer()
        self._array_visualizer.set_array(self._array.traverse())

        if center_widget and center_layout:
            center_layout.insertWidget(0, self._array_visualizer, 1)

    def _create_stack_visualizer(self):
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                self._remove_current_visualizer(center_layout)
                center_layout.removeWidget(self._visualization_panel)
                self._visualization_panel.hide()

        self._stack_visualizer = StackVisualizer()
        self._stack_visualizer.set_stack(self._stack.traverse())

        if center_widget and center_layout:
            center_layout.insertWidget(0, self._stack_visualizer, 1)

    def _create_queue_visualizer(self):
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                self._remove_current_visualizer(center_layout)
                center_layout.removeWidget(self._visualization_panel)
                self._visualization_panel.hide()

        self._queue_visualizer = QueueVisualizer()
        self._queue_visualizer.set_queue(self._queue.traverse())

        if center_widget and center_layout:
            center_layout.insertWidget(0, self._queue_visualizer, 1)

    def _create_linked_list_visualizer(self):
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                self._remove_current_visualizer(center_layout)
                center_layout.removeWidget(self._visualization_panel)
                self._visualization_panel.hide()

        self._linked_list_visualizer = LinkedListVisualizer()
        self._linked_list_visualizer.set_list(self._linked_list.traverse())

        if center_widget and center_layout:
            center_layout.insertWidget(0, self._linked_list_visualizer, 1)

    def _create_bst_visualizer(self):
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                self._remove_current_visualizer(center_layout)
                center_layout.removeWidget(self._visualization_panel)
                self._visualization_panel.hide()

        self._bst_visualizer = BSTVisualizer()
        self._bst_visualizer.set_tree(self._bst.root)

        if center_widget and center_layout:
            center_layout.insertWidget(0, self._bst_visualizer, 1)

    def _create_heap_visualizer(self):
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                self._remove_current_visualizer(center_layout)
                center_layout.removeWidget(self._visualization_panel)
                self._visualization_panel.hide()

        self._heap_visualizer = HeapVisualizer()
        self._heap_visualizer.set_heap(self._heap.traverse())

        if center_widget and center_layout:
            center_layout.insertWidget(0, self._heap_visualizer, 1)

    def _remove_current_visualizer(self, center_layout):
        """Remove any currently displayed visualizer from the layout."""
        if self._array_visualizer:
            center_layout.removeWidget(self._array_visualizer)
            self._array_visualizer.deleteLater()
            self._array_visualizer = None
        if self._stack_visualizer:
            center_layout.removeWidget(self._stack_visualizer)
            self._stack_visualizer.deleteLater()
            self._stack_visualizer = None
        if self._queue_visualizer:
            center_layout.removeWidget(self._queue_visualizer)
            self._queue_visualizer.deleteLater()
            self._queue_visualizer = None
        if self._linked_list_visualizer:
            center_layout.removeWidget(self._linked_list_visualizer)
            self._linked_list_visualizer.deleteLater()
            self._linked_list_visualizer = None
        if self._bst_visualizer:
            center_layout.removeWidget(self._bst_visualizer)
            self._bst_visualizer.deleteLater()
            self._bst_visualizer = None
        if self._heap_visualizer:
            center_layout.removeWidget(self._heap_visualizer)
            self._heap_visualizer.deleteLater()
            self._heap_visualizer = None

    def _enable_controls(self):
        self._operation_combo.setEnabled(True)
        self._value_input.setEnabled(True)
        self._execute_button.setEnabled(True)
        self._reset_button.setEnabled(True)

    def _on_operation_changed(self, operation: str):
        if not self._current_data_structure:
            return

        if self._current_data_structure == "Array":
            op_info = ARRAY_OPERATIONS.get(operation)
        elif self._current_data_structure == "Stack":
            op_info = STACK_OPERATIONS.get(operation)
        elif self._current_data_structure == "Queue":
            op_info = QUEUE_OPERATIONS.get(operation)
        elif self._current_data_structure == "Linked List":
            op_info = LINKED_LIST_OPERATIONS.get(operation)
        elif self._current_data_structure == "Binary Search Tree":
            op_info = BST_OPERATIONS.get(operation)
        elif self._current_data_structure == "Heap":
            op_info = HEAP_OPERATIONS.get(operation)
        else:
            return

        if not op_info:
            return

        input_type = op_info["input_type"]
        input_label = op_info["input_label"]
        placeholder = op_info["placeholder"]
        description = op_info["description"]

        self._value_group.setTitle(input_label)
        self._value_input.setPlaceholderText(placeholder)
        self._operation_description.setText(description)

        if input_type == "none":
            self._value_input.setEnabled(False)
            self._value_input.clear()
        else:
            self._value_input.setEnabled(True)

    def _get_operations_for_structure(self, name):
        return DATA_STRUCTURE_OPERATIONS.get(name, ["No operations available"])

    def _on_execute(self):
        if not self._current_data_structure:
            return

        operation = self._operation_combo.currentText()
        value_text = self._value_input.text().strip()

        if self._current_data_structure == "Array":
            self._execute_array_operation(operation, value_text)
        elif self._current_data_structure == "Stack":
            self._execute_stack_operation(operation, value_text)
        elif self._current_data_structure == "Queue":
            self._execute_queue_operation(operation, value_text)
        elif self._current_data_structure == "Linked List":
            self._execute_linked_list_operation(operation, value_text)
        elif self._current_data_structure == "Binary Search Tree":
            self._execute_bst_operation(operation, value_text)
        elif self._current_data_structure == "Heap":
            self._execute_heap_operation(operation, value_text)

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
            self._show_error(self._format_error_message(e, operation))
            self._status_bar.showMessage(f"Error: {e}")

    def _format_error_message(self, error: ArrayError, operation: str) -> str:
        """Convert technical error messages to user-friendly ones."""
        error_str = str(error)

        if isinstance(error, ArrayEmptyError):
            empty_messages = {
                "Delete": "Cannot delete: the array is empty.",
                "Search": "Cannot search: the array is empty.",
                "Get": "Cannot get an element: the array is empty.",
                "Update": "Cannot update: the array is empty.",
            }
            return empty_messages.get(operation, error_str)

        if isinstance(error, ArrayIndexError):
            if "out of range" in error_str:
                if self._array:
                    max_index = self._array.size() - 1
                    if max_index >= 0:
                        return f"Invalid index. Valid indices are 0–{max_index}."
                return "Invalid index. The array is empty."
            return error_str

        if isinstance(error, ArrayValueError):
            if "Invalid format" in error_str:
                return "Invalid format. Enter index,value (example: 2,50)."
            if "must be integers" in error_str:
                return "Invalid input. Please enter an integer."
            return error_str

        return error_str

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
        op_info = ARRAY_OPERATIONS["Append"]
        self._update_status("Append", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_insert(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index and value required for Insert (format: index,value)")
        index, value = self._parse_index_value(value_text)
        self._array.insert(index, value)
        self._array_visualizer.set_array(self._array.traverse())
        self._array_visualizer.mark_new(index)
        self._array_visualizer.set_feedback(f"Inserted {value} at index {index}.")
        op_info = ARRAY_OPERATIONS["Insert"]
        self._update_status("Insert", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_delete(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index required for Delete")
        index = self._parse_index(value_text)
        deleted_value = self._array.delete(index)
        self._array_visualizer.set_array(self._array.traverse())
        self._array_visualizer.mark_deleted(index, deleted_value)
        self._array_visualizer.set_feedback(f"Deleted value {deleted_value} from index {index}.")
        op_info = ARRAY_OPERATIONS["Delete"]
        self._update_status("Delete", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_search(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Value required for Search")
        value = self._parse_value(value_text)
        index = self._array.search(value)
        self._array_visualizer.highlight_index(index)
        self._array_visualizer.set_feedback(f"Value {value} found at index {index}.")
        op_info = ARRAY_OPERATIONS["Search"]
        self._update_status("Search", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_update(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index and value required for Update (format: index,value)")
        index, value = self._parse_index_value(value_text)
        old_value = self._array.update(index, value)
        self._array_visualizer.set_array(self._array.traverse())
        self._array_visualizer.select_index(index)
        self._array_visualizer.set_feedback(f"Updated index {index} from {old_value} to {value}.")
        op_info = ARRAY_OPERATIONS["Update"]
        self._update_status("Update", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_get(self, value_text: str):
        if not value_text:
            raise ArrayValueError("Index required for Get")
        index = self._parse_index(value_text)
        value = self._array.get(index)
        self._array_visualizer.highlight_index(index)
        self._array_visualizer.set_feedback(f"arr[{index}] = {value}.")
        op_info = ARRAY_OPERATIONS["Get"]
        self._update_status("Get", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_traverse(self):
        elements = self._array.traverse()
        if not elements:
            self._array_visualizer.set_feedback("Array is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in elements)
            self._array_visualizer.set_feedback(f"Traversal: {traversal_str}")
        op_info = ARRAY_OPERATIONS["Traverse"]
        self._update_status("Traverse", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_clear(self):
        self._array.clear()
        self._array_visualizer.set_array([])
        self._array_visualizer.clear_highlights()
        self._array_visualizer.set_feedback("Array cleared.")
        op_info = ARRAY_OPERATIONS["Clear"]
        self._update_status("Clear", op_info["time_complexity"], op_info["space_complexity"])

    # ============================================================
    # STACK OPERATIONS
    # ============================================================

    def _execute_stack_operation(self, operation: str, value_text: str):
        try:
            if operation == "Push":
                self._execute_push(value_text)
            elif operation == "Pop":
                self._execute_pop()
            elif operation == "Peek":
                self._execute_peek()
            elif operation == "Is Empty":
                self._execute_is_empty()
            elif operation == "Size":
                self._execute_size()
            elif operation == "Traverse":
                self._execute_stack_traverse()
            elif operation == "Clear":
                self._execute_stack_clear()
        except StackError as e:
            self._show_error(self._format_stack_error(e, operation))
            self._status_bar.showMessage(f"Error: {e}")

    def _format_stack_error(self, error: StackError, operation: str) -> str:
        if isinstance(error, StackEmptyError):
            empty_messages = {
                "Pop": "Cannot pop: the stack is empty.",
                "Peek": "Cannot peek: the stack is empty.",
            }
            return empty_messages.get(operation, str(error))
        return str(error)

    def _execute_push(self, value_text: str):
        if not value_text:
            raise StackValueError("Value required for Push")
        value = self._parse_value(value_text)
        self._stack.push(value)
        self._stack_visualizer.set_stack(self._stack.traverse(), preserve_highlights=True)
        self._stack_visualizer.mark_new_top()
        self._stack_visualizer.set_feedback(f"Pushed {value} onto the stack.")
        op_info = STACK_OPERATIONS["Push"]
        self._update_status("Push", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_pop(self):
        popped_value = self._stack.pop()
        remaining = self._stack.traverse()
        self._stack_visualizer.set_stack(remaining, preserve_highlights=True)
        self._stack_visualizer.mark_popped(popped_value)
        self._stack_visualizer.set_feedback(f"Popped {popped_value} from the stack.")
        op_info = STACK_OPERATIONS["Pop"]
        self._update_status("Pop", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_peek(self):
        value = self._stack.peek()
        self._stack_visualizer.set_stack(self._stack.traverse(), preserve_highlights=True)
        self._stack_visualizer.highlight_top()
        self._stack_visualizer.set_feedback(f"Top of stack: {value}")
        op_info = STACK_OPERATIONS["Peek"]
        self._update_status("Peek", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_is_empty(self):
        empty = self._stack.is_empty()
        msg = "Stack is empty." if empty else "Stack is not empty."
        self._stack_visualizer.set_stack(self._stack.traverse(), preserve_highlights=True)
        self._stack_visualizer.set_feedback(msg)
        op_info = STACK_OPERATIONS["Is Empty"]
        self._update_status("Is Empty", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_size(self):
        sz = self._stack.size()
        self._stack_visualizer.set_stack(self._stack.traverse(), preserve_highlights=True)
        self._stack_visualizer.set_feedback(f"Stack size: {sz}")
        op_info = STACK_OPERATIONS["Size"]
        self._update_status("Size", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_stack_traverse(self):
        elements = self._stack.traverse()
        if not elements:
            self._stack_visualizer.set_feedback("Stack is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in elements)
            self._stack_visualizer.set_feedback(f"TOP → {traversal_str} → BOTTOM")
        self._stack_visualizer.set_stack(elements, preserve_highlights=True)
        op_info = STACK_OPERATIONS["Traverse"]
        self._update_status("Traverse", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_stack_clear(self):
        self._stack.clear()
        self._stack_visualizer.set_stack([])
        self._stack_visualizer.clear_highlights()
        self._stack_visualizer.set_feedback("Stack cleared.")
        op_info = STACK_OPERATIONS["Clear"]
        self._update_status("Clear", op_info["time_complexity"], op_info["space_complexity"])

    # ============================================================
    # QUEUE OPERATIONS
    # ============================================================

    def _execute_queue_operation(self, operation: str, value_text: str):
        try:
            if operation == "Enqueue":
                self._execute_enqueue(value_text)
            elif operation == "Dequeue":
                self._execute_dequeue()
            elif operation == "Front":
                self._execute_front()
            elif operation == "Rear":
                self._execute_rear()
            elif operation == "Is Empty":
                self._execute_queue_is_empty()
            elif operation == "Size":
                self._execute_queue_size()
            elif operation == "Traverse":
                self._execute_queue_traverse()
            elif operation == "Clear":
                self._execute_queue_clear()
        except QueueError as e:
            self._show_error(self._format_queue_error(e, operation))
            self._status_bar.showMessage(f"Error: {e}")

    def _format_queue_error(self, error: QueueError, operation: str) -> str:
        if isinstance(error, QueueEmptyError):
            empty_messages = {
                "Dequeue": "Cannot dequeue: the queue is empty.",
                "Front": "Cannot get front: the queue is empty.",
                "Rear": "Cannot get rear: the queue is empty.",
            }
            return empty_messages.get(operation, str(error))
        return str(error)

    def _execute_enqueue(self, value_text: str):
        if not value_text:
            raise QueueValueError("Value required for Enqueue")
        value = self._parse_value(value_text)
        self._queue.enqueue(value)
        self._queue_visualizer.set_queue(self._queue.traverse(), preserve_highlights=True)
        self._queue_visualizer.mark_new_rear()
        self._queue_visualizer.set_feedback(f"Enqueued {value} at the rear.")
        op_info = QUEUE_OPERATIONS["Enqueue"]
        self._update_status("Enqueue", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_dequeue(self):
        dequeued_value = self._queue.dequeue()
        remaining = self._queue.traverse()
        self._queue_visualizer.set_queue(remaining, preserve_highlights=True)
        self._queue_visualizer.mark_dequeued(dequeued_value)
        self._queue_visualizer.set_feedback(f"Dequeued {dequeued_value} from the front.")
        op_info = QUEUE_OPERATIONS["Dequeue"]
        self._update_status("Dequeue", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_front(self):
        value = self._queue.front()
        self._queue_visualizer.set_queue(self._queue.traverse(), preserve_highlights=True)
        self._queue_visualizer.highlight_front()
        self._queue_visualizer.set_feedback(f"Front element: {value}.")
        op_info = QUEUE_OPERATIONS["Front"]
        self._update_status("Front", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_rear(self):
        value = self._queue.rear()
        self._queue_visualizer.set_queue(self._queue.traverse(), preserve_highlights=True)
        self._queue_visualizer.highlight_rear()
        self._queue_visualizer.set_feedback(f"Rear element: {value}.")
        op_info = QUEUE_OPERATIONS["Rear"]
        self._update_status("Rear", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_queue_is_empty(self):
        empty = self._queue.is_empty()
        msg = "Queue is empty." if empty else "Queue is not empty."
        self._queue_visualizer.set_queue(self._queue.traverse(), preserve_highlights=True)
        self._queue_visualizer.set_feedback(msg)
        op_info = QUEUE_OPERATIONS["Is Empty"]
        self._update_status("Is Empty", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_queue_size(self):
        sz = self._queue.size()
        self._queue_visualizer.set_queue(self._queue.traverse(), preserve_highlights=True)
        self._queue_visualizer.set_feedback(f"Queue size = {sz}.")
        op_info = QUEUE_OPERATIONS["Size"]
        self._update_status("Size", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_queue_traverse(self):
        elements = self._queue.traverse()
        if not elements:
            self._queue_visualizer.set_feedback("Queue is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in elements)
            self._queue_visualizer.set_feedback(f"Traversal (FRONT → REAR): {traversal_str}")
        self._queue_visualizer.set_queue(elements, preserve_highlights=True)
        op_info = QUEUE_OPERATIONS["Traverse"]
        self._update_status("Traverse", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_queue_clear(self):
        self._queue.clear()
        self._queue_visualizer.set_queue([])
        self._queue_visualizer.clear_highlights()
        self._queue_visualizer.set_feedback("Queue cleared.")
        op_info = QUEUE_OPERATIONS["Clear"]
        self._update_status("Clear", op_info["time_complexity"], op_info["space_complexity"])

    # ============================================================
    # LINKED LIST OPERATIONS
    # ============================================================

    def _execute_linked_list_operation(self, operation: str, value_text: str):
        try:
            if operation == "Insert at Head":
                self._execute_insert_at_head(value_text)
            elif operation == "Insert at Tail":
                self._execute_insert_at_tail(value_text)
            elif operation == "Insert at Index":
                self._execute_insert_at_index(value_text)
            elif operation == "Delete Head":
                self._execute_delete_head()
            elif operation == "Delete Tail":
                self._execute_delete_tail()
            elif operation == "Delete at Index":
                self._execute_delete_at_index(value_text)
            elif operation == "Search":
                self._execute_ll_search(value_text)
            elif operation == "Update":
                self._execute_ll_update(value_text)
            elif operation == "Get":
                self._execute_ll_get(value_text)
            elif operation == "Traverse":
                self._execute_ll_traverse()
            elif operation == "Size":
                self._execute_ll_size()
            elif operation == "Is Empty":
                self._execute_ll_is_empty()
            elif operation == "Clear":
                self._execute_ll_clear()
        except LinkedListError as e:
            self._show_error(self._format_ll_error(e, operation))
            self._status_bar.showMessage(f"Error: {e}")

    def _format_ll_error(self, error: LinkedListError, operation: str) -> str:
        if isinstance(error, LinkedListEmptyError):
            empty_messages = {
                "Delete Head": "Cannot delete head: the linked list is empty.",
                "Delete Tail": "Cannot delete tail: the linked list is empty.",
                "Delete at Index": "Cannot delete from an empty linked list.",
                "Search": "Cannot search an empty linked list.",
                "Update": "Cannot update an empty linked list.",
                "Get": "Cannot get from an empty linked list.",
            }
            return empty_messages.get(operation, str(error))
        if isinstance(error, LinkedListIndexError):
            error_str = str(error)
            if "out of range" in error_str:
                if self._linked_list:
                    sz = self._linked_list.size()
                    if operation == "Insert at Index":
                        return f"Invalid insertion index. Valid indices are 0–{sz}."
                    if sz > 0:
                        return f"Invalid index. Valid indices are 0–{sz - 1}."
                return "Invalid index. The linked list is empty."
            return error_str
        if isinstance(error, LinkedListValueError):
            error_str = str(error)
            if "not found" in error_str:
                return error_str
            if "Invalid format" in error_str:
                return "Invalid format. Enter index,value (example: 2,50)."
            if "must be integers" in error_str:
                return "Invalid input. Please enter integers."
            return error_str
        return str(error)

    def _parse_ll_index_value(self, text: str) -> tuple:
        parts = [p.strip() for p in text.split(",")]
        if len(parts) != 2:
            raise LinkedListValueError("Invalid format. Use: index,value (e.g., 2,50)")
        try:
            index = int(parts[0])
            value = int(parts[1])
        except ValueError:
            raise LinkedListValueError("Index and value must be integers")
        return index, value

    def _parse_ll_index(self, text: str) -> int:
        try:
            return int(text.strip())
        except ValueError:
            raise LinkedListValueError("Index must be an integer")

    def _parse_ll_value(self, text: str) -> int:
        try:
            return int(text.strip())
        except ValueError:
            raise LinkedListValueError("Value must be an integer")

    def _execute_insert_at_head(self, value_text: str):
        if not value_text:
            raise LinkedListValueError("Value required for Insert at Head")
        value = self._parse_ll_value(value_text)
        self._linked_list.insert_at_head(value)
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.mark_new(0)
        self._linked_list_visualizer.set_feedback(f"Inserted {value} at the head.")
        op_info = LINKED_LIST_OPERATIONS["Insert at Head"]
        self._update_status("Insert at Head", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_insert_at_tail(self, value_text: str):
        if not value_text:
            raise LinkedListValueError("Value required for Insert at Tail")
        value = self._parse_ll_value(value_text)
        self._linked_list.insert_at_tail(value)
        new_idx = self._linked_list.size() - 1
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.mark_new(new_idx)
        self._linked_list_visualizer.set_feedback(f"Inserted {value} at the tail.")
        op_info = LINKED_LIST_OPERATIONS["Insert at Tail"]
        self._update_status("Insert at Tail", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_insert_at_index(self, value_text: str):
        if not value_text:
            raise LinkedListValueError("Index and value required for Insert at Index (format: index,value)")
        index, value = self._parse_ll_index_value(value_text)
        self._linked_list.insert_at_index(index, value)
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.mark_new(index)
        self._linked_list_visualizer.set_feedback(f"Inserted {value} at index {index}.")
        op_info = LINKED_LIST_OPERATIONS["Insert at Index"]
        self._update_status("Insert at Index", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_delete_head(self):
        value = self._linked_list.delete_head()
        self._linked_list_visualizer.set_list(self._linked_list.traverse())
        self._linked_list_visualizer.set_feedback(f"Deleted head node containing {value}.")
        op_info = LINKED_LIST_OPERATIONS["Delete Head"]
        self._update_status("Delete Head", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_delete_tail(self):
        value = self._linked_list.delete_tail()
        self._linked_list_visualizer.set_list(self._linked_list.traverse())
        self._linked_list_visualizer.set_feedback(f"Deleted tail node containing {value}.")
        op_info = LINKED_LIST_OPERATIONS["Delete Tail"]
        self._update_status("Delete Tail", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_delete_at_index(self, value_text: str):
        if not value_text:
            raise LinkedListValueError("Index required for Delete at Index")
        index = self._parse_ll_index(value_text)
        value = self._linked_list.delete_at_index(index)
        self._linked_list_visualizer.set_list(self._linked_list.traverse())
        self._linked_list_visualizer.set_feedback(f"Deleted node containing {value} from index {index}.")
        op_info = LINKED_LIST_OPERATIONS["Delete at Index"]
        self._update_status("Delete at Index", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_ll_search(self, value_text: str):
        if not value_text:
            raise LinkedListValueError("Value required for Search")
        value = self._parse_ll_value(value_text)
        index = self._linked_list.search(value)
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.highlight_index(index)
        self._linked_list_visualizer.set_feedback(f"Value {value} found at index {index}.")
        op_info = LINKED_LIST_OPERATIONS["Search"]
        self._update_status("Search", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_ll_update(self, value_text: str):
        if not value_text:
            raise LinkedListValueError("Index and value required for Update (format: index,value)")
        index, value = self._parse_ll_index_value(value_text)
        old_value = self._linked_list.update(index, value)
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.highlight_index(index)
        self._linked_list_visualizer.set_feedback(f"Updated index {index} from {old_value} to {value}.")
        op_info = LINKED_LIST_OPERATIONS["Update"]
        self._update_status("Update", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_ll_get(self, value_text: str):
        if not value_text:
            raise LinkedListValueError("Index required for Get")
        index = self._parse_ll_index(value_text)
        value = self._linked_list.get(index)
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.highlight_index(index)
        self._linked_list_visualizer.set_feedback(f"Node at index {index} contains {value}.")
        op_info = LINKED_LIST_OPERATIONS["Get"]
        self._update_status("Get", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_ll_traverse(self):
        elements = self._linked_list.traverse()
        if not elements:
            self._linked_list_visualizer.set_feedback("Linked List is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in elements)
            self._linked_list_visualizer.set_feedback(f"Traversal (HEAD → TAIL): {traversal_str}")
        self._linked_list_visualizer.set_list(elements, preserve_highlights=True)
        op_info = LINKED_LIST_OPERATIONS["Traverse"]
        self._update_status("Traverse", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_ll_size(self):
        sz = self._linked_list.size()
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.set_feedback(f"Linked List size = {sz}.")
        op_info = LINKED_LIST_OPERATIONS["Size"]
        self._update_status("Size", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_ll_is_empty(self):
        empty = self._linked_list.is_empty()
        msg = "Linked List is empty." if empty else "Linked List is not empty."
        self._linked_list_visualizer.set_list(self._linked_list.traverse(), preserve_highlights=True)
        self._linked_list_visualizer.set_feedback(msg)
        op_info = LINKED_LIST_OPERATIONS["Is Empty"]
        self._update_status("Is Empty", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_ll_clear(self):
        self._linked_list.clear()
        self._linked_list_visualizer.set_list([])
        self._linked_list_visualizer.clear_highlights()
        self._linked_list_visualizer.set_feedback("Linked List cleared.")
        op_info = LINKED_LIST_OPERATIONS["Clear"]
        self._update_status("Clear", op_info["time_complexity"], op_info["space_complexity"])

    # ============================================================
    # BST OPERATIONS
    # ============================================================

    def _execute_bst_operation(self, operation: str, value_text: str):
        try:
            if operation == "Insert":
                self._execute_bst_insert(value_text)
            elif operation == "Delete":
                self._execute_bst_delete(value_text)
            elif operation == "Search":
                self._execute_bst_search(value_text)
            elif operation == "Inorder Traversal":
                self._execute_bst_inorder()
            elif operation == "Preorder Traversal":
                self._execute_bst_preorder()
            elif operation == "Postorder Traversal":
                self._execute_bst_postorder()
            elif operation == "Level Order Traversal":
                self._execute_bst_level_order()
            elif operation == "Find Minimum":
                self._execute_bst_find_min()
            elif operation == "Find Maximum":
                self._execute_bst_find_max()
            elif operation == "Height":
                self._execute_bst_height()
            elif operation == "Size":
                self._execute_bst_size()
            elif operation == "Is Empty":
                self._execute_bst_is_empty()
            elif operation == "Clear":
                self._execute_bst_clear()
        except BSTError as e:
            self._show_error(self._format_bst_error(e, operation))
            self._status_bar.showMessage(f"Error: {e}")

    def _format_bst_error(self, error: BSTError, operation: str) -> str:
        if isinstance(error, BSTEmptyError):
            empty_messages = {
                "Delete": "Cannot delete from an empty BST.",
                "Search": "Cannot search an empty BST.",
                "Find Minimum": "Cannot find minimum: BST is empty.",
                "Find Maximum": "Cannot find maximum: BST is empty.",
            }
            return empty_messages.get(operation, str(error))
        if isinstance(error, BSTValueError):
            error_str = str(error)
            if "already exists" in error_str:
                return error_str
            if "not found" in error_str:
                return error_str
            return error_str
        return str(error)

    def _parse_bst_value(self, text: str) -> int:
        try:
            return int(text.strip())
        except ValueError:
            raise BSTValueError("Value must be an integer")

    def _execute_bst_insert(self, value_text: str):
        if not value_text:
            raise BSTValueError("Value required for Insert")
        value = self._parse_bst_value(value_text)
        self._bst.insert(value)
        self._bst_visualizer.set_tree(self._bst.root, new_value=value)
        self._bst_visualizer.set_feedback(f"Inserted {value} into BST.")
        op_info = BST_OPERATIONS["Insert"]
        self._update_status("Insert", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_delete(self, value_text: str):
        if not value_text:
            raise BSTValueError("Value required for Delete")
        value = self._parse_bst_value(value_text)
        self._bst.delete(value)
        self._bst_visualizer.set_tree(self._bst.root)
        self._bst_visualizer.set_feedback(f"Deleted {value} from BST.")
        op_info = BST_OPERATIONS["Delete"]
        self._update_status("Delete", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_search(self, value_text: str):
        if not value_text:
            raise BSTValueError("Value required for Search")
        value = self._parse_bst_value(value_text)
        path = self._bst.search_path(value)
        found = self._bst.search(value) is not None
        self._bst_visualizer.set_tree(self._bst.root, highlight_path=path)
        if found:
            self._bst_visualizer.set_feedback(f"Value {value} found in BST.")
        else:
            self._bst_visualizer.set_feedback(f"Value {value} not found in BST.")
        op_info = BST_OPERATIONS["Search"]
        self._update_status("Search", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_inorder(self):
        result = self._bst.inorder()
        if not result:
            self._bst_visualizer.set_feedback("BST is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in result)
            self._bst_visualizer.set_feedback(f"Inorder: {traversal_str}")
        self._bst_visualizer.set_tree(self._bst.root)
        op_info = BST_OPERATIONS["Inorder Traversal"]
        self._update_status("Inorder Traversal", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_preorder(self):
        result = self._bst.preorder()
        if not result:
            self._bst_visualizer.set_feedback("BST is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in result)
            self._bst_visualizer.set_feedback(f"Preorder: {traversal_str}")
        self._bst_visualizer.set_tree(self._bst.root)
        op_info = BST_OPERATIONS["Preorder Traversal"]
        self._update_status("Preorder Traversal", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_postorder(self):
        result = self._bst.postorder()
        if not result:
            self._bst_visualizer.set_feedback("BST is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in result)
            self._bst_visualizer.set_feedback(f"Postorder: {traversal_str}")
        self._bst_visualizer.set_tree(self._bst.root)
        op_info = BST_OPERATIONS["Postorder Traversal"]
        self._update_status("Postorder Traversal", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_level_order(self):
        result = self._bst.level_order()
        if not result:
            self._bst_visualizer.set_feedback("BST is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in result)
            self._bst_visualizer.set_feedback(f"Level Order: {traversal_str}")
        self._bst_visualizer.set_tree(self._bst.root)
        op_info = BST_OPERATIONS["Level Order Traversal"]
        self._update_status("Level Order Traversal", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_find_min(self):
        value = self._bst.find_min()
        self._bst_visualizer.set_tree(self._bst.root)
        self._bst_visualizer.set_feedback(f"Minimum value: {value}")
        op_info = BST_OPERATIONS["Find Minimum"]
        self._update_status("Find Minimum", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_find_max(self):
        value = self._bst.find_max()
        self._bst_visualizer.set_tree(self._bst.root)
        self._bst_visualizer.set_feedback(f"Maximum value: {value}")
        op_info = BST_OPERATIONS["Find Maximum"]
        self._update_status("Find Maximum", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_height(self):
        h = self._bst.height()
        self._bst_visualizer.set_tree(self._bst.root)
        self._bst_visualizer.set_feedback(f"Height of BST: {h}")
        op_info = BST_OPERATIONS["Height"]
        self._update_status("Height", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_size(self):
        sz = self._bst.size()
        self._bst_visualizer.set_tree(self._bst.root)
        self._bst_visualizer.set_feedback(f"Size of BST: {sz}")
        op_info = BST_OPERATIONS["Size"]
        self._update_status("Size", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_is_empty(self):
        empty = self._bst.is_empty()
        msg = "BST is empty." if empty else "BST is not empty."
        self._bst_visualizer.set_tree(self._bst.root)
        self._bst_visualizer.set_feedback(msg)
        op_info = BST_OPERATIONS["Is Empty"]
        self._update_status("Is Empty", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_bst_clear(self):
        self._bst.clear()
        self._bst_visualizer.set_tree(None)
        self._bst_visualizer.clear_highlights()
        self._bst_visualizer.set_feedback("BST cleared.")
        op_info = BST_OPERATIONS["Clear"]
        self._update_status("Clear", op_info["time_complexity"], op_info["space_complexity"])

    # ============================================================
    # HEAP OPERATIONS
    # ============================================================

    def _execute_heap_operation(self, operation: str, value_text: str):
        try:
            if operation == "Insert":
                self._execute_heap_insert(value_text)
            elif operation == "Extract Max":
                self._execute_heap_extract_max()
            elif operation == "Peek":
                self._execute_heap_peek()
            elif operation == "Build Heap":
                self._execute_heap_build(value_text)
            elif operation == "Traverse":
                self._execute_heap_traverse()
            elif operation == "Size":
                self._execute_heap_size()
            elif operation == "Is Empty":
                self._execute_heap_is_empty()
            elif operation == "Clear":
                self._execute_heap_clear()
        except HeapError as e:
            self._show_error(self._format_heap_error(e, operation))
            self._status_bar.showMessage(f"Error: {e}")

    def _format_heap_error(self, error: HeapError, operation: str) -> str:
        if isinstance(error, HeapEmptyError):
            empty_messages = {
                "Extract Max": "Cannot extract maximum: the heap is empty.",
                "Peek": "Cannot peek: the heap is empty.",
            }
            return empty_messages.get(operation, str(error))
        if isinstance(error, HeapValueError):
            return str(error)
        return str(error)

    def _parse_heap_value(self, text: str) -> int:
        try:
            return int(text.strip())
        except ValueError:
            raise HeapValueError("Value must be an integer")

    def _parse_heap_values(self, text: str) -> list:
        parts = [p.strip() for p in text.split(",")]
        if not parts or all(p == "" for p in parts):
            raise HeapValueError("Values required for Build Heap")
        values = []
        for p in parts:
            if p == "":
                raise HeapValueError("Invalid values. Enter comma-separated integers.")
            try:
                values.append(int(p))
            except ValueError:
                raise HeapValueError("Invalid values. Enter comma-separated integers.")
        return values

    def _execute_heap_insert(self, value_text: str):
        if not value_text:
            raise HeapValueError("Value required for Insert")
        value = self._parse_heap_value(value_text)
        self._heap.insert(value)
        self._heap_visualizer.set_heap(self._heap.traverse(), new_index=0)
        self._heap_visualizer.set_feedback(f"Inserted {value} into heap.")
        op_info = HEAP_OPERATIONS["Insert"]
        self._update_status("Insert", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_heap_extract_max(self):
        value = self._heap.extract_max()
        self._heap_visualizer.set_heap(self._heap.traverse())
        self._heap_visualizer.set_feedback(f"Extracted maximum value {value}.")
        op_info = HEAP_OPERATIONS["Extract Max"]
        self._update_status("Extract Max", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_heap_peek(self):
        value = self._heap.peek()
        self._heap_visualizer.set_heap(self._heap.traverse(), highlight_indices=[0])
        self._heap_visualizer.set_feedback(f"Maximum element: {value}.")
        op_info = HEAP_OPERATIONS["Peek"]
        self._update_status("Peek", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_heap_build(self, value_text: str):
        values = self._parse_heap_values(value_text)
        self._heap.build_heap(values)
        self._heap_visualizer.set_heap(self._heap.traverse())
        self._heap_visualizer.set_feedback(f"Built max heap from {len(values)} values.")
        op_info = HEAP_OPERATIONS["Build Heap"]
        self._update_status("Build Heap", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_heap_traverse(self):
        result = self._heap.traverse()
        if not result:
            self._heap_visualizer.set_feedback("Heap is empty.")
        else:
            traversal_str = " → ".join(str(x) for x in result)
            self._heap_visualizer.set_feedback(f"Level-order: {traversal_str}")
        self._heap_visualizer.set_heap(result)
        op_info = HEAP_OPERATIONS["Traverse"]
        self._update_status("Traverse", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_heap_size(self):
        sz = self._heap.size()
        self._heap_visualizer.set_heap(self._heap.traverse())
        self._heap_visualizer.set_feedback(f"Heap size = {sz}.")
        op_info = HEAP_OPERATIONS["Size"]
        self._update_status("Size", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_heap_is_empty(self):
        empty = self._heap.is_empty()
        msg = "Heap is empty." if empty else "Heap is not empty."
        self._heap_visualizer.set_heap(self._heap.traverse())
        self._heap_visualizer.set_feedback(msg)
        op_info = HEAP_OPERATIONS["Is Empty"]
        self._update_status("Is Empty", op_info["time_complexity"], op_info["space_complexity"])

    def _execute_heap_clear(self):
        self._heap.clear()
        self._heap_visualizer.set_heap([])
        self._heap_visualizer.clear_highlights()
        self._heap_visualizer.set_feedback("Heap cleared.")
        op_info = HEAP_OPERATIONS["Clear"]
        self._update_status("Clear", op_info["time_complexity"], op_info["space_complexity"])

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

        if self._stack_visualizer:
            center_widget = self._visualization_panel.parent()
            if center_widget:
                center_layout = center_widget.layout()
                if center_layout:
                    center_layout.removeWidget(self._stack_visualizer)
                    self._stack_visualizer.deleteLater()
                    self._stack_visualizer = None

        if self._queue_visualizer:
            center_widget = self._visualization_panel.parent()
            if center_widget:
                center_layout = center_widget.layout()
                if center_layout:
                    center_layout.removeWidget(self._queue_visualizer)
                    self._queue_visualizer.deleteLater()
                    self._queue_visualizer = None

        if self._linked_list_visualizer:
            center_widget = self._visualization_panel.parent()
            if center_widget:
                center_layout = center_widget.layout()
                if center_layout:
                    center_layout.removeWidget(self._linked_list_visualizer)
                    self._linked_list_visualizer.deleteLater()
                    self._linked_list_visualizer = None

        if self._bst_visualizer:
            center_widget = self._visualization_panel.parent()
            if center_widget:
                center_layout = center_widget.layout()
                if center_layout:
                    center_layout.removeWidget(self._bst_visualizer)
                    self._bst_visualizer.deleteLater()
                    self._bst_visualizer = None

        if self._heap_visualizer:
            center_widget = self._visualization_panel.parent()
            if center_widget:
                center_layout = center_widget.layout()
                if center_layout:
                    center_layout.removeWidget(self._heap_visualizer)
                    self._heap_visualizer.deleteLater()
                    self._heap_visualizer = None

        self._visualization_panel.show()
        center_widget = self._visualization_panel.parent()
        if center_widget:
            center_layout = center_widget.layout()
            if center_layout:
                center_layout.insertWidget(0, self._visualization_panel, 1)

        self._array = None
        self._stack = None
        self._queue = None
        self._linked_list = None
        self._bst = None
        self._heap = None
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
        self._value_group.setTitle(VALUE_LABEL)
        self._value_input.setPlaceholderText("Enter value")
        self._operation_description.setText("")