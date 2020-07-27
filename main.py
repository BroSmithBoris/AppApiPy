from PyQt5.QtWidgets import *
import sys
from Gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())