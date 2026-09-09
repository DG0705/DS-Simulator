APP_TITLE = "Data Structure Visualizer"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SIDEBAR_WIDTH = 280
VISUALIZATION_PANEL_MIN_WIDTH = 600

DATA_STRUCTURES = [
    "Array",
    "Stack",
    "Queue",
    "Linked List",
    "Binary Search Tree",
    "Heap",
    "Graph"
]

# ============================================================
# THEME COLOR PALETTE
# ============================================================

# Base surfaces
BG_APP = "#F5F7FA"
BG_SURFACE = "#FFFFFF"
BG_SECONDARY = "#EEF1F5"
BG_TERTIARY = "#E5E9F0"

# Text colors
TEXT_PRIMARY = "#1F2937"
TEXT_SECONDARY = "#4B5563"
TEXT_MUTED = "#6B7280"
TEXT_DISABLED = "#9CA3AF"
TEXT_ON_ACCENT = "#FFFFFF"
TEXT_INPUT = "#111827"
TEXT_PLACEHOLDER = "#6B7280"

# Borders
BORDER_LIGHT = "#D1D5DB"
BORDER_MEDIUM = "#9CA3AF"
BORDER_FOCUS = "#2563EB"

# Accent colors
ACCENT_PRIMARY = "#2563EB"
ACCENT_PRIMARY_HOVER = "#1D4ED8"
ACCENT_PRIMARY_PRESSED = "#1E40AF"
ACCENT_PRIMARY_LIGHT = "#DBEAFE"

ACCENT_SUCCESS = "#15803D"
ACCENT_SUCCESS_LIGHT = "#D1FAE5"
ACCENT_SUCCESS_BORDER = "#86EFAC"

ACCENT_ERROR = "#B91C1C"
ACCENT_ERROR_LIGHT = "#FEE2E2"
ACCENT_ERROR_BORDER = "#FCA5A5"

ACCENT_WARNING = "#B45309"
ACCENT_WARNING_LIGHT = "#FEF3C7"
ACCENT_WARNING_BORDER = "#FDE68A"

# Scrollbar
SCROLLBAR_BG = "#F0F0F0"
SCROLLBAR_HANDLE = "#CCCCCC"
SCROLLBAR_HANDLE_HOVER = "#BBBBBB"

# ============================================================
# WIDGET STYLES (built from theme colors)
# ============================================================

PLACEHOLDER_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {BG_TERTIARY};
    color: {TEXT_DISABLED};
    border: 1px solid {BORDER_LIGHT};
    border-radius: 6px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {BORDER_LIGHT};
    border-color: {BORDER_MEDIUM};
}}
QPushButton:disabled {{
    background-color: {BG_SECONDARY};
    color: {TEXT_DISABLED};
    border-color: {BORDER_LIGHT};
}}
"""

ENABLED_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_LIGHT};
    border-radius: 6px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {BG_SECONDARY};
    border-color: {BORDER_MEDIUM};
}}
QPushButton:pressed {{
    background-color: {ACCENT_PRIMARY_LIGHT};
    border-color: {ACCENT_PRIMARY};
}}
QPushButton:checked {{
    background-color: {ACCENT_PRIMARY_LIGHT};
    border-color: {ACCENT_PRIMARY};
    color: {ACCENT_PRIMARY};
}}
"""

SIDEBAR_STYLE = f"""
QWidget {{
    background-color: {BG_SECONDARY};
    border-right: 1px solid {BORDER_LIGHT};
}}
QLabel#sectionTitle {{
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 8px 16px 4px 16px;
}}
"""

VISUALIZATION_PANEL_STYLE = f"""
QWidget {{
    background-color: {BG_SURFACE};
}}
QLabel#titleLabel {{
    font-size: 28px;
    font-weight: 300;
    color: {TEXT_PRIMARY};
}}
QLabel#subtitleLabel {{
    font-size: 16px;
    font-weight: 400;
    color: {TEXT_MUTED};
}}
"""

