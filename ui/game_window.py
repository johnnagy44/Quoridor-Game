from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QRadioButton, QLineEdit, QGroupBox, QFormLayout, QButtonGroup
)
from PyQt6.QtCore import Qt
from .board_widget import BoardWidget
from game.game_state import GameState

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quoridor Game")
        self.game_state = GameState()
        self.board_widget = BoardWidget(self.game_state)

        self.init_ui()

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
                self.board_widget.update()
                self.update_status()
            else:
                self.status_label.setText("Invalid wall placement!")
        except ValueError:
            self.status_label.setText("Invalid input!")

    def undo_move(self):
        if self.game_state.undo():
            self.board_widget.update()
            self.update_status()
        else:
            self.status_label.setText("No moves to undo!")

    def reset_game(self):
        self.game_state = GameState()
        self.board_widget.game = self.game_state
        self.board_widget.update()
        self.update_status()

    def update_status(self):
        if self.game_state.winner is not None:
            self.status_label.setText(f"Player {self.game_state.winner + 1} wins!")
            return
        player = self.game_state.current + 1
        walls = self.game_state.players[self.game_state.current].walls
        self.status_label.setText(f"Player {player}'s turn - Walls: {walls}")
