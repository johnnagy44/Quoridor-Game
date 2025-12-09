from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QFont, QLinearGradient, QBrush, QColor
from PyQt6.QtCore import Qt, QPointF

class GlowGradientLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.gradient_colors = [
            QColor("#00eaff"),  # neon cyan
            QColor("#00ff95"),  # neon green
            QColor("#ff00ff")   # neon magenta
        ]

        self.glow_color = QColor(255, 0, 255, 180)   # neon magenta glow
        self.glow_strength = 6                      # how strong the glow is

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        rect = self.rect()

        # --- Neon Glow Layer ---
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.glow_color)

        # draw multiple blurred glow outlines
        for s in range(self.glow_strength):
            painter.drawText(
                rect.adjusted(-s, -s, s, s),
                Qt.AlignmentFlag.AlignCenter,
                self.text()
            )

        # --- Gradient Text Layer ---
        gradient = QLinearGradient(0, 0, rect.width(), 0)
        count = len(self.gradient_colors)
        for i, color in enumerate(self.gradient_colors):
            gradient.setColorAt(i / (count - 1), color)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))

        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
