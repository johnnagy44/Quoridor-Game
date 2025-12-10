from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QRadioButton, QLineEdit, QGroupBox, QFormLayout, QButtonGroup
)
from PyQt6.QtCore import Qt
from .neon_board import NeonQuoridorBoard
from game.game_state import GameState

class GameWindow(QWidget):
    def __init__(self,stacked_widget):
        super().__init__()
        self.stacked_widget=stacked_widget
        self.load_stylesheet()
        self.setWindowTitle("Quoridor Game")
        self.game_state = GameState()
        self.board_widget = NeonQuoridorBoard()

        self.init_ui()

    def load_stylesheet(self):
        try:
            with open("ui/quoridor_neon.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Failed to load stylesheet:", e)

    def sync_board(self):
        # Update player positions
        p1 = self.game_state.players[0].pos
        p2 = self.game_state.players[1].pos
        self.board_widget.p1_pos = p1
        self.board_widget.p2_pos = p2

        # Update walls
        self.board_widget.p1_walls = self.game_state.players[0].walls_pos
        self.board_widget.p2_walls = self.game_state.players[1].walls_pos

        # Highlight legal moves (optional)
        self.board_widget.highlight_moves = self.game_state.legal_moves()

        self.board_widget.update()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Status bar
        self.status_label = QLabel("Player 1's turn")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Board
        main_layout.addWidget(self.board_widget)
        

        # Controls
        controls_layout = QHBoxLayout()

        # Wall placement controls
        wall_group = QGroupBox("Place Wall")
        wall_layout = QVBoxLayout()

        # Orientation
        orient_layout = QHBoxLayout()
        orient_layout.addWidget(QLabel("Orientation:"))
        self.h_radio = QRadioButton("Horizontal")
        self.v_radio = QRadioButton("Vertical")
        self.h_radio.setChecked(True)
        orient_layout.addWidget(self.h_radio)
        orient_layout.addWidget(self.v_radio)
        wall_layout.addLayout(orient_layout)

        # Position
        pos_layout = QFormLayout()
        self.row_edit = QLineEdit("0")
        self.col_edit = QLineEdit("0")
        pos_layout.addRow("Row:", self.row_edit)
        pos_layout.addRow("Col:", self.col_edit)
        wall_layout.addLayout(pos_layout)

        # Place button
        self.place_btn = QPushButton("Place Wall")
        self.place_btn.clicked.connect(self.place_wall)
        wall_layout.addWidget(self.place_btn)

        wall_group.setLayout(wall_layout)
        controls_layout.addWidget(wall_group)

        # Game controls
        game_group = QGroupBox("Game Controls")
        game_layout = QVBoxLayout()

        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo_move)
        game_layout.addWidget(self.undo_btn)

        self.reset_btn = QPushButton("New Game")
        self.reset_btn.clicked.connect(self.reset_game)
        game_layout.addWidget(self.reset_btn)

        game_group.setLayout(game_layout)
        controls_layout.addWidget(game_group)

        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)
        self.update_status()

    def place_wall(self):
        try:
            wr = int(self.row_edit.text())
            wc = int(self.col_edit.text())
            orient = 'H' if self.h_radio.isChecked() else 'V'
            if self.game_state.try_place_wall(self.game_state.current, orient, wr, wc):
                self.sync_board()
                self.update_status()
            else:
                self.status_label.setText("Invalid wall placement!")
        except ValueError:
            self.status_label.setText("Invalid input!")

    def undo_move(self):
        if self.game_state.undo():
            self.sync_board()
            self.update_status()
        else:
            self.status_label.setText("No moves to undo!")

    def reset_game(self):
        self.game_state = GameState()
        self.board_widget.game = self.game_state
        self.sync_board()
        self.update_status()

    def update_status(self):
        if self.game_state.winner is not None:
            self.status_label.setText(f"Player {self.game_state.winner + 1} wins!")
            return
        player = self.game_state.current + 1
        walls = self.game_state.players[self.game_state.current].walls
        self.status_label.setText(f"Player {player}'s turn - Walls: {walls}")