CONTROL_PANEL_STYLE = f"""
QWidget {{
    background-color: {BG_SECONDARY};
    border-top: 1px solid {BORDER_LIGHT};
}}
QGroupBox {{
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_LIGHT};
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 16px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    background-color: {BG_SECONDARY};
}}
QComboBox {{
    padding: 8px 12px;
    border: 1px solid {BORDER_LIGHT};
    border-radius: 4px;
    background-color: {BG_SURFACE};
    color: {TEXT_INPUT};
    font-size: 13px;
    min-width: 140px;
}}
QComboBox:hover {{
    border-color: {BORDER_MEDIUM};
}}
QComboBox:focus {{
    border-color: {BORDER_FOCUS};
}}
QComboBox:disabled {{
    background-color: {BG_TERTIARY};
    color: {TEXT_DISABLED};
    border-color: {BORDER_LIGHT};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {TEXT_MUTED};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {BG_SURFACE};
    border: 1px solid {BORDER_LIGHT};
    selection-background-color: {ACCENT_PRIMARY_LIGHT};
    selection-color: {ACCENT_PRIMARY};
    color: {TEXT_PRIMARY};
    padding: 4px;
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px 12px;
    border-radius: 4px;
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: {BG_SECONDARY};
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: {ACCENT_PRIMARY_LIGHT};
    color: {ACCENT_PRIMARY};
}}
QLineEdit {{
    padding: 8px 12px;
    border: 1px solid {BORDER_LIGHT};
    border-radius: 4px;
    background-color: {BG_SURFACE};
    color: {TEXT_INPUT};
    font-size: 13px;
}}
QLineEdit:focus {{
    border-color: {BORDER_FOCUS};
}}
QLineEdit:disabled {{
    background-color: {BG_TERTIARY};
    color: {TEXT_DISABLED};
    border-color: {BORDER_LIGHT};
}}
QLineEdit::placeholder {{
    color: {TEXT_PLACEHOLDER};
}}
QPushButton {{
    padding: 8px 16px;
    border: 1px solid {BORDER_LIGHT};
    border-radius: 4px;
    background-color: {BG_SURFACE};
    font-size: 13px;
    font-weight: 500;
    color: {TEXT_PRIMARY};
}}
QPushButton:hover {{
    background-color: {BG_SECONDARY};
    border-color: {BORDER_MEDIUM};
}}
QPushButton:pressed {{
    background-color: {BG_TERTIARY};
}}
QPushButton:disabled {{
    background-color: {BG_TERTIARY};
    color: {TEXT_DISABLED};
    border-color: {BORDER_LIGHT};
}}
QPushButton#executeButton {{
    background-color: {ACCENT_PRIMARY};
    color: {TEXT_ON_ACCENT};
    border-color: {ACCENT_PRIMARY};
}}
QPushButton#executeButton:hover {{
    background-color: {ACCENT_PRIMARY_HOVER};
    border-color: {ACCENT_PRIMARY_HOVER};
}}
QPushButton#executeButton:pressed {{
    background-color: {ACCENT_PRIMARY_PRESSED};
    border-color: {ACCENT_PRIMARY_PRESSED};
}}
QPushButton#executeButton:disabled {{
    background-color: {BORDER_LIGHT};
    color: {TEXT_DISABLED};
    border-color: {BORDER_LIGHT};
}}
QPushButton#resetButton {{
    background-color: {BG_SURFACE};
    color: {TEXT_SECONDARY};
    border-color: {BORDER_LIGHT};
}}
QPushButton#resetButton:hover {{
    background-color: {BG_SECONDARY};
    color: {TEXT_PRIMARY};
    border-color: {BORDER_MEDIUM};
}}
QPushButton#resetButton:pressed {{
    background-color: {BG_TERTIARY};
}}
"""

