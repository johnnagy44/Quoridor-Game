from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from .game_window import GameWindow
from .settings_window import SettingsWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")

        layout = QVBoxLayout()

        btn_game = QPushButton("Start Game")
        btn_game.clicked.connect(self.open_game)

        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(self.open_settings)

        layout.addWidget(btn_game)
        layout.addWidget(btn_settings)
        self.setLayout(layout)

        self.game_win = None
        self.settings_win = None

    def open_game(self):
        self.game_win = GameWindow()
        self.game_win.show()

    def open_settings(self):
        self.settings_win = SettingsWindow()
        self.settings_win.show()
