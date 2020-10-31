import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
import sqlite3

from studeditform import Ui_Form

class StudEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()

        query = cur.execute('SELECT * FROM t_classes ORDER BY class_name')
        classes = []

        rows = cur.fetchall()
        for row in rows:
            classes.append(row[0])

        self.ui.class_comboBox.addItems(classes)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    stud_edit = StudEdit()
    stud_edit.show()
    sys.exit(app.exec_())