STATUS_BAR_STYLE = f"""
QStatusBar {{
    background-color: {BG_SECONDARY};
    border-top: 1px solid {BORDER_LIGHT};
    color: {TEXT_MUTED};
    font-size: 12px;
    padding: 4px 12px;
}}
"""

MAIN_WINDOW_STYLE = f"""
QMainWindow {{
    background-color: {BG_APP};
}}
"""

# Scrollbar styles (shared)
SCROLLBAR_STYLE = f"""
QScrollArea {{
    border: none;
    background-color: transparent;
}}
QScrollBar:vertical, QScrollBar:horizontal {{
    background-color: {SCROLLBAR_BG};
    width: 8px;
    height: 8px;
    border: none;
}}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background-color: {SCROLLBAR_HANDLE};
    border-radius: 4px;
    min-height: 30px;
    min-width: 30px;
}}
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {{
    background-color: {SCROLLBAR_HANDLE_HOVER};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    height: 0;
    width: 0;
}}
"""

# Text constants
DATA_STRUCTURES_SECTION_TITLE = "Data Structures"
SELECT_DATA_STRUCTURE_TEXT = "Select a Data Structure"
CHOOSE_DATA_STRUCTURE_TEXT = "Choose a data structure from the sidebar to begin visualization."
NO_OPERATION_SELECTED = "No operation selected"
OPERATION_LABEL = "Operation"
VALUE_LABEL = "Value"
EXECUTE_BUTTON_TEXT = "Execute"
RESET_BUTTON_TEXT = "Reset"

# ============================================================
# OPERATION DEFINITIONS
# ============================================================

ARRAY_OPERATIONS = {
    "Append": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value (e.g. 60)",
        "description": "Append adds a value to the end of the array.",
        "time_complexity": "O(1) amortized",
        "space_complexity": "O(1) auxiliary",
    },
    "Insert": {
        "input_type": "index_value",
        "input_label": "Index, Value",
        "placeholder": "Enter index,value (e.g. 2,50)",
        "description": "Insert places a value at the specified index.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Delete": {
        "input_type": "index",
        "input_label": "Index",
        "placeholder": "Enter index (e.g. 6)",
        "description": "Delete removes the element at the specified index.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Search": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value to search (e.g. 50)",
        "description": "Search finds the first occurrence of a value.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Update": {
        "input_type": "index_value",
        "input_label": "Index, Value",
        "placeholder": "Enter index,value (e.g. 2,50)",
        "description": "Update replaces the value at the specified index.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Get": {
        "input_type": "index",
        "input_label": "Index",
        "placeholder": "Enter index (e.g. 2)",
        "description": "Get returns the value at the specified index.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Traverse": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Traverse displays all array elements in order.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Clear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Clear removes all elements from the array.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
}

ARRAY_OPERATION_NAMES = list(ARRAY_OPERATIONS.keys())

STACK_OPERATIONS = {
    "Push": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value to push (e.g. 42)",
        "description": "Push adds a value to the top of the stack.",
        "time_complexity": "O(1) amortized",
        "space_complexity": "O(1) auxiliary",
    },
    "Pop": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Pop removes and returns the top value.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Peek": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Peek returns the top value without removing it.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Is Empty": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Check if the stack is empty.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Size": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the number of elements in the stack.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Traverse": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Display all elements from TOP to BOTTOM.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Clear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Clear removes all elements from the stack.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
}

STACK_OPERATION_NAMES = list(STACK_OPERATIONS.keys())

QUEUE_OPERATIONS = {
    "Enqueue": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value to enqueue (e.g. 50)",
        "description": "Enqueue adds a value to the rear of the queue.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1) auxiliary",
    },
    "Dequeue": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Dequeue removes and returns the front value.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Front": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Front returns the front value without removing it.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Rear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Rear returns the rear value without removing it.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Is Empty": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Check if the queue is empty.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Size": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the number of elements in the queue.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Traverse": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Display all elements from FRONT to REAR.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Clear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Clear removes all elements from the queue.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
}

QUEUE_OPERATION_NAMES = list(QUEUE_OPERATIONS.keys())

LINKED_LIST_OPERATIONS = {
    "Insert at Head": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value (e.g. 50)",
        "description": "Insert a new node at the head of the list.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Insert at Tail": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value (e.g. 50)",
        "description": "Insert a new node at the tail of the list.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Insert at Index": {
        "input_type": "index_value",
        "input_label": "Index, Value",
        "placeholder": "Enter index,value (e.g. 2,50)",
        "description": "Insert a new node at the specified index.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
    },
    "Delete Head": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Remove and return the head node.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Delete Tail": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Remove and return the tail node.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
    },
    "Delete at Index": {
        "input_type": "index",
        "input_label": "Index",
        "placeholder": "Enter index (e.g. 2)",
        "description": "Remove the node at the specified index.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
    },
    "Search": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value to search (e.g. 50)",
        "description": "Find the first occurrence of a value.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
    },
    "Update": {
        "input_type": "index_value",
        "input_label": "Index, Value",
        "placeholder": "Enter index,value (e.g. 2,50)",
        "description": "Replace the value at the specified index.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
    },
    "Get": {
        "input_type": "index",
        "input_label": "Index",
        "placeholder": "Enter index (e.g. 2)",
        "description": "Return the value at the specified index.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
    },
    "Traverse": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Display all nodes from HEAD to TAIL.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Size": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the number of nodes.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Is Empty": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Check if the linked list is empty.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Clear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Remove all nodes from the list.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
}

