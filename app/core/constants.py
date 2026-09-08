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

PLACEHOLDER_BUTTON_STYLE = """
QPushButton {
    background-color: #e0e0e0;
    color: #888888;
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #d5d5d5;
    border-color: #bbbbbb;
}
QPushButton:disabled {
    background-color: #f0f0f0;
    color: #aaaaaa;
    border-color: #dddddd;
}
"""

SIDEBAR_STYLE = """
QWidget {
    background-color: #fafafa;
    border-right: 1px solid #e0e0e0;
}
QLabel#sectionTitle {
    font-size: 13px;
    font-weight: 600;
    color: #666666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 8px 16px 4px 16px;
}
"""

VISUALIZATION_PANEL_STYLE = """
QWidget {
    background-color: #ffffff;
}
QLabel#titleLabel {
    font-size: 28px;
    font-weight: 300;
    color: #333333;
}
QLabel#subtitleLabel {
    font-size: 16px;
    font-weight: 400;
    color: #888888;
}
"""

CONTROL_PANEL_STYLE = """
QWidget {
    background-color: #fafafa;
    border-top: 1px solid #e0e0e0;
}
QGroupBox {
    font-size: 13px;
    font-weight: 600;
    color: #444444;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 16px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    background-color: #fafafa;
}
QComboBox {
    padding: 8px 12px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
    font-size: 13px;
    min-width: 140px;
}
QComboBox:hover {
    border-color: #bbbbbb;
}
QComboBox:focus {
    border-color: #0078d4;
}
QLineEdit {
    padding: 8px 12px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
    font-size: 13px;
}
QLineEdit:focus {
    border-color: #0078d4;
}
QPushButton {
    padding: 8px 16px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
    font-size: 13px;
    font-weight: 500;
    color: #333333;
}
QPushButton:hover {
    background-color: #f0f0f0;
    border-color: #bbbbbb;
}
QPushButton:pressed {
    background-color: #e0e0e0;
}
QPushButton#executeButton {
    background-color: #0078d4;
    color: #ffffff;
    border-color: #0078d4;
}
QPushButton#executeButton:hover {
    background-color: #0063b1;
    border-color: #0063b1;
}
QPushButton#resetButton {
    background-color: #ffffff;
    color: #666666;
}
QPushButton#resetButton:hover {
    background-color: #f0f0f0;
    color: #333333;
}
"""

STATUS_BAR_STYLE = """
QStatusBar {
    background-color: #fafafa;
    border-top: 1px solid #e0e0e0;
    color: #666666;
    font-size: 12px;
    padding: 4px 12px;
}
"""

MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #ffffff;
}
"""

DATA_STRUCTURES_SECTION_TITLE = "Data Structures"
SELECT_DATA_STRUCTURE_TEXT = "Select a Data Structure"
CHOOSE_DATA_STRUCTURE_TEXT = "Choose a data structure from the sidebar to begin visualization."
NO_OPERATION_SELECTED = "No operation selected"
OPERATION_LABEL = "Operation"
VALUE_LABEL = "Value"
EXECUTE_BUTTON_TEXT = "Execute"
RESET_BUTTON_TEXT = "Reset"