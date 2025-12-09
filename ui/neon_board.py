from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF

class NeonQuoridorBoard(QWidget):
    def __init__(self, rows=9, cols=9):
        super().__init__()
        self.rows = rows
        self.cols = cols

        # Game state placeholders
        self.p1_pos = (4, 0)
        self.p2_pos = (4, 8)

        self.p1_walls = []
        self.p2_walls = []
        self.highlight_moves = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        cell_w = w / self.cols
        cell_h = h / self.rows

        # Colors
        neon_cyan = QColor("#00eaff")
        neon_pink = QColor("#ff0080")
        grid_color = QColor("#2b2b2e")

        # Draw grid squares
        for r in range(self.rows):
            for c in range(self.cols):
                rect = QRectF(c * cell_w, r * cell_h, cell_w, cell_h)
                pen = QPen(grid_color, 2)
                painter.setPen(pen)
                painter.drawRect(rect)

        # Highlight moves with glowing cyan
        for r, c in self.highlight_moves:
            rect = QRectF(c * cell_w, r * cell_h, cell_w, cell_h)
            painter.setBrush(QBrush(neon_cyan.withAlpha(60)))
            painter.setPen(QPen(neon_cyan, 2))
            painter.drawRect(rect)

        # Draw players
        def draw_piece(r, c, color):
            x = c * cell_w + cell_w / 2
            y = r * cell_h + cell_h / 2
            radius = min(cell_w, cell_h) * 0.32
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color, 4))
            painter.drawEllipse(QRectF(x - radius, y - radius, radius * 2, radius * 2))

        draw_piece(*self.p1_pos, neon_cyan)
        draw_piece(*self.p2_pos, neon_pink)

        # Draw walls (horizontal and vertical)
        wall_thickness = 12

        for r, c in self.p1_walls:
            rect = QRectF(c * cell_w, r * cell_h + cell_h - 5, cell_w * 2, wall_thickness)
            painter.fillRect(rect, neon_cyan)

        for r, c in self.p2_walls:
            rect = QRectF(c * cell_w, r * cell_h + cell_h - 5, cell_w * 2, wall_thickness)
            painter.fillRect(rect, neon_pink)
