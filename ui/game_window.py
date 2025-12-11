from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton,QComboBox,
    QCheckBox, QSpinBox, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import os

from .board_widget import BoardWidget
from game.game_state import GameState
from ai.ai import MinimaxAI

class GameWindow(QWidget):
    def __init__(self,stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Quoridor - Game Board")
        self.resize(2500, 1950)
        
        
        img = os.path.join(os.path.dirname(__file__), "assets", "background.jpg")
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
        p1_card = self.build_player_card("Player 1", "Reach bottom row", "p1")
        p2_card = self.build_player_card("Player 2", "Reach top row", "p2")

        
        game_state=GameState(size=9)

        # Game board
        self.board = BoardWidget(game_state)
        self.board.moveMade.connect(self.update_turn_bar)
        

        layout.addWidget(p1_card)
        layout.addWidget(self.board, stretch=1)
        layout.addWidget(p2_card)

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

        return card


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
        current = self.board.game.current  # 0 or 1

        if current == 0:
            self.bottom_bar.setProperty("role", "p1")
            self.turn_label.setText("Current Turn: Player 1")
        else:
            self.bottom_bar.setProperty("role", "p2")
            self.turn_label.setText("Current Turn: Player 2")

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

        self.stacked_widget.removeWidget(self)
        self.deleteLater()

        new_window = GameWindow(self.stacked_widget)

        self.stacked_widget.insertWidget(index, new_window)
        # Note: reset_game logic might need to be adjusted to preserve AI settings if desired,
        # but for now we follow the existing pattern which resets to default.
        
        self.stacked_widget.setCurrentIndex(index)

    def start_game(self, ai_enabled: bool, difficulty: str):
        depth = 3
        if difficulty == "Easy":
            depth = 1
        elif difficulty == "Medium":
            depth = 2
        elif difficulty == "Hard":
            depth = 3
            
        self.ai = MinimaxAI(max_depth=depth) if ai_enabled else None
        
        # Create new game state
        self.game = GameState(size=9)
        if ai_enabled:
            self.game.players[1].is_ai = True
        self.game.add_observer(self.on_game_state_change)
        
        # Update board reference
        self.board.game = self.game
        
        # Force UI update
        self.board.update()
        self.update_turn_bar()
        
    def on_game_state_change(self):
        self.update_turn_bar()
        
        if self.game.winner is not None:
            # Handle game over if needed (maybe show message)
            pass
            
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
