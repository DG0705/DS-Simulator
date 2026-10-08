"""Dialog for building an undirected graph from an adjacency matrix."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QHeaderView, QLabel, QMessageBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout,
)


class AdjacencyMatrixDialog(QDialog):
    """Editable symmetric 0/1 adjacency matrix."""

    def __init__(self, node_count, parent=None):
        super().__init__(parent)
        self.node_count = node_count
        self.setWindowTitle(f"Adjacency Matrix — {node_count} nodes")
        self.resize(
            min(1100, max(480, node_count * 56)),
            min(720, max(420, node_count * 46)),
        )

        layout = QVBoxLayout(self)
        help_label = QLabel(
            "Enter 1 to create an edge and 0 for no edge. "
            "The matching cell is updated automatically because the graph is undirected."
        )
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        self.table = QTableWidget(node_count, node_count)
        labels = [str(index + 1) for index in range(node_count)]
        self.table.setHorizontalHeaderLabels(labels)
        self.table.setVerticalHeaderLabels(labels)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for row in range(node_count):
            for column in range(node_count):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if row == column:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setBackground(Qt.GlobalColor.lightGray)
                self.table.setItem(row, column, item)
        self.table.cellChanged.connect(self._mirror_cell)
        layout.addWidget(self.table, 1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Build Graph")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _mirror_cell(self, row, column):
        if row == column:
            return
        text = self.table.item(row, column).text().strip()
        opposite = self.table.item(column, row)
        if opposite.text() != text:
            self.table.blockSignals(True)
            opposite.setText(text)
            self.table.blockSignals(False)

    def matrix(self):
        matrix = []
        for row in range(self.node_count):
            values = []
            for column in range(self.node_count):
                text = self.table.item(row, column).text().strip()
                if text not in {"0", "1"}:
                    raise ValueError(
                        f"Cell ({row + 1}, {column + 1}) must contain 0 or 1."
                    )
                value = int(text)
                if row == column and value:
                    raise ValueError("Diagonal cells must be 0 because self-loops are not allowed.")
                values.append(value)
            matrix.append(values)
        if any(matrix[row][column] != matrix[column][row]
               for row in range(self.node_count)
               for column in range(self.node_count)):
            raise ValueError("An undirected graph requires a symmetric adjacency matrix.")
        return matrix

    def accept(self):
        try:
            self.matrix()
        except ValueError as error:
            QMessageBox.warning(self, "Invalid matrix", str(error))
            return
        super().accept()
