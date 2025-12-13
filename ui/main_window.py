from PyQt6.QtWidgets import QWidget, QVBoxLayout,QStackedWidget

from PyQt6.QtGui import QIcon
from .game_window import GameWindow
from .settings_window import SettingsWindow
from .main_menu import MainMenu
from .how_to_play_window import HowToPlayWindow
from .settings_window import SettingsWindow
from .setup_window import SetupWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Quoridor Game")
        self.setWindowIcon(QIcon("ui/assets/icon.ico"))
        self.setMinimumSize(1200, 800)
        self.resize(1200, 800)
        self.setContentsMargins(0, 0, 0, 0)
         
        

        self.stack = QStackedWidget()

        self.main_menu = MainMenu(self.stack)
        self.how_to_play = HowToPlayWindow(self.stack)
        self.settings=SettingsWindow(self.stack)
        self.game_setup=SetupWindow(self.stack)
        self.game=GameWindow(self.stack)

        self.stack.addWidget(self.main_menu)      # index 0
        self.stack.addWidget(self.how_to_play)    # index 1
        self.stack.addWidget(self.settings)       # index 2
        self.stack.addWidget(self.game_setup)     # index 3
        self.stack.addWidget(self.game)           # index 4

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)

        self.stack.setCurrentIndex(0)
