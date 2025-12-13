import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QCheckBox, QComboBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import os

GAME_WINDOW=4
MAIN_MENU=0
class SetupWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Setup New Game")

        # ===== Background =====
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

        # ================================
        # MAIN WRAPPER LAYOUT (non-scroll)
        # ================================
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # ---- Back button ----
        back_btn = QPushButton("← Back to Menu")
        back_btn.clicked.connect(self.handle_back)
        main_layout.addWidget(back_btn)

        # ---- Header ----
        title = QLabel("Setup New Game")
        title.setObjectName("setupTitle")
        main_layout.addWidget(title)

        # ================================
        # SCROLL AREA FOR FORM CONTENT
        # ================================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Container inside scroll area
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setSpacing(20)

        # ---------------------------------
        # Player Name Section
        # ---------------------------------
        row = QHBoxLayout()
        row.setSpacing(20)

        self.p1 = QLineEdit("Player 1")
        self.p1.setObjectName("setupField")

        self.p2 = QLineEdit("Player 2")
        self.p2.setObjectName("setupField")

        col1 = QVBoxLayout()
        lab1 = QLabel("Player 1 Name")
        lab1.setObjectName("setupFieldLabel")
        col1.addWidget(lab1)
        col1.addWidget(self.p1)

        col2 = QVBoxLayout()
        lab2 = QLabel("Player 2 Name")
        lab2.setObjectName("setupFieldLabel")
        col2.addWidget(lab2)
        col2.addWidget(self.p2)

        row.addLayout(col1)
        row.addLayout(col2)

        scroll_layout.addLayout(row)

        # ---- Player 2 AI Toggle (Under Player 2) ----
        ai_row = QHBoxLayout()
        ai_row.addSpacing(40)  # indent
        self.ai_toggle = QCheckBox("Player 2 is an AI")
        self.ai_toggle.setObjectName("aiToggle")
        self.ai_toggle.stateChanged.connect(self.toggle_ai_mode)
        ai_row.addWidget(self.ai_toggle)
        ai_row.addStretch()
        scroll_layout.addLayout(ai_row)

        # ---- Difficulty Selection ----
        difficulty_row = QHBoxLayout()

        self.difficulty_label = QLabel("AI Difficulty:")
        self.difficulty_label.setObjectName("setupFieldLabel")
        self.difficulty_label.hide()

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setObjectName("aiDifficulty")
        self.difficulty_combo.hide()

        difficulty_row.addWidget(self.difficulty_label)
        difficulty_row.addWidget(self.difficulty_combo)

        scroll_layout.addLayout(difficulty_row)

        self.difficulty_row = difficulty_row

        # ---- Time Limit ----
        t_label = QLabel("Time Limit (minutes, 0 for no limit)")
        t_label.setObjectName("setupFieldLabel")
        self.time_box = QLineEdit("0")
        self.time_box.setObjectName("setupField")

        scroll_layout.addWidget(t_label)
        scroll_layout.addWidget(self.time_box)

        # ---- Board Size ----
        bs_label = QLabel("setupField")
        bs_label.setObjectName("panelText")
        self.board_size_combo = QComboBox()
        self.board_size_combo.addItems(["9×9", "11×11", "13×13"])
        self.board_size_combo.setObjectName("gridSizeCombo")
        
        scroll_layout.addWidget(bs_label)
        scroll_layout.addWidget(self.board_size_combo)

        # ---- Rules Panel ----
        rules_frame = QFrame()
        rules_frame.setObjectName("rulesPanel")

        rules_layout = QVBoxLayout()
        rules_layout.setContentsMargins(20, 20, 20, 20)

        rules_title = QLabel("Game Rules Summary")
        rules_title.setObjectName("rulesTitle")

        rules_text = QLabel(
            "• Each player starts with 10 walls\n"
            "• First player to reach the opposite side wins\n"
            "• Walls cannot completely block a player's path\n"
            "• Players alternate between moving and placing walls"
        )
        rules_text.setWordWrap(True)
        rules_text.setObjectName("rulesText")

        rules_layout.addWidget(rules_title)
        rules_layout.addWidget(rules_text)

        rules_frame.setLayout(rules_layout)
        scroll_layout.addWidget(rules_frame)

        # Set scroll content
        scroll.setWidget(scroll_container)
        main_layout.addWidget(scroll)

        # ---- Start Game Button ----
        self.start_btn = QPushButton("Start Game")
        self.start_btn.setObjectName("startGameBtn")
        self.start_btn.clicked.connect(self.handle_start)
        main_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    # ==========================================================
    # Resize event to maintain background scaling
    # ==========================================================
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

    # ==========================================================
    # UI Logic
    # ==========================================================
    def showEvent(self, event):
        # Try to sync with SettingsWindow default
        try:
            settings_window = self.stacked_widget.widget(2)
            if hasattr(settings_window, 'board_size'):
                default_size = settings_window.selected_grid
                # map 9 -> 0, 11 -> 1, 13 -> 2
                index_map = {9: 0, 11: 1, 13: 2}
                if default_size in index_map:
                    self.board_size_combo.setCurrentIndex(index_map[default_size])
        except:
            pass
        super().showEvent(event)

    def handle_back(self):
        self.stacked_widget.setCurrentIndex(MAIN_MENU)
    
    def handle_start(self):
        ai_enabled = self.ai_toggle.isChecked()
        difficulty_str = self.difficulty_combo.currentText()
        
        game_window = self.stacked_widget.widget(GAME_WINDOW)
        
        # Get board size from combo box
        size_str = self.board_size_combo.currentText() # "9×9"
        try:
            board_size = int(size_str.split('×')[0])
        except:
            board_size = 9
        
        game_window.p1_name = self.p1.text()
        game_window.p2_name = self.p2.text()
        try:
            game_window.time_limit = int(self.time_box.text())
        except ValueError:
            game_window.time_limit = 0

        if hasattr(game_window, 'start_game'):
            game_window.start_game(ai_enabled, difficulty_str, board_size)
        
        self.stacked_widget.setCurrentIndex(GAME_WINDOW)

    def toggle_ai_mode(self):
        if self.ai_toggle.isChecked():
            self.p2.setText("AI")
            self.p2.setDisabled(True)

            self.difficulty_label.show()
            self.difficulty_combo.show()

        else:
            self.p2.setDisabled(False)
            self.p2.setText("Player 2")

            self.difficulty_label.hide()
            self.difficulty_combo.hide()
