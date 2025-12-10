from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton,QComboBox,
    QCheckBox, QSpinBox, QFrame, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import os


class SettingsWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.setWindowTitle("Settings")
        
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
        
    # ================================================================
    # BUILD UI
    # ================================================================
    def build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---- Scroll area ----
        scroll = QScrollArea()
        scroll.setObjectName("scrollArea")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        root.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # ---- Back button ----
        back_btn = QPushButton("← Back to Menu")
        back_btn.clicked.connect(self.handle_back)
        layout.addWidget(back_btn)

        # ---- Page title ----
        title = QLabel("Settings")
        title.setObjectName("howTitle")  # uses your Poppins ExtraBold style
        layout.addWidget(title)

        # ---- Sections ----
        layout.addWidget(self.audio_panel())
        layout.addWidget(self.game_defaults_panel())
        layout.addWidget(self.display_panel())

        # ---- Save button ----
        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("blue")  # uses your blue button theme
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addStretch()

    # ================================================================
    # NEON PANEL TEMPLATE
    # ================================================================
    def neon_panel(self, title_text):
        frame = QFrame()
        frame.setObjectName("neonPanel")
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(25, 25, 25, 25)
        frame.layout().setSpacing(15)

        title = QLabel(title_text)
        title.setObjectName("panelTitle")
        frame.layout().addWidget(title)

        return frame

    # ================================================================
    # PANELS
    # ================================================================
    def audio_panel(self):
        panel = self.neon_panel("Audio Settings")

        row = QHBoxLayout()
        lbl = QLabel("Sound Effects")
        lbl.setObjectName("panelText")

        self.sound_toggle = QPushButton("ON")
        self.sound_toggle.setCheckable(True)
        self.sound_toggle.setChecked(True)
        self.sound_toggle.clicked.connect(self.update_toggle_text)
        self.sound_toggle.setFixedWidth(120)
        self.sound_toggle.setObjectName("purple")

        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(self.sound_toggle)

        panel.layout().addLayout(row)
        return panel

    def update_toggle_text(self):
        self.sound_toggle.setText("ON" if self.sound_toggle.isChecked() else "OFF")

    def game_defaults_panel(self):
        panel = self.neon_panel("Default Game Settings")

        # Player 1
        label = QLabel("Default Player 1 Name")
        label.setObjectName("panelText")
        panel.layout().addWidget(label)

        self.p1 = QLineEdit()
        self.p1.setText("Player 1")
        self.p1.setObjectName("neonField")
        panel.layout().addWidget(self.p1)

        # Player 2
        label = QLabel("Default Player 2 Name")
        label.setObjectName("panelText")
        panel.layout().addWidget(label)

        self.p2 = QLineEdit()
        self.p2.setText("Player 2")
        self.p2.setObjectName("neonField")
        panel.layout().addWidget(self.p2)

        # Time limit
        label = QLabel("Default Time Limit (minutes)")
        label.setObjectName("panelText")
        panel.layout().addWidget(label)

        self.time_limit = QSpinBox()
        self.time_limit.setRange(0, 120)
        self.time_limit.setObjectName("neonSpin")
        panel.layout().addWidget(self.time_limit)

        # Grid Size
        label = QLabel("Grid Size")
        label.setObjectName("panelText")
        panel.layout().addWidget(label)

        self.grid_size = QComboBox()
        self.grid_size.setObjectName("gridSizeCombo")
        self.grid_size.addItems(["9×9", "11×11", "13×13"])

        # Set default selected value (optional)
        self.grid_size.setCurrentIndex(0)   # selects 9×9

        panel.layout().addWidget(self.grid_size)
        self.grid_size.activated.connect(self.grid_size_selected)

        return panel

    
    def grid_size_selected(self):
        text = self.grid_size.currentText()

        # Convert label to numeric value
        if text == "9×9":
            self.selected_grid = 9
        elif text == "11×11":
            self.selected_grid = 11
        elif text == "13×13":
            self.selected_grid = 13

        self.grid_size.hide()
        self.grid_size.show()

    def display_panel(self):
        panel = self.neon_panel("Display Settings")

        # checkboxes
        self.cb_hints = QCheckBox("Show move hints")
        self.cb_valid = QCheckBox("Show valid moves")
        self.cb_anim = QCheckBox("Animate moves")

        for cb in (self.cb_hints, self.cb_valid, self.cb_anim):
            cb.setObjectName("panelText")
            panel.layout().addWidget(cb)

        return panel

    # ================================================================
    # SAVE
    # ================================================================
    def save_settings(self):
        settings = {
            "sound": self.sound_toggle.isChecked(),
            "player1": self.p1.text(),
            "player2": self.p2.text(),
            "time_limit": self.time_limit.value(),
            "board_size": self.board_size.value(),
            "show_hints": self.cb_hints.isChecked(),
            "show_valid": self.cb_valid.isChecked(),
            "animate": self.cb_anim.isChecked(),
        }


    # ================================================================
    # BACK
    # ================================================================
    def handle_back(self):
        self.stacked_widget.setCurrentIndex(0)
