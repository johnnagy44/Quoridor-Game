from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton,
     QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import os

from .board_widget import BoardWidget
from utils import resource_path
from game.game_state import GameState
from ai.ai import MinimaxAI

class GameWindow(QWidget):
    def __init__(self,stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Quoridor - Game Board")
        self.resize(1200, 900)
        
        self.p1_name = "Player 1"
        self.p2_name = "Player 2"
        self.time_limit = 0
        
        img = resource_path(os.path.join(os.path.dirname(__file__), "assets", "background.jpg"))
        pix = QPixmap(img).scaled(
        self.size(),
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pix))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        main_layout = QVBoxLayout(self)
        top_bar = self.build_top_bar()
        self.center_panel = self.build_center_panel()
        self.bottom_bar = self.build_bottom_bar()

        main_layout.addLayout(top_bar)
        main_layout.addLayout(self.center_panel)
        main_layout.addWidget(self.bottom_bar)

    # -------------------------
    # Top Bar
    # -------------------------
    def build_top_bar(self):
        layout = QHBoxLayout()

        menu_btn = QPushButton("Menu")
        reset_btn = QPushButton("Reset")
        
        menu_btn.clicked.connect(self.menu_handle)
        reset_btn.clicked.connect(self.reset_handle)
        
        layout.addWidget(menu_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(reset_btn, alignment=Qt.AlignmentFlag.AlignRight)

        return layout

    # -------------------------
    # Center Panels
    # -------------------------
    def build_center_panel(self):
        layout = QHBoxLayout()
        layout.setSpacing(50)

        # Player cards
        # Player cards
        # Player cards
        self.p1_card_frame, self.p1_name_label, self.p1_walls_label = self.build_player_card("Player 1", "Reach bottom row", "p1")
        self.p2_card_frame, self.p2_name_label, self.p2_walls_label = self.build_player_card("Player 2", "Reach top row", "p2")

        
        game_state=GameState(size=9)

        # Game board
        self.board = BoardWidget(game_state)
        self.board.moveMade.connect(self.update_turn_bar)
        
        layout.addWidget(self.p1_card_frame)
        layout.addWidget(self.board, stretch=1)
        layout.addWidget(self.p2_card_frame)
        
        return layout

    # -------------------------
    # Player Info Card
    # -------------------------
    def build_player_card(self, name, goal, style_name):
        card = QFrame()
        card.setObjectName(f"{style_name}Card")     # e.g. "Player1Card"
        card.setProperty("role", style_name)        # e.g. "p1" or "p2"

        layout = QVBoxLayout(card)

        title = QLabel(name)
        walls = QLabel("Walls remaining: 10")
        goal_label = QLabel(f"Goal: {goal}")

        # Shared class for styling text inside the card
        title.setObjectName("PlayerCardLabel")
        walls.setObjectName("PlayerCardLabel")
        goal_label.setObjectName("PlayerCardLabel")

        layout.addWidget(title)
        layout.addWidget(walls)
        layout.addWidget(goal_label)
        layout.addStretch()

        return card, title, walls


    # -------------------------
    # Bottom Bar
    # -------------------------
    def build_bottom_bar(self):
        bar = QFrame()
        bar.setObjectName("TurnBar")
        bar.setProperty("role", "p1")   # start at player 1

        layout = QHBoxLayout(bar)

        self.turn_label = QLabel("Current Turn: Player 1")
        self.turn_label.setObjectName("TurnLabel")
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        


        layout.addWidget(self.turn_label)

        return bar
    
    def update_turn_bar(self):
        if not hasattr(self, 'game') or not self.game:
            return
            
        current = self.game.current  # 0 or 1
        player = self.game.players[current]

        if current == 0:
            self.bottom_bar.setProperty("role", "p1")
            self.turn_label.setText(f"Current Turn: {player.name}")
        else:
            self.bottom_bar.setProperty("role", "p2")
            if getattr(player, 'is_ai', False):
                self.turn_label.setText(f"{player.name} is thinking...")
            else:
                self.turn_label.setText(f"Current Turn: {player.name}")

        # Force stylesheet refresh
        self.turn_label.style().unpolish(self.turn_label)
        self.turn_label.style().polish(self.turn_label)
        self.turn_label.update()

        self.bottom_bar.style().unpolish(self.bottom_bar)
        self.bottom_bar.style().polish(self.bottom_bar)
        self.bottom_bar.update()



    def resizeEvent(self, event):
        pix = QPixmap(os.path.join(os.path.dirname(__file__), "assets", "background.jpg")).scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pix))
        self.setPalette(palette)
        super().resizeEvent(event)
        
        
    def menu_handle(self):
        self.reset_game()
        self.stacked_widget.setCurrentIndex(0)
        
    def reset_handle(self):
        self.reset_game()
        
    def reset_game(self):
        index = self.stacked_widget.indexOf(self)

        # Preserve AI settings
        ai_enabled = self.ai is not None
        difficulty = "Hard"  # Default to Hard if AI is enabled
        if self.ai:
            if self.ai.max_depth == 1:
                difficulty = "Easy"
            elif self.ai.max_depth == 2:
                difficulty = "Medium"

        board_size = self.board.size

        self.stacked_widget.removeWidget(self)
        self.deleteLater()

        # Pass AI settings to the new GameWindow
        new_window = GameWindow(self.stacked_widget)
        new_window.start_game(ai_enabled=ai_enabled, difficulty=difficulty, board_size=board_size)

        self.stacked_widget.insertWidget(index, new_window)
        self.stacked_widget.setCurrentIndex(index)

    def start_game(self, ai_enabled: bool, difficulty: str, board_size: int = 9):
        depth = 3
        if difficulty == "Easy":
            depth = 1
        elif difficulty == "Medium":
            depth = 2
        elif difficulty == "Hard":
            depth = 3
            
        self.ai = MinimaxAI(max_depth=depth) if ai_enabled else None
        
        # Create new game state
        self.game = GameState(size=board_size)
        self.game.players[0].name = self.p1_name
        self.game.players[1].name = self.p2_name
        
        # Update player names based on AI state
        if ai_enabled:
            self.p2_name = "AI"
        else:
            self.p2_name = "Player 2"

        # Update UI labels
        self.p1_name_label.setText(self.p1_name)
        self.p2_name_label.setText(self.p2_name)

        if ai_enabled:
            self.game.players[1].is_ai = True
        self.game.add_observer(self.on_game_state_change)
        
        # Update board reference
        self.board.game = self.game
        self.board.size = board_size
        
        # Force UI update
        self.board.update()
        self.update_turn_bar()
        self.update_walls_labels()
        
    def on_game_state_change(self):
        self.update_turn_bar()
        self.update_walls_labels()
        
        if self.game.winner is not None:
            self.board.show_winner()
            
        # If AI is enabled and it is AI turn (player 1)
        if self.ai and self.game.current == 1 and self.game.winner is None:
            # Small delay to let UI refresh before AI thinks
            QTimer.singleShot(100, self.make_ai_move)

    def make_ai_move(self):
        if self.game.winner is not None or self.game.current != 1:
            return

        move = self.ai.choose_move(self.game, 1)
        if move:
            if move[0] == 'M':
                # ('M', r, c)
                self.game.move_pawn(1, move[1], move[2])
            elif move[0] == 'W':
                # ('W', orient, r, c)
                self.game.try_place_wall(1, move[1], move[2], move[3])
        
        self.board.update()

    def update_walls_labels(self):
        if hasattr(self, 'game') and self.game:
            w1 = self.game.players[0].walls
            w2 = self.game.players[1].walls
            self.p1_walls_label.setText(f"Walls remaining: {w1}")
            self.p2_walls_label.setText(f"Walls remaining: {w2}")
