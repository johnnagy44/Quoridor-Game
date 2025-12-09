from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QStackedWidget
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import os


class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setObjectName("MainMenu")
        self.setWindowTitle("Quoridor Game - Main Menu")
        #self.setFixedSize(900, 700)
        img = os.path.join(os.path.dirname(__file__), "assets", "background.jpg")
        #print(os.path.exists(img), img)


        pix = QPixmap(img).scaled(
        self.size(),
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pix))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        
        self.build_ui()


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

    def build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(25)
        layout.setContentsMargins(100, 40, 100, 40)

        # --- Title ---
        title = QLabel("QUORIDOR")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Poppins ExtraBold", 48))

        subtitle = QLabel("Strategic Board Game")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Poppins Medium", 18))


        layout.addWidget(title)
        layout.addWidget(subtitle)

        # --- Buttons ---
        btn_new = self.make_button("New Game", "play.png", "btnNewGame")
        btn_how = self.make_button("How to Play", "book.png", "btnHowToPlay")
        btn_set = self.make_button("Settings", "settings.png", "btnSettings")
        btn_exit = self.make_button("Exit", "exit.png", "btnExit")

        #buttons functionallity
        btn_how.clicked.connect(self.open_how_to_play)
        
        
        layout.addSpacing(30)
        layout.addWidget(btn_new)
        layout.addWidget(btn_how)
        layout.addWidget(btn_set)
        layout.addWidget(btn_exit)

        # --- Version ---
        version = QLabel("Version 1.0.0")
        version.setObjectName("versionLabel")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(30)
        layout.addWidget(version)

        self.setLayout(layout)

    def make_button(self, text, icon_filename, obj_name):
        btn = QPushButton(f"   {text}")
        btn.setObjectName(obj_name)
        btn.setMinimumHeight(70)
        btn.setIconSize(QSize(32, 32))
        btn.setStyleSheet("")
        btn.setFont(QFont("Poppins Semibold", 18))




        icon_path = os.path.join(os.path.dirname(__file__), "assets", icon_filename)
        if os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(btn.iconSize())

        return btn
    
    def open_how_to_play(self):
        self.stacked_widget.setCurrentIndex(1)   # Switch to HowToPlay page
