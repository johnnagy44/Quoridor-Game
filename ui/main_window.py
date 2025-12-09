from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout,QStackedWidget
from PyQt6.QtCore import Qt
from .game_window import GameWindow
from .settings_window import SettingsWindow
from .main_menu import MainMenu
from .how_to_play_window import HowToPlayWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Quoridor Game - Main Menu")
        self.setFixedSize(900, 700)
        self.setContentsMargins(0, 0, 0, 0)
        #self.setStyleSheet("QWidget { border: 0px; }") 
        

        self.stack = QStackedWidget()

        self.main_menu = MainMenu(self.stack)
        self.how_to_play = HowToPlayWindow(self.stack)

        self.stack.addWidget(self.main_menu)      # index 0
        self.stack.addWidget(self.how_to_play)    # index 1

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)

        self.stack.setCurrentIndex(0)
