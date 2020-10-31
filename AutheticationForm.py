 -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AuthenticationForm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(514, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("auth_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.user_lineEdit = QtWidgets.QLineEdit(Form)
        self.user_lineEdit.setObjectName("user_lineEdit")
        self.gridLayout.addWidget(self.user_lineEdit, 0, 4, 1, 2)
        self.signin_btn = QtWidgets.QPushButton(Form)
        self.signin_btn.setObjectName("signin_btn")
        self.gridLayout.addWidget(self.signin_btn, 2, 4, 1, 1)
        self.pwdlineEdit = QtWidgets.QLineEdit(Form)
        self.pwdlineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwdlineEdit.setObjectName("pwdlineEdit")
        self.gridLayout.addWidget(self.pwdlineEdit, 1, 4, 1, 2)
        self.change_btn = QtWidgets.QPushButton(Form)
        self.change_btn.setObjectName("change_btn")
        self.gridLayout.addWidget(self.change_btn, 2, 5, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.response_label = QtWidgets.QLabel(Form)
        self.response_label.setObjectName("response_label")
        self.verticalLayout.addWidget(self.response_label)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setStyleSheet("background-color: rgb(254, 254, 254);\n"
"border-color: rgb(254, 254, 254);")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "User Authentication"))
        self.signin_btn.setText(_translate("Form", "Sign In"))
        self.change_btn.setText(_translate("Form", "Sign Up"))
        self.label.setText(_translate("Form", "Username:"))
        self.label_2.setText(_translate("Form", "Password:"))
        self.pushButton.setText(_translate("Form", "Login as Admin"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
