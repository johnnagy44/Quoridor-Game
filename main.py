import sys
import os
import platform
if platform.system() == "Windows":
    import ctypes
    
from PyQt6.QtWidgets import QApplication,QStackedWidget
from PyQt6.QtGui import QIcon,QFontDatabase
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow
from utils import resource_path



def load_fonts():
    QFontDatabase.addApplicationFont(resource_path("ui/assets/fonts/Poppins-ExtraBold.ttf"))
    QFontDatabase.addApplicationFont(resource_path("ui/assets/fonts/Poppins-SemiBold.ttf"))
    QFontDatabase.addApplicationFont(resource_path("ui/assets/fonts/Poppins-Medium.ttf"))


def load_styles(app):
    with open(resource_path("ui/assets/quoridor_neon.qss"), "r") as f:
        qss = f.read()
    
    # Replace placeholders with actual resource paths for PyInstaller compatibility
    arrow_up_path = resource_path("ui/assets/arrow-light-up.png").replace("\\", "/")
    arrow_down_path = resource_path("ui/assets/arrow-light-down.png").replace("\\", "/")
    winner_bg_path = resource_path("ui/assets/pop_up_win3.png").replace("\\", "/")
    
    qss = qss.replace("PLACEHOLDER_ARROW_UP", arrow_up_path)
    qss = qss.replace("PLACEHOLDER_ARROW_DOWN", arrow_down_path)
    qss = qss.replace("PLACEHOLDER_WINNER_BG", winner_bg_path)
    
    app.setStyleSheet(qss)

if __name__ == "__main__":
    
    if platform.system() == "Windows":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("quoridor.game")
    
    app = QApplication(sys.argv)
    
    # dark theme
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    
    app.setWindowIcon(QIcon(resource_path("ui/assets/icon.ico")))
    load_fonts()
    load_styles(app)

    menu=MainWindow()
    menu.show()

    sys.exit(app.exec())
