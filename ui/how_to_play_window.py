from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame,QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import os


class HowToPlayWindow(QWidget):
    def __init__(self, stacked_widget):   
        super().__init__()
        self.stacked_widget = stacked_widget
        
        self.setWindowTitle("Quoridor Game - How To Play")
        self.setObjectName("HowToPlayPage")
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




        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        back = QPushButton("← Back to Menu")
        back.setObjectName("backButton")
        back.clicked.connect(self.go_back)

        layout.addWidget(back)
        
        # --- TITLE ---
        title = QLabel("How to Play Quoridor")
        title.setObjectName("howTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(30)

        # ---------------------------------------
        # Helper to create neon panels
        # ---------------------------------------
        def make_panel(title, body):
            frame = QFrame()
            frame.setObjectName("neonPanel")
            v = QVBoxLayout(frame)
            v.setContentsMargins(25, 25, 25, 25)
            v.setSpacing(10)

            t = QLabel(title)
            t.setObjectName("panelTitle")
            b = QLabel(body)
            b.setObjectName("panelText")
            b.setWordWrap(True)

            v.addWidget(t)
            v.addWidget(b)
            return frame

        # Panels
        content_layout.addWidget(
            make_panel(
                "Objective",
                "Be the first player to reach the opposite side of the board. "
                "Player 1 (blue) must reach the top row, while Player 2 (red) "
                "must reach the bottom row."
            )
        )

        content_layout.addWidget(
            make_panel(
                "Game Setup",
                "• The game is played on a 9×9 grid\n"
                "• Player 1 starts at the bottom center (row 8, column 4)\n"
                "• Player 2 starts at the top center (row 0, column 4)\n"
                "• Each player receives 10 walls at the start of the game"
            )
        )

        content_layout.addWidget(
            make_panel(
                "Player Movement",
                "• Players alternate turns\n"
                "• Move your pawn OR place a wall\n"
                "• Pawns move 1 square (up, down, left, right)\n"
                "• Cannot move through walls or pawns\n"
                "• If adjacent to opponent, you may jump over them"
            )
        )

        content_layout.addWidget(
            make_panel(
                "Wall Placement",
                "• Walls go between squares\n"
                "• Placed horizontally or vertically\n"
                "• Cannot overlap other walls\n"
                "• Cannot block all paths to goal\n"
                "• When you run out of walls, you must move"
            )
        )

        content_layout.addWidget(
            make_panel(
                "Winning the Game",
                "First player to reach any square on the opposite side wins."
            )
        )

        content_layout.addWidget(
            make_panel(
                "Strategy Tips",
                "• Balance between progressing and blocking\n"
                "• Save some walls for late game\n"
                "• Create long paths for your opponent\n"
                "• Look for jump opportunities\n"
                "• Always maintain a legal path"
            )
        )

        scroll.setWidget(content)

        layout.addWidget(title)
        layout.addWidget(scroll)


    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)
        
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