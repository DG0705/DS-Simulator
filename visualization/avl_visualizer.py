"""AVL tree view with balance factors and manual step controls."""

from PyQt6.QtCore import QEasingCurve, QVariantAnimation, pyqtSignal
from visualization.bst_visualizer import BSTVisualizer


class AVLVisualizer(BSTVisualizer):
    LEVEL_HEIGHT = 100
    ROTATION_DURATION_MS = 1100
    animation_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._show_balance = True
        self._feedback_label.setFixedHeight(58)
        self._feedback_label.setWordWrap(True)
        self._rotation_animation = QVariantAnimation(self)
        self._rotation_animation.setStartValue(0.0)
        self._rotation_animation.setEndValue(1.0)
        self._rotation_animation.setDuration(self.ROTATION_DURATION_MS)
        self._rotation_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._rotation_animation.valueChanged.connect(self._on_animation_frame)
        self._rotation_animation.finished.connect(self._on_animation_finished)
        self._current_step_number = 0
        self._total_steps = 0

        self.progress_label.setText("BF = left height - right height")

    def prepare_steps(self, count):
        self._rotation_animation.stop()
        self._animation_origin = {}
        self._animation_progress = 1.0
        self._current_step_number = 0
        self._total_steps = count
        self.step_button.setEnabled(count > 0)
        self.progress_label.setText(f"0 of {count} steps shown")
        self.set_feedback("Click Step to inspect the next AVL calculation or rotation.")

    def show_step(self, step, number, total):
        old_screen_positions = {}
        if self._positions:
            old_scale, old_x, old_y = self._paint_area._fit_transform()
            old_screen_positions = {
                value: (old_x + x * old_scale, old_y + y * old_scale)
                for x, y, value, _ in self._positions.values()
            }
        self.set_tree(step.root)
        self._focus_values = set(step.focus_values)
        self._rotation_values = set(step.rotation_values)
        self._current_step_number = number
        self._total_steps = total
        self._paint_area.update()
        self.progress_label.setText(f"{number} of {total} steps shown")
        rotation = f"[{step.rotation_type}] " if step.rotation_type else ""
        self.set_feedback(f"Step {number}/{total}: {rotation}{step.description}")

        if step.rotation_type and old_screen_positions and self._positions:
            new_scale, new_x, new_y = self._paint_area._fit_transform()
            moved = any(
                value in old_screen_positions and
                abs(new_x + x * new_scale - old_screen_positions[value][0]) +
                abs(new_y + y * new_scale - old_screen_positions[value][1]) > 1
                for x, y, value, _ in self._positions.values()
            )
            if moved:
                self._animation_origin = old_screen_positions
                self._animation_progress = 0.0
                self.progress_label.setText(
                    f"Animating {step.rotation_type} rotation · step {number} of {total}"
                )
                self.step_button.setEnabled(False)
                self._rotation_animation.start()
                return True
        self._animation_origin = {}
        self._animation_progress = 1.0
        return False

    def _on_animation_frame(self, value):
        self._animation_progress = float(value)
        self._paint_area.update()

    def _on_animation_finished(self):
        self._animation_progress = 1.0
        self._animation_origin = {}
        self._paint_area.update()
        self.progress_label.setText(
            f"{self._current_step_number} of {self._total_steps} steps shown"
        )
        if self._current_step_number < self._total_steps:
            self.step_button.setEnabled(True)
        self.animation_finished.emit()

    def finish_steps(self):
        self.step_button.setEnabled(False)
        self.progress_label.setText("AVL operation complete · BF = left height - right height")
