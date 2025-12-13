import sys
from PyQt6.QtWidgets import QApplication,QStackedWidget
import ctypes
from PyQt6.QtGui import QIcon,QFontDatabase
from ui.main_window import MainWindow



def load_fonts():
    QFontDatabase.addApplicationFont("ui/assets/fonts/Poppins-ExtraBold.ttf")
    QFontDatabase.addApplicationFont("ui/assets/fonts/Poppins-SemiBold.ttf")
    QFontDatabase.addApplicationFont("ui/assets/fonts/Poppins-Medium.ttf")


def load_styles(app):
    with open("ui/quoridor_neon.qss", "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("quoridor.game")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("ui/assets/icon.ico"))
    load_fonts()
    load_styles(app)

    menu=MainWindow()
    menu.show()

    sys.exit(app.exec())
