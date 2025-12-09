import sys
from PyQt6.QtWidgets import QApplication,QStackedWidget
from ui.main_menu import MainMenu
from ui.main_window import MainWindow

from PyQt6.QtGui import QFontDatabase

def load_fonts():
    QFontDatabase.addApplicationFont("ui/assets/fonts/Poppins-ExtraBold.ttf")
    QFontDatabase.addApplicationFont("ui/assets/fonts/Poppins-SemiBold.ttf")
    QFontDatabase.addApplicationFont("ui/assets/fonts/Poppins-Medium.ttf")


def load_styles(app):
    with open("ui/quoridor_neon.qss", "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_fonts()
    load_styles(app)

    #menu = MainMenu()
    menu=MainWindow()
    menu.show()

    sys.exit(app.exec())
