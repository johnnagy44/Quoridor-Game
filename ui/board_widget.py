from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt

CELL = 60   # pixel size
OFFSET = 10


class BoardWidget(QWidget):

    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.game = game_state
        self.size = game_state.board.size
        self.setMinimumSize(self.size * CELL, self.size * CELL)

    # -------------------------------------------------
    # PAINT EVENT
    # -------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grid(painter)
        self.draw_walls(painter)
        self.draw_players(painter)

    # -------------------------------------------------
    # GRID
    # -------------------------------------------------
    def draw_grid(self, p: QPainter):
        p.setPen(QPen(Qt.GlobalColor.black, 2))

        for r in range(self.size):
            for c in range(self.size):
                x = c * CELL
                y = r * CELL
                p.drawRect(x, y, CELL, CELL)

    # -------------------------------------------------
    # PLAYERS
    # -------------------------------------------------
    def draw_players(self, p: QPainter):
        p.setBrush(QBrush(QColor(255, 0, 0)))
        p1 = self.game.players[0]
        p.drawEllipse(
            p1.c * CELL + OFFSET,
            p1.r * CELL + OFFSET,
            CELL - 2*OFFSET,
            CELL - 2*OFFSET
        )

        p.setBrush(QBrush(QColor(0, 0, 255)))
        p2 = self.game.players[1]
        p.drawEllipse(
            p2.c * CELL + OFFSET,
            p2.r * CELL + OFFSET,
            CELL - 2*OFFSET,
            CELL - 2*OFFSET
        )

    # -------------------------------------------------
    # WALLS
    # -------------------------------------------------
    def draw_walls(self, p: QPainter):
        # brown
        p.setBrush(QBrush(QColor(120, 70, 15)))
        p.setPen(Qt.GlobalColor.black)

        # draw horizontal walls
        for r in range(self.size - 1):
            for c in range(self.size - 1):
                if self.game.board.h_walls[r][c]:
                    x = c * CELL
                    y = (r+1) * CELL - 5
                    p.drawRect(x, y, CELL*2, 10)

        # draw vertical walls
        for r in range(self.size - 1):
            for c in range(self.size - 1):
                if self.game.board.v_walls[r][c]:
                    x = (c+1) * CELL - 5
                    y = r * CELL
                    p.drawRect(x, y, 10, CELL*2)

    # -------------------------------------------------
    # CLICK EVENT
    # -------------------------------------------------
    def mousePressEvent(self, event):
        # convert pixel to board coords
        pos = event.position()
        col = int(pos.x() // CELL)
        row = int(pos.y() // CELL)


        # handle board click = pawn move
        self.try_pawn_move(row, col)

    # -------------------------------------------------
    # PAWN MOVE HANDLER
    # -------------------------------------------------
    def try_pawn_move(self, row, col):
        current = self.game.current
        moves = self.game.legal_moves(current)

        if (row, col) in moves:
            self.game.move_pawn(current, row, col)
            self.update()
