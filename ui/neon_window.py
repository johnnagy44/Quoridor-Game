from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys


class NeonWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neon Game UI")
        self.setMinimumSize(700, 450)

        # Main frame with neon border
        self.frame = QFrame()
        self.frame.setObjectName("mainFrame")

        self.title = QLabel("NEON GAME UI")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.play_btn = QPushButton("Play")
        self.settings_btn = QPushButton("Settings")
        self.exit_btn = QPushButton("Exit")

        # Vertical layout
        layout = QVBoxLayout(self.frame)
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addWidget(self.play_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.exit_btn)
        layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.frame)

        # Neon animations
        self.add_glow_animation(self.play_btn)
        self.add_glow_animation(self.settings_btn)
        self.add_glow_animation(self.exit_btn)

    def add_glow_animation(self, button):
        # Smooth hover glow animation using QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setOffset(0)
        shadow.setColor(QColor("#00eaff"))
        button.setGraphicsEffect(shadow)

        animation = QPropertyAnimation(shadow, b'blurRadius')
        animation.setDuration(400)
        animation.setStartValue(0)
        animation.setEndValue(30)
        animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        def start_anim():
            animation.setDirection(QPropertyAnimation.Direction.Forward)
            animation.start()

        def stop_anim():
            animation.setDirection(QPropertyAnimation.Direction.Backward)
            animation.start()

        button.enterEvent = lambda event: start_anim()
        button.leaveEvent = lambda event: stop_anim()


def run():
    app = QApplication(sys.argv)

    # LOAD QSS
    with open("neon_theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = NeonWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
