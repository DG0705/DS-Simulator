"""Live display of important data-structure and algorithm variables."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHeaderView, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout


class VariableStatePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)
        self.setMaximumHeight(285)
        self.setStyleSheet("QFrame { background: #F9FAFB; border-top: 1px solid #D1D5DB; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 10)
        title = QLabel("Important Variables")
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: #111827;")
        layout.addWidget(title)
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Variable", "Current value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)

    def set_variables(self, variables):
        rows = list(variables.items())
        self.table.setRowCount(len(rows))
        for row, (name, value) in enumerate(rows):
            full_value = str(value)
            shown = full_value if len(full_value) <= 90 else full_value[:87] + "..."
            name_item = QTableWidgetItem(str(name))
            value_item = QTableWidgetItem(shown)
            value_item.setToolTip(full_value)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, value_item)