LINKED_LIST_OPERATION_NAMES = list(LINKED_LIST_OPERATIONS.keys())

BST_OPERATIONS = {
    "Insert": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value (e.g. 50)",
        "description": "Insert a value into the BST. Duplicates are not allowed.",
        "time_complexity": "O(log n) average, O(n) worst",
        "space_complexity": "O(log n) recursion stack",
    },
    "Delete": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value to delete (e.g. 50)",
        "description": "Remove a value from the BST.",
        "time_complexity": "O(log n) average, O(n) worst",
        "space_complexity": "O(log n) recursion stack",
    },
    "Search": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value to search (e.g. 50)",
        "description": "Find a value in the BST.",
        "time_complexity": "O(log n) average, O(n) worst",
        "space_complexity": "O(log n) recursion stack",
    },
    "Inorder Traversal": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Visit nodes in sorted order (Left → Root → Right).",
        "time_complexity": "O(n)",
        "space_complexity": "O(h) recursion stack",
    },
    "Preorder Traversal": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Visit nodes in root-first order (Root → Left → Right).",
        "time_complexity": "O(n)",
        "space_complexity": "O(h) recursion stack",
    },
    "Postorder Traversal": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Visit nodes in children-first order (Left → Right → Root).",
        "time_complexity": "O(n)",
        "space_complexity": "O(h) recursion stack",
    },
    "Level Order Traversal": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Visit nodes level by level (BFS).",
        "time_complexity": "O(n)",
        "space_complexity": "O(w) where w = max width",
    },
    "Find Minimum": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Find the minimum value in the BST.",
        "time_complexity": "O(log n) average, O(n) worst",
        "space_complexity": "O(1)",
    },
    "Find Maximum": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Find the maximum value in the BST.",
        "time_complexity": "O(log n) average, O(n) worst",
        "space_complexity": "O(1)",
    },
    "Height": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the height of the tree. Empty = 0, single node = 1.",
        "time_complexity": "O(n)",
        "space_complexity": "O(h) recursion stack",
    },
    "Size": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the number of nodes.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Is Empty": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Check if the BST is empty.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Clear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Remove all nodes from the BST.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
}

BST_OPERATION_NAMES = list(BST_OPERATIONS.keys())

HEAP_OPERATIONS = {
    "Insert": {
        "input_type": "value",
        "input_label": "Value",
        "placeholder": "Enter value (e.g. 50)",
        "description": "Insert a value into the Max Heap.",
        "time_complexity": "O(log n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Extract Max": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Remove and return the maximum value from the heap.",
        "time_complexity": "O(log n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Peek": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the maximum value without removing it.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Build Heap": {
        "input_type": "values",
        "input_label": "Values",
        "placeholder": "Enter values separated by commas (e.g. 50,30,70,20)",
        "description": "Build a max heap from a list of values using bottom-up construction.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
    },
    "Traverse": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Display the internal heap array (level-order representation).",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) auxiliary",
    },
    "Size": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the number of elements in the heap.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Is Empty": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Check if the heap is empty.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Clear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Remove all elements from the heap.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
}

HEAP_OPERATION_NAMES = list(HEAP_OPERATIONS.keys())

GRAPH_OPERATIONS = {
    "Add Vertex": {
        "input_type": "value",
        "input_label": "Vertex",
        "placeholder": "Enter vertex (e.g. A)",
        "description": "Add a vertex to the graph.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Add Edge": {
        "input_type": "pair",
        "input_label": "Vertices",
        "placeholder": "Enter two vertices, e.g. A,B",
        "description": "Add an undirected edge between two vertices.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Remove Vertex": {
        "input_type": "value",
        "input_label": "Vertex",
        "placeholder": "Enter vertex (e.g. A)",
        "description": "Remove a vertex and all its edges.",
        "time_complexity": "O(degree)",
        "space_complexity": "O(1)",
    },
    "Remove Edge": {
        "input_type": "pair",
        "input_label": "Vertices",
        "placeholder": "Enter two vertices, e.g. A,B",
        "description": "Remove an undirected edge between two vertices.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Neighbors": {
        "input_type": "value",
        "input_label": "Vertex",
        "placeholder": "Enter vertex (e.g. A)",
        "description": "Return the list of adjacent vertices.",
        "time_complexity": "O(degree * log(degree))",
        "space_complexity": "O(degree)",
    },
    "Vertices": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return all vertices in insertion order.",
        "time_complexity": "O(V)",
        "space_complexity": "O(V)",
    },
    "Edges": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return all unique undirected edges.",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(E)",
    },
    "BFS": {
        "input_type": "value",
        "input_label": "Start Vertex",
        "placeholder": "Enter start vertex (e.g. A)",
        "description": "Breadth-first traversal. Visits vertices level by level using a queue.",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
    },
    "DFS": {
        "input_type": "value",
        "input_label": "Start Vertex",
        "placeholder": "Enter start vertex (e.g. A)",
        "description": "Depth-first traversal. Explores branches deeply before backtracking using a stack.",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
    },
    "Size": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Return the number of vertices.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Is Empty": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Check if the graph is empty.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Has Vertex": {
        "input_type": "value",
        "input_label": "Vertex",
        "placeholder": "Enter vertex (e.g. A)",
        "description": "Check if a vertex exists in the graph.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Has Edge": {
        "input_type": "pair",
        "input_label": "Vertices",
        "placeholder": "Enter two vertices, e.g. A,B",
        "description": "Check if an edge exists between two vertices.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
    "Clear": {
        "input_type": "none",
        "input_label": "Input",
        "placeholder": "No input required",
        "description": "Remove all vertices and edges.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
    },
}

GRAPH_OPERATION_NAMES = list(GRAPH_OPERATIONS.keys())

DATA_STRUCTURE_OPERATIONS = {
    "Array": ARRAY_OPERATION_NAMES,
    "Stack": STACK_OPERATION_NAMES,
    "Queue": QUEUE_OPERATION_NAMES,
    "Linked List": LINKED_LIST_OPERATION_NAMES,
    "Binary Search Tree": BST_OPERATION_NAMES,
    "Heap": HEAP_OPERATION_NAMES,
    "Graph": GRAPH_OPERATION_NAMES,
}