import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import sqlite3
from InherAlqalamMain import InherAlqalam, InherAdminAuthentication, InherChangePwd
from AuthenticationForm import Ui_Form


class InherAuthentication(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.inher_alqalam = InherAlqalam()
        self.inher_admin = InherAdminAuthentication()

        self.ui.signin_btn.clicked.connect(self.userLogin)
        self.ui.change_btn.clicked.connect(self.signUp)
        self.ui.admin_btn.clicked.connect(self.showAdminAuth)

    def userLogin(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")

        cur = con.cursor()

        username = self.ui.user_lineEdit.text()
        password = self.ui.pwdlineEdit.text()

        cmd = "SELECT username, password FROM t_users WHERE username = ? AND password = ?"

        cur.execute(cmd, (username, password))

        row = cur.fetchone()

        if row == None:
            self.ui.response_label.setText("Incorrect username or password")
        else:
            self.ui.response_label.setText("")
            QMessageBox.information(self, "Authentication", "You are successfully logged in", QMessageBox.Ok)


            self.inher_alqalam.showMaximized()
            self.inher_alqalam.ui.welcome_label.setText(username + ", welcome to the")
            self.inher_alqalam.ui.welcome_label2.setText("Alqalam Students' Record Manager and Reports Generator Software")
            self.close()
        con.close()

    def signUp(self):
        self.ui.response_label.setText("Please contact Admin to make you a user")

    def showAdminAuth(self):
        self.inher_admin.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InherAuthentication()
    widget.showMaximized()
    sys.exit(app.exec_())
