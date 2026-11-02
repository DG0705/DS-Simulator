"""Scrollable, step-by-step display for sorting algorithms."""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QScrollArea,
    QSplitter, QTextEdit, QVBoxLayout, QWidget,
)
from PyQt6.QtGui import QColor, QFont, QTextCursor, QTextFormat

from app.core.constants import (
    ACCENT_PRIMARY_LIGHT, ACCENT_SUCCESS_LIGHT, BG_SURFACE,
    BORDER_LIGHT, TEXT_PRIMARY, TEXT_MUTED,
)
from algorithms.sorting_algorithms import (
    BUBBLE_SORT_CODE, COCKTAIL_SORT_CODE, HEAP_SORT_CODE, QUICK_SORT_CODE,
    SHELL_SORT_CODE,
)
from algorithms.searching_algorithms import BINARY_SEARCH_CODE, LINEAR_SEARCH_CODE

SORTING_CODE = {
    "Quick Sort": QUICK_SORT_CODE,
    "Bubble Sort": BUBBLE_SORT_CODE,
    "Heap Sort": HEAP_SORT_CODE,
    "Shell Sort": SHELL_SORT_CODE,
    "Cocktail Sort": COCKTAIL_SORT_CODE,
    "Linear Search": LINEAR_SEARCH_CODE,
    "Binary Search": BINARY_SEARCH_CODE,
}


