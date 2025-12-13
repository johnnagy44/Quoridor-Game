from PyQt6.QtWidgets import QWidget,QMessageBox
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QTimer,pyqtSignal

# Removed fixed CELL size
OFFSET_RATIO = 0.16
WALL_THICK_RATIO = 0.16
WALL_PREVIEW_ALPHA = 100
WALL_GLOW_ALPHA = 120
FLASH_DURATION_MS = 600
HIT_MARGIN = 12  # pixels tolerance to click a wall band

NEON_GRID = QColor(0, 234, 255)   # cyan neon
NEON_P1 = QColor(0, 255, 255)     # cyan glow
NEON_P2 = QColor(255, 0, 255)     # magenta glow
NEON_WALL = QColor(255, 0, 150)   # pink wall
BOARD_BG = QColor(0, 0, 0, 0)     # transparent
GRID_SHADOW = QColor(0, 120, 140, 180)


class BoardWidget(QWidget):
    moveMade = pyqtSignal()
    """
    Playable board widget:
      - left click: pawn move
      - right click: place wall (auto-detect orientation)
      - hover: shows cell glow and wall preview
    It will attempt to call game methods using common names:
      - pawn movement: game.legal_moves(player), game.move_pawn(player, r, c)
      - wall placement: game.can_place_wall(r, c, orient) OR game.canPlaceWall(...)
                        game.place_wall(r, c, orient) OR game.placeWall(...)
      - path checking after placement: game.path_exists_after_wall(r,c,orient) OR game.would_block_path(...)
    If your game API uses different names adapt the small helper methods below.
    """
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.setObjectName("BoardWidget_Neon")
        

        self.game = game_state
        self.size = getattr(game_state.board, "size", None) or getattr(game_state, "size", 9)
        self.setMinimumSize(400, 400) # Set a reasonable minimum size

        # hover
        self.hover_row = None
        self.hover_col = None
        self.wall_preview = None  # tuple (r,c,orient) or None
        self.invalid_flash = None  # tuple (r,c,orient) being flashed red
        self.setMouseTracking(True)

    @property
    def cell_size(self):
        return min(self.width(), self.height()) / self.size

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
        self.draw_wall_preview(p)
        self.draw_players(p)
        self.draw_invalid_flash(p)

    # -------------------------------------------------
    # DARK BACKGROUND
    # -------------------------------------------------
    def draw_background(self, p: QPainter):
        p.fillRect(self.rect(), BOARD_BG)

    # -------------------------------------------------
    # NEON GRID
    # -------------------------------------------------
    def draw_grid(self, p: QPainter):
        cs = self.cell_size
        for r in range(self.size):
            for c in range(self.size):
                x = c * cs
                y = r * cs

                # shadow under grid cell
                p.setPen(QPen(GRID_SHADOW, 12))
                p.drawRect(int(x), int(y), int(cs), int(cs))

                # actual neon cell border
                p.setPen(QPen(NEON_GRID, 2))
                p.drawRect(int(x), int(y), int(cs), int(cs))

    # -------------------------------------------------
    # CELL HOVER GLOW
    # -------------------------------------------------
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

    # -------------------------------------------------
    # PLAYERS (NEON GLOWING)
    # -------------------------------------------------
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

    # -------------------------------------------------
    # NEON WALLS (PINK)
    # -------------------------------------------------
    def draw_walls(self, p: QPainter):
        p.setPen(Qt.PenStyle.NoPen)
        glow = QColor(255, 0, 150, WALL_GLOW_ALPHA)
        p.setBrush(glow)
        
        cs = self.cell_size
        wall_thick = cs * WALL_THICK_RATIO

        # draw horizontal walls from game.board.h_walls if present
        h_walls = getattr(self.game.board, "h_walls", None)
        if h_walls is not None:
            for r in range(self.size - 1):
                for c in range(self.size - 1):
                    if h_walls[r][c]:
                        x = c * cs
                        y = (r + 1) * cs - wall_thick / 2

                        # glow
                        p.drawRect(int(x - 3), int(y - 3), int(cs * 2 + 6), int(wall_thick + 6))

                        # main neon
                        p.setBrush(QBrush(NEON_WALL))
                        p.drawRect(int(x), int(y), int(cs * 2), int(wall_thick))

                        p.setBrush(glow)

        # vertical walls
        v_walls = getattr(self.game.board, "v_walls", None)
        if v_walls is not None:
            for r in range(self.size - 1):
                for c in range(self.size - 1):
                    if v_walls[r][c]:
                        x = (c + 1) * cs - wall_thick / 2
                        y = r * cs

                        p.drawRect(int(x - 3), int(y - 3), int(wall_thick + 6), int(cs * 2 + 6))

                        p.setBrush(QBrush(NEON_WALL))
                        p.drawRect(int(x), int(y), int(wall_thick), int(cs * 2))

                        p.setBrush(glow)

    # -------------------------------------------------
    # WALL PREVIEW (on hover)
    # -------------------------------------------------
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

    # -------------------------------------------------
    # INVALID FLASH (red) when trying to place an illegal wall
    # -------------------------------------------------
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

    # -------------------------------------------------
    # MOUSE MOVEMENT: keeps hover + wall preview
    # -------------------------------------------------
    def mouseMoveEvent(self, event):
        pos = event.position()
        cs = self.cell_size
        col = int(pos.x() // cs)
        row = int(pos.y() // cs)

        if 0 <= row < self.size and 0 <= col < self.size:
            self.hover_row = row
            self.hover_col = col
            # update wall preview candidate
            preview = self._detect_wall_near(pos.x(), pos.y())
            self.wall_preview = preview
        else:
            self.hover_row = None
            self.hover_col = None
            self.wall_preview = None

        self.update()

    # -------------------------------------------------
    # LEFT: pawn move
    # -------------------------------------------------
    def mousePressEvent(self, event):
        pos = event.position()
        cs = self.cell_size
        col = int(pos.x() // cs)
        row = int(pos.y() // cs)

        if event.button() == Qt.MouseButton.LeftButton:
            self.try_pawn_move(row, col)
        elif event.button() == Qt.MouseButton.RightButton:
            # attempt to place wall at currently previewed slot (if any)
            preview = self._detect_wall_near(pos.x(), pos.y())
            if preview:
                r, c, orient = preview
                self.try_place_wall(r, c, orient)

    # -------------------------------------------------
    # HELPERS: pawn move
    # -------------------------------------------------
    def try_pawn_move(self, row, col):
        current = getattr(self.game, "current", 0)
        # expect game.legal_moves(player) -> set/list of (r,c)
        legal = None
        try:
            legal = self.game.legal_moves(current)
        except Exception:
            # try alternate name
            f = getattr(self.game, "get_legal_moves", None)
            if f:
                legal = f(current)
        if legal is None:
            print("WARNING: could not obtain legal moves from game; move won't be performed.")
            return

        if (row, col) in legal:
            # call move function
            moved = False
            for name in ("move_pawn", "movePawn", "move_player", "move_player_pawn"):
                f = getattr(self.game, name, None)
                if callable(f):
                    try:
                        try:
                            f(current, row, col)
                        except TypeError:
                            f(row, col)
                        moved = True
                        self.moveMade.emit()
                        # self.after_move_logic() - Handled by GameWindow via on_game_state_change
                        break
                    except Exception as e:
                        print("Error calling", name, e)
            if not moved:
                print("WARNING: no move function found on game object. Tried move_pawn / movePawn etc.")
            self.update()
        else:
            pass

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
        # We'll attempt to compute closest horizontal wall slot
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

    # -------------------------------------------------
    # TRY PLACE WALL: calls your game's APIs if present.
    # We'll attempt a small list of common method names for can_place & place_wall.
    # If the game's API is missing, we print instructions so you can adapt quickly.
    # -------------------------------------------------
    # -------------------------------------------------
    # TRY PLACE WALL
    # -------------------------------------------------
    def try_place_wall(self, r, c, orient):
        # 1) Direct call to GameState API
        # GameState.try_place_wall(player_index, orientation, r, c) returns True/False
        # validation, wall decrement, and turn switching happen inside GameState.
        if hasattr(self.game, "try_place_wall") and hasattr(self.game, "current"):
            # Ensure orientation is uppercase 'H' or 'V' as expected by GameState
            orient_upper = orient.upper()
            try:
                success = self.game.try_place_wall(self.game.current, orient_upper, r, c)
                if success:
                    # Successful placement
                    self.wall_preview = None
                    self.moveMade.emit()
                    self.update()
                    return
            except Exception as e:
                print(f"Error calling try_place_wall: {e}")
        
        # If we reach here, placement failed or API missing
        self._flash_invalid_wall(r, c, orient)

    # -------------------------------------------------
    # Visual flash for invalid wall placement
    # -------------------------------------------------
    def _flash_invalid_wall(self, r, c, orient):
        self.invalid_flash = (r, c, orient)
        self.update()
        QTimer.singleShot(FLASH_DURATION_MS, self._clear_invalid_flash)

    def _clear_invalid_flash(self):
        self.invalid_flash = None
        self.update()

    def after_move_logic(self):
        # Check for winner
        if self.game.get_winner() is not None:
            self.show_winner()
            return

        # If next player is AI
        #if self.game.players[self.game.current].is_ai:
        #    do_ai_turn()


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

        # Disable window resizing
        msg.setFixedSize(400, 300)

        msg.exec()
