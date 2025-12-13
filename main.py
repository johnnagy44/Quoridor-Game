import sys
from PyQt6.QtWidgets import QApplication,QStackedWidget
import ctypes
from PyQt6.QtGui import QIcon,QFontDatabase
from ui.main_window import MainWindow
from utils import resource_path



def load_fonts():
    QFontDatabase.addApplicationFont(resource_path("ui/assets/fonts/Poppins-ExtraBold.ttf"))
    QFontDatabase.addApplicationFont(resource_path("ui/assets/fonts/Poppins-SemiBold.ttf"))
    QFontDatabase.addApplicationFont(resource_path("ui/assets/fonts/Poppins-Medium.ttf"))


def load_styles(app):
    with open(resource_path("ui/assets/quoridor_neon.qss"), "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("quoridor.game")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("ui/assets/icon.ico")))
    load_fonts()
    load_styles(app)

    menu=MainWindow()
    menu.show()

    sys.exit(app.exec())