class SortingVisualizer(QWidget):
    CELL_WIDTH = 64

    def __init__(self, algorithm, parent=None):
        super().__init__(parent)
        self.algorithm = algorithm
        self.displayed_steps = []
        self.final_values = None
        self._code_view = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel(algorithm)
        title.setStyleSheet(f"font-size: 20px; font-weight: 600; color: {TEXT_PRIMARY};")
        layout.addWidget(title)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self._content = QWidget()
        self._rows = QVBoxLayout(self._content)
        self._rows.setContentsMargins(8, 8, 8, 8)
        self._rows.setSpacing(12)
        self._rows.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll.setWidget(self._content)

        if algorithm in SORTING_CODE:
            splitter = QSplitter(Qt.Orientation.Horizontal)
            splitter.addWidget(self._scroll)
            code_panel = QFrame()
            code_panel.setStyleSheet(
                f"QFrame {{ background: #111827; border: 1px solid {BORDER_LIGHT}; "
                f"border-radius: 6px; }}"
            )
            code_layout = QVBoxLayout(code_panel)
            code_title = QLabel(f"{algorithm} Python Code")
            code_title.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")
            code_layout.addWidget(code_title)
            self._code_view = QPlainTextEdit()
            self._code_view.setReadOnly(True)
            self._code_view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
            self._code_view.setFont(QFont("Consolas", 10))
            self._code_view.setPlainText("\n".join(SORTING_CODE[algorithm]))
            self._code_view.setStyleSheet(
                "QPlainTextEdit { background: #111827; color: #E5E7EB; "
                "border: none; padding: 8px; selection-background-color: #F59E0B; }"
            )
            code_layout.addWidget(self._code_view, 1)
            splitter.addWidget(code_panel)
            splitter.setSizes([650, 500])
            layout.addWidget(splitter, 1)
        else:
            layout.addWidget(self._scroll, 1)

        controls = QHBoxLayout()
        self.progress_label = QLabel("Enter numbers and click Execute to begin.")
        self.progress_label.setStyleSheet(f"color: {TEXT_MUTED};")
        controls.addWidget(self.progress_label, 1)
        self.step_button = QPushButton("Step")
        self.skip_button = QPushButton("Skip")
        self.step_button.setEnabled(False)
        self.skip_button.setEnabled(False)
        controls.addWidget(self.step_button)
        controls.addWidget(self.skip_button)
        layout.addLayout(controls)

    def start(self, values, step_count):
        while self._rows.count():
            item = self._rows.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.displayed_steps = []
        self.final_values = None
        self._content.setMinimumWidth(max(0, len(values) * (self.CELL_WIDTH + 6) + 48))
        self._add_row("Input", values, ACCENT_PRIMARY_LIGHT)
        self.progress_label.setText(f"0 of {step_count} steps shown")
        self.step_button.setEnabled(step_count > 0)
        self.skip_button.setEnabled(step_count > 0)
        self._scroll.verticalScrollBar().setValue(0)
        self._highlight_code_line(2 if self.algorithm == "Quick Sort" else 1 if self.algorithm in SORTING_CODE else None)

    def add_step(self, number, description, values, total):
        self.displayed_steps.append((description, list(values)))
        self._add_row(f"Step {number}: {description}", values, BG_SURFACE)
        self._highlight_code_line(getattr(values, "code_line", None))
        self.progress_label.setText(f"{number} of {total} steps shown")
        self._scroll_to_bottom()

    def show_final(self, values, title="Final sorted result"):
        self.final_values = list(values)
        self._add_row(title, values, ACCENT_SUCCESS_LIGHT)
        self.progress_label.setText(f"Completed {len(self.displayed_steps)} steps")
        self.step_button.setEnabled(False)
        self.skip_button.setEnabled(False)
        final_line = {
            "Quick Sort": 22,
            "Bubble Sort": len(BUBBLE_SORT_CODE),
            "Heap Sort": 6,
            "Shell Sort": len(SHELL_SORT_CODE),
            "Cocktail Sort": len(COCKTAIL_SORT_CODE),
            "Linear Search": len(LINEAR_SEARCH_CODE),
            "Binary Search": len(BINARY_SEARCH_CODE),
        }.get(self.algorithm)
        self._highlight_code_line(final_line)
        self._scroll_to_bottom()

    def _highlight_code_line(self, line_number):
        if self._code_view is None or line_number is None:
            return
        block = self._code_view.document().findBlockByNumber(line_number - 1)
        if not block.isValid():
            return
        selection = QTextEdit.ExtraSelection()
        selection.cursor = QTextCursor(block)
        selection.format.setBackground(QColor("#92400E"))
        selection.format.setForeground(QColor("#FFFFFF"))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        self._code_view.setExtraSelections([selection])
        self._code_view.setTextCursor(selection.cursor)
        self._code_view.ensureCursorVisible()

    def _add_row(self, title, values, background):
        row = QFrame()
        row.setStyleSheet(
            f"QFrame {{ background-color: {background}; border: 1px solid {BORDER_LIGHT}; "
            f"border-radius: 6px; }} QLabel {{ border: none; background: transparent; }}"
        )
        column = QVBoxLayout(row)
        column.setContentsMargins(12, 8, 12, 10)
        column.setSpacing(7)
        heading = QLabel(title)
        heading.setStyleSheet(f"font-weight: 600; color: {TEXT_PRIMARY};")
        heading.setWordWrap(True)
        column.addWidget(heading)

        pointers = getattr(values, "pointers", {})
        compared = getattr(values, "compared", set())
        matched = getattr(values, "matched", None)
        if pointers:
            pointer_row = QHBoxLayout()
            pointer_row.setSpacing(6)
            labels_by_index = {}
            for name in ("i", "j", "key", "min", "pivot", "parent", "child", "low", "mid", "high"):
                index = pointers.get(name)
                if index is not None and 0 <= index < len(values):
                    labels_by_index.setdefault(index, []).append(name)
            for index in range(len(values)):
                names = labels_by_index.get(index, [])
                marker = QLabel((" / ".join(names) + "\n↓") if names else "")
                marker.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
                marker.setFixedSize(self.CELL_WIDTH, 34)
                marker.setStyleSheet(
                    "font-size: 11px; font-weight: 700; color: #D97706; "
                    "border: none; background: transparent;"
                )
                pointer_row.addWidget(marker)
            pointer_row.addStretch()
            column.addLayout(pointer_row)

        cells = QHBoxLayout()
        cells.setSpacing(6)
        for index, value in enumerate(values):
            cell = QLabel("·" if value is None else str(value))
            cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell.setFixedSize(self.CELL_WIDTH, 42)
            border_color = "#15803D" if index == matched else "#D97706" if index in compared else BORDER_LIGHT
            border_width = 2 if index == matched or index in compared else 1
            cell_background = ACCENT_SUCCESS_LIGHT if index == matched else "white"
            cell.setStyleSheet(
                f"background: {cell_background}; color: {TEXT_PRIMARY}; "
                f"border: {border_width}px solid {border_color}; border-radius: 5px; font-size: 15px;"
            )
            cells.addWidget(cell)
        cells.addStretch()
        column.addLayout(cells)
        self._rows.addWidget(row)

    def _scroll_to_bottom(self):
        QTimer.singleShot(0, lambda: self._scroll.verticalScrollBar().setValue(
            self._scroll.verticalScrollBar().maximum()
        ))
