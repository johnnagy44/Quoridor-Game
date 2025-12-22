from PyQt6.QtWidgets import QWidget,QMessageBox
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QTimer,pyqtSignal
import os
from utils import resource_path

OFFSET_RATIO = 0.16
WALL_THICK_RATIO = 0.16
WALL_PREVIEW_ALPHA = 100
WALL_GLOW_ALPHA = 120
FLASH_DURATION_MS = 600
HIT_MARGIN = 12

NEON_GRID = QColor(0, 234, 255)
NEON_P1 = QColor(0, 255, 255)
NEON_P2 = QColor(255, 0, 255)
NEON_WALL = QColor(255, 0, 150)
BOARD_BG = QColor(0, 0, 0, 0)
GRID_SHADOW = QColor(0, 120, 140, 180)


class BoardWidget(QWidget):
    moveMade = pyqtSignal()
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.setObjectName("BoardWidget_Neon")
        

        self.game = game_state
        self.size = getattr(game_state.board, "size", None) or getattr(game_state, "size", 9)
        self.setMinimumSize(400, 400)

        self.hover_row = None
        self.hover_col = None
        self.wall_preview = None
        self.invalid_flash = None
        self.setMouseTracking(True)

    @property
    def cell_size(self):
        return min(self.width(), self.height()) / self.size

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.draw_background(p)
        self.draw_grid(p)
        self.draw_hover(p)
        self.draw_walls(p)
        self.draw_wall_preview(p)
        self.draw_players(p)
        self.draw_invalid_flash(p)

    def draw_background(self, p: QPainter):
        p.fillRect(self.rect(), BOARD_BG)

    def draw_grid(self, p: QPainter):
        cs = self.cell_size
        for r in range(self.size):
            for c in range(self.size):
                x = c * cs
                y = r * cs

                p.setPen(QPen(GRID_SHADOW, 12))
                p.drawRect(int(x), int(y), int(cs), int(cs))

                p.setPen(QPen(NEON_GRID, 2))
                p.drawRect(int(x), int(y), int(cs), int(cs))

    def draw_hover(self, p: QPainter):
        if self.hover_row is None:
            return

        cs = self.cell_size
        x = self.hover_col * cs
        y = self.hover_row * cs

        glow = QColor(0, 255, 255, 80)
        p.setBrush(QBrush(glow))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(int(x), int(y), int(cs), int(cs))

    def draw_players(self, p: QPainter):
        p.setPen(Qt.PenStyle.NoPen)
        cs = self.cell_size
        offset = cs * OFFSET_RATIO

        # Player 1
        p1 = self.game.players[0]
        x = p1.c * cs + offset
        y = p1.r * cs + offset

        p.setBrush(QBrush(QColor(0, 255, 255, 120)))
        p.drawEllipse(int(x - 5), int(y - 5), int(cs - 2*offset + 10), int(cs - 2*offset + 10))

        p.setBrush(QBrush(NEON_P1))
        p.drawEllipse(int(x), int(y), int(cs - 2*offset), int(cs - 2*offset))

        # Player 2
        p2 = self.game.players[1]
        x = p2.c * cs + offset
        y = p2.r * cs + offset

        p.setBrush(QBrush(QColor(255, 0, 255, 120)))
        p.drawEllipse(int(x - 5), int(y - 5), int(cs - 2*offset + 10), int(cs - 2*offset + 10))

        p.setBrush(QBrush(NEON_P2))
        p.drawEllipse(int(x), int(y), int(cs - 2*offset), int(cs - 2*offset))

    def draw_walls(self, p: QPainter):
        p.setPen(Qt.PenStyle.NoPen)
        glow = QColor(255, 0, 150, WALL_GLOW_ALPHA)
        p.setBrush(glow)
        
        cs = self.cell_size
        wall_thick = cs * WALL_THICK_RATIO

        h_walls = self.game.board.h_walls
        for r in range(self.size - 1):
            for c in range(self.size - 1):
                if h_walls[r][c]:
                    x = c * cs
                    y = (r + 1) * cs - wall_thick / 2

                    p.drawRect(int(x - 3), int(y - 3), int(cs * 2 + 6), int(wall_thick + 6))
                    p.setBrush(QBrush(NEON_WALL))
                    p.drawRect(int(x), int(y), int(cs * 2), int(wall_thick))
                    p.setBrush(glow)

        v_walls = self.game.board.v_walls
        for r in range(self.size - 1):
            for c in range(self.size - 1):
                if v_walls[r][c]:
                    x = (c + 1) * cs - wall_thick / 2
                    y = r * cs

                    p.drawRect(int(x - 3), int(y - 3), int(wall_thick + 6), int(cs * 2 + 6))
                    p.setBrush(QBrush(NEON_WALL))
                    p.drawRect(int(x), int(y), int(wall_thick), int(cs * 2))
                    p.setBrush(glow)

    def draw_wall_preview(self, p: QPainter):
        if not self.wall_preview:
            return
        r, c, orient = self.wall_preview
        cs = self.cell_size
        wall_thick = cs * WALL_THICK_RATIO
        
        if orient == "h":
            x = c * cs
            y = (r + 1) * cs - wall_thick / 2
            preview = QColor(255, 0, 150, WALL_PREVIEW_ALPHA)
            p.setBrush(QBrush(preview))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRect(int(x), int(y), int(cs * 2), int(wall_thick))
        else:  # 'v'
            x = (c + 1) * cs - wall_thick / 2
            y = r * cs
            preview = QColor(255, 0, 150, WALL_PREVIEW_ALPHA)
            p.setBrush(QBrush(preview))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRect(int(x), int(y), int(wall_thick), int(cs * 2))

    def draw_invalid_flash(self, p: QPainter):
        if not self.invalid_flash:
            return
        r, c, orient = self.invalid_flash
        cs = self.cell_size
        wall_thick = cs * WALL_THICK_RATIO
        
        red = QColor(255, 60, 80, 200)
        p.setBrush(QBrush(red))
        p.setPen(Qt.PenStyle.NoPen)
        if orient == "h":
            x = c * cs
            y = (r + 1) * cs - wall_thick / 2
            p.drawRect(int(x - 2), int(y - 2), int(cs * 2 + 4), int(wall_thick + 4))
        else:
            x = (c + 1) * cs - wall_thick / 2
            y = r * cs
            p.drawRect(int(x - 2), int(y - 2), int(wall_thick + 4), int(cs * 2 + 4))

    def mouseMoveEvent(self, event):
        pos = event.position()
        cs = self.cell_size
        col = int(pos.x() // cs)
        row = int(pos.y() // cs)

        if 0 <= row < self.size and 0 <= col < self.size:
            self.hover_row = row
            self.hover_col = col
            self.wall_preview = self._detect_wall_near(pos.x(), pos.y())
        else:
            self.hover_row = None
            self.hover_col = None
            self.wall_preview = None

        self.update()

    def mousePressEvent(self, event):
        pos = event.position()
        cs = self.cell_size
        col = int(pos.x() // cs)
        row = int(pos.y() // cs)

        if event.button() == Qt.MouseButton.LeftButton:
            self.try_pawn_move(row, col)
        elif event.button() == Qt.MouseButton.RightButton:
            preview = self._detect_wall_near(pos.x(), pos.y())
            if preview:
                r, c, orient = preview
                self.try_place_wall(r, c, orient)

    def try_pawn_move(self, row, col):
        current = self.game.current
        legal = self.game.legal_moves(current)

        if (row, col) in legal:
            try:
                self.game.move_pawn(current, row, col)
                self.moveMade.emit()
            except Exception as e:
                print(f"Error calling move_pawn: {e}")
            self.update()

    # -------------------------------------------------
    # HELPERS: wall detection based on mouse position
    # returns (r,c,orient) or None
    # Horizontal wall index (r,c) corresponds to wall between rows r and r+1,
    # spanning columns c and c+1 (0 <= r < size-1, 0 <= c < size-1)
    # Vertical similar: wall between columns c and c+1 spanning rows r and r+1
    # -------------------------------------------------
    def _detect_wall_near(self, xpix: float, ypix: float):
        cs = self.cell_size
        # clamp inside board bounds
        if xpix < 0 or ypix < 0 or xpix > self.size * cs or ypix > self.size * cs:
            return None

        col = int(xpix // cs)
        row = int(ypix // cs)
        rx = xpix - col * cs
        ry = ypix - row * cs

        # check bottom horizontal band of this cell (between row and row+1)
        # horizontal wall is centered at y ~= CELL (bottom edge of cell)
        # It spans two cells horizontally: choose c such that wall occupies [c, c+1] columns.
        # Candidate c: col-1 or col depending where you clicked horizontally
        # Horizontal candidate indices (r_h, c_h): r_h = row, c_h = col (or col-1)
        best = None

        # 1) horizontal candidate where wall sits between row and row+1,
        # spanning columns col and col+1 (so c must be <= size-2)
        # the screen y of that band is y = (row+1)*CELL
        y_of_bot_edge = (row + 1) * cs
        dy = abs(ypix - y_of_bot_edge)
        if dy <= HIT_MARGIN:
            # choose c such that wall will cover col and col+1 if possible, else col-1 & col
            if col <= self.size - 2:
                c_candidate = col
            else:
                c_candidate = col - 1
            r_candidate = row
            if 0 <= r_candidate < self.size - 1 and 0 <= c_candidate < self.size - 1:
                best = (r_candidate, c_candidate, "h")
                return best  # horizontal wins if close enough

        # 2) vertical candidate where wall sits between col and col+1,
        # spanning rows row and row+1; screen x ~ (col+1)*CELL
        x_of_right_edge = (col + 1) * cs
        dx = abs(xpix - x_of_right_edge)
        if dx <= HIT_MARGIN:
            if row <= self.size - 2:
                r_candidate = row
            else:
                r_candidate = row - 1
            c_candidate = col
            if 0 <= r_candidate < self.size - 1 and 0 <= c_candidate < self.size - 1:
                best = (r_candidate, c_candidate, "v")
                return best

        return None

    def try_place_wall(self, r, c, orient):
        orient_upper = orient.upper()
        try:
            success = self.game.try_place_wall(self.game.current, orient_upper, r, c)
            if success:
                self.wall_preview = None
                self.moveMade.emit()
                self.update()
                return
        except Exception as e:
            print(f"Error calling try_place_wall: {e}")
        self._flash_invalid_wall(r, c, orient)

    def _flash_invalid_wall(self, r, c, orient):
        self.invalid_flash = (r, c, orient)
        self.update()
        QTimer.singleShot(FLASH_DURATION_MS, self._clear_invalid_flash)

    def _clear_invalid_flash(self):
        self.invalid_flash = None
        self.update()

    def after_move_logic(self):
        if self.game.get_winner() is not None:
            self.show_winner()

    def show_winner(self):
        winner_index = self.game.get_winner()
        if winner_index is None:
            return

        winner_name = self.game.players[winner_index].name

        msg = QMessageBox(self)
        msg.setObjectName("WinnerMsgBox")

        msg.setWindowTitle("Game Over")
        msg.setText(f"<div style='text-align:center; font-size:24px; font-weight:bold;'>"
                    f"🏆 {winner_name} wins! 🏆"
                    "</div>")
        
        msg.setIcon(QMessageBox.Icon.NoIcon) 
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        ok_button = msg.button(QMessageBox.StandardButton.Ok)
        ok_button.setObjectName("WinnerOkBtn")
        ok_button.setText("Continue")
        msg.setFixedSize(400, 300)
        msg.exec()
