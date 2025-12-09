from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt

CELL = 60
OFFSET = 10

NEON_GRID = QColor(0, 234, 255)   # cyan neon
NEON_P1 = QColor(0, 255, 255)     # cyan glow
NEON_P2 = QColor(255, 0, 255)     # magenta glow
NEON_WALL = QColor(255, 0, 150)   # pink wall
BOARD_BG = QColor(12, 12, 16)     # very dark
GRID_SHADOW = QColor(0, 120, 140, 180)


class BoardWidget(QWidget):

    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.game = game_state
        self.size = game_state.board.size
        self.setMinimumSize(self.size * CELL, self.size * CELL)

        # neon hover highlight
        self.hover_row = None
        self.hover_col = None
        self.setMouseTracking(True)

    # -------------------------------------------------
    # PAINT EVENT
    # -------------------------------------------------
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.draw_background(p)
        self.draw_grid(p)
        self.draw_hover(p)
        self.draw_walls(p)
        self.draw_players(p)

    # -------------------------------------------------
    # DARK BACKGROUND
    # -------------------------------------------------
    def draw_background(self, p: QPainter):
        p.fillRect(self.rect(), BOARD_BG)

    # -------------------------------------------------
    # NEON GRID
    # -------------------------------------------------
    def draw_grid(self, p: QPainter):
        pen = QPen(NEON_GRID, 2)
        p.setPen(pen)

        for r in range(self.size):
            for c in range(self.size):
                x = c * CELL
                y = r * CELL

                # glowing shadow under grid cell
                p.setPen(QPen(GRID_SHADOW, 12))
                p.drawRect(x, y, CELL, CELL)

                # actual neon cell
                p.setPen(QPen(NEON_GRID, 2))
                p.drawRect(x, y, CELL, CELL)

    # -------------------------------------------------
    # CELL HOVER GLOW
    # -------------------------------------------------
    def draw_hover(self, p: QPainter):
        if self.hover_row is None:
            return

        x = self.hover_col * CELL
        y = self.hover_row * CELL

        glow = QColor(0, 255, 255, 80)
        p.setBrush(QBrush(glow))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(x, y, CELL, CELL)

    # -------------------------------------------------
    # PLAYERS (NEON GLOWING)
    # -------------------------------------------------
    def draw_players(self, p: QPainter):
        # PLAYER 1 (cyan)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(NEON_P1))

        p1 = self.game.players[0]
        x = p1.c * CELL + OFFSET
        y = p1.r * CELL + OFFSET

        # outer glow
        p.setBrush(QBrush(QColor(0, 255, 255, 120)))
        p.drawEllipse(x - 5, y - 5, CELL - 2*OFFSET + 10, CELL - 2*OFFSET + 10)

        # inner piece
        p.setBrush(QBrush(NEON_P1))
        p.drawEllipse(x, y, CELL - 2*OFFSET, CELL - 2*OFFSET)

        # PLAYER 2 (pink)
        p2 = self.game.players[1]
        x = p2.c * CELL + OFFSET
        y = p2.r * CELL + OFFSET

        p.setBrush(QBrush(QColor(255, 0, 255, 120)))
        p.drawEllipse(x - 5, y - 5, CELL - 2*OFFSET + 10, CELL - 2*OFFSET + 10)

        p.setBrush(QBrush(NEON_P2))
        p.drawEllipse(x, y, CELL - 2*OFFSET, CELL - 2*OFFSET)

    # -------------------------------------------------
    # NEON WALLS (PINK)
    # -------------------------------------------------
    def draw_walls(self, p: QPainter):
        p.setPen(Qt.PenStyle.NoPen)

        # shadow/glow
        glow = QColor(255, 0, 150, 120)
        p.setBrush(glow)

        # horizontal walls
        for r in range(self.size - 1):
            for c in range(self.size - 1):
                if self.game.board.h_walls[r][c]:
                    x = c * CELL
                    y = (r + 1) * CELL - 5

                    # glow
                    p.drawRect(x - 3, y - 3, CELL*2 + 6, 16)

                    # main neon wall
                    p.setBrush(QBrush(NEON_WALL))
                    p.drawRect(x, y, CELL*2, 10)

                    p.setBrush(glow)

        # vertical walls
        for r in range(self.size - 1):
            for c in range(self.size - 1):
                if self.game.board.v_walls[r][c]:
                    x = (c + 1) * CELL - 5
                    y = r * CELL

                    # glow
                    p.drawRect(x - 3, y - 3, 16, CELL*2 + 6)

                    p.setBrush(QBrush(NEON_WALL))
                    p.drawRect(x, y, 10, CELL*2)

                    p.setBrush(glow)

    # -------------------------------------------------
    # MOUSE HOVER
    # -------------------------------------------------
    def mouseMoveEvent(self, event):
        pos = event.position()
        col = int(pos.x() // CELL)
        row = int(pos.y() // CELL)

        if 0 <= row < self.size and 0 <= col < self.size:
            self.hover_row = row
            self.hover_col = col
        else:
            self.hover_row = None
            self.hover_col = None

        self.update()

    # -------------------------------------------------
    # CLICK TO MOVE
    # -------------------------------------------------
    def mousePressEvent(self, event):
        pos = event.position()
        col = int(pos.x() // CELL)
        row = int(pos.y() // CELL)
        self.try_pawn_move(row, col)

    def try_pawn_move(self, row, col):
        current = self.game.current
        moves = self.game.legal_moves(current)

        if (row, col) in moves:
            self.game.move_pawn(current, row, col)
            self.update()
