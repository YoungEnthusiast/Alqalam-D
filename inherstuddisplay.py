import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
#from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QAction
#from PyQt5.QtCore import QDateTime, QBuffer, QIODevice
#from PyQt5.QtGui import QPixmap
from studdetailsdisplay import Ui_StudDetailsForm


class StudDisplay(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_StudDetailsForm()
        self.ui.setupUi(self)














if __name__ == "__main__":
    app = QApplication(sys.argv)
    stud_display = StudDisplay()
    stud_display.show()
    sys.exit(app.exec_())
