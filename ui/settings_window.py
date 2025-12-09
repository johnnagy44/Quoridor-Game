from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QCheckBox, QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Settings")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Board size
        board_group = QGroupBox("Board Settings")
        board_layout = QFormLayout()
        self.size_combo = QComboBox()
        self.size_combo.addItems(["9x9", "11x11", "13x13"])
        self.size_combo.setCurrentText("9x9")
        board_layout.addRow("Board Size:", self.size_combo)
        board_group.setLayout(board_layout)
        layout.addWidget(board_group)

        # AI settings
        ai_group = QGroupBox("AI Players")
        ai_layout = QVBoxLayout()
        self.ai_player1 = QCheckBox("Player 1 is AI")
        self.ai_player2 = QCheckBox("Player 2 is AI")
        ai_layout.addWidget(self.ai_player1)
        ai_layout.addWidget(self.ai_player2)
        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)

        # Buttons
        btn_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply Settings")
        self.apply_btn.clicked.connect(self.apply_settings)
        btn_layout.addWidget(self.apply_btn)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def apply_settings(self):
        # Get settings
        size_text = self.size_combo.currentText()
        size = int(size_text.split('x')[0])
        ai1 = self.ai_player1.isChecked()
        ai2 = self.ai_player2.isChecked()

        # Apply to main window's game if exists
        if self.main_window and hasattr(self.main_window, 'game_win') and self.main_window.game_win:
            self.main_window.game_win.game_state.players[0].is_ai = ai1
            self.main_window.game_win.game_state.players[1].is_ai = ai2
            # Note: Changing board size would require resetting the game
            # For now, just update AI settings

        self.close()
