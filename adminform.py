# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adminform.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1105, 694)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("administartion icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"\n"
"")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(400, 0, 281, 20))
        self.label.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.groupBox_5 = QtWidgets.QGroupBox(Form)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 510, 1109, 181))
        self.groupBox_5.setStyleSheet("QPushButton{\n"
"background-color: rgb(189, 218, 255);\n"
"}")
        self.groupBox_5.setObjectName("groupBox_5")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_5)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 1071, 145))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mgmt_edit_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.mgmt_edit_btn.setObjectName("mgmt_edit_btn")
        self.verticalLayout.addWidget(self.mgmt_edit_btn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.session_label = QtWidgets.QLabel(self.layoutWidget)
        self.session_label.setObjectName("session_label")
        self.horizontalLayout.addWidget(self.session_label)
        self.session_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.session_lineEdit.setObjectName("session_lineEdit")
        self.horizontalLayout.addWidget(self.session_lineEdit)
        self.next_term_label = QtWidgets.QLabel(self.layoutWidget)
        self.next_term_label.setObjectName("next_term_label")
        self.horizontalLayout.addWidget(self.next_term_label)
        self.next_term_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.next_term_lineEdit.setText("")
        self.next_term_lineEdit.setObjectName("next_term_lineEdit")
        self.horizontalLayout.addWidget(self.next_term_lineEdit)
        self.fees_label = QtWidgets.QLabel(self.layoutWidget)
        self.fees_label.setObjectName("fees_label")
        self.horizontalLayout.addWidget(self.fees_label)
        self.fees_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.fees_lineEdit.setText("")
        self.fees_lineEdit.setObjectName("fees_lineEdit")
        self.horizontalLayout.addWidget(self.fees_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.mgmt_update_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.mgmt_update_btn.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.mgmt_update_btn.setObjectName("mgmt_update_btn")
        self.verticalLayout.addWidget(self.mgmt_update_btn)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 160, 651, 351))
        self.groupBox_2.setStyleSheet("QPushButton{\n"
"background-color: rgb(189, 218, 255);\n"
"}\n"
"\n"
"QComboBox{\n"
"background-color: rgb(189, 218, 255);\n"
"}")
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 631, 322))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.class_comboBox = QtWidgets.QComboBox(self.layoutWidget1)
        self.class_comboBox.setEditable(False)
        self.class_comboBox.setObjectName("class_comboBox")
        self.verticalLayout_6.addWidget(self.class_comboBox)
        self.class_delete_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.class_delete_btn.setObjectName("class_delete_btn")
        self.verticalLayout_6.addWidget(self.class_delete_btn)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.add_new_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.add_new_btn.setObjectName("add_new_btn")
        self.horizontalLayout_7.addWidget(self.add_new_btn)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.class_add_label = QtWidgets.QLabel(self.layoutWidget1)
        self.class_add_label.setObjectName("class_add_label")
        self.horizontalLayout_9.addWidget(self.class_add_label)
        self.class_add_lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.class_add_lineEdit.setObjectName("class_add_lineEdit")
        self.horizontalLayout_9.addWidget(self.class_add_lineEdit)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.form_master_add_label = QtWidgets.QLabel(self.layoutWidget1)
        self.form_master_add_label.setObjectName("form_master_add_label")
        self.horizontalLayout_8.addWidget(self.form_master_add_label)
        self.form_master_lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.form_master_lineEdit.setObjectName("form_master_lineEdit")
        self.horizontalLayout_8.addWidget(self.form_master_lineEdit)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.class_save_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.class_save_btn.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.class_save_btn.setObjectName("class_save_btn")
        self.verticalLayout_5.addWidget(self.class_save_btn)
        self.horizontalLayout_10.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.class_edit_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.class_edit_btn.setObjectName("class_edit_btn")
        self.horizontalLayout_11.addWidget(self.class_edit_btn)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.class_edit_label = QtWidgets.QLabel(self.layoutWidget1)
        self.class_edit_label.setObjectName("class_edit_label")
        self.horizontalLayout_5.addWidget(self.class_edit_label)
        self.class_edit_lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.class_edit_lineEdit.setObjectName("class_edit_lineEdit")
        self.horizontalLayout_5.addWidget(self.class_edit_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.form_master_edit_label = QtWidgets.QLabel(self.layoutWidget1)
        self.form_master_edit_label.setObjectName("form_master_edit_label")
        self.horizontalLayout_4.addWidget(self.form_master_edit_label)
        self.form_master_edit_lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.form_master_edit_lineEdit.setText("")
        self.form_master_edit_lineEdit.setObjectName("form_master_edit_lineEdit")
        self.horizontalLayout_4.addWidget(self.form_master_edit_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.class_update_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.class_update_btn.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.class_update_btn.setObjectName("class_update_btn")
        self.verticalLayout_3.addWidget(self.class_update_btn)
        self.horizontalLayout_11.addLayout(self.verticalLayout_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(690, 170, 401, 171))
        self.groupBox.setStyleSheet("QPushButton{\n"
"background-color: rgb(189, 218, 255);\n"
"}\n"
"\n"
"QComboBox{\n"
"background-color: rgb(189, 218, 255);\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(16, 40, 381, 76))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.class_comboBox2 = QtWidgets.QComboBox(self.layoutWidget2)
        self.class_comboBox2.setObjectName("class_comboBox2")
        self.horizontalLayout_3.addWidget(self.class_comboBox2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stud_name_comboBox = QtWidgets.QComboBox(self.layoutWidget2)
        self.stud_name_comboBox.setObjectName("stud_name_comboBox")
        self.verticalLayout_2.addWidget(self.stud_name_comboBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.stud_del_btn = QtWidgets.QPushButton(self.layoutWidget2)
        self.stud_del_btn.setObjectName("stud_del_btn")
        self.horizontalLayout_2.addWidget(self.stud_del_btn)
        self.stud_edit_btn = QtWidgets.QPushButton(self.layoutWidget2)
        self.stud_edit_btn.setObjectName("stud_edit_btn")
        self.horizontalLayout_2.addWidget(self.stud_edit_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(580, 20, 511, 151))
        self.groupBox_3.setStyleSheet("QPushButton{\n"
"background-color: rgb(189, 218, 255);\n"
"}\n"
"\n"
"QComboBox{\n"
"background-color: rgb(189, 218, 255);\n"
"}\n"
"")
        self.groupBox_3.setObjectName("groupBox_3")
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 30, 491, 115))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.user_comboBox = QtWidgets.QComboBox(self.layoutWidget3)
        self.user_comboBox.setObjectName("user_comboBox")
        self.verticalLayout_8.addWidget(self.user_comboBox)
        self.user_delete_btn = QtWidgets.QPushButton(self.layoutWidget3)
        self.user_delete_btn.setObjectName("user_delete_btn")
        self.verticalLayout_8.addWidget(self.user_delete_btn)
        self.horizontalLayout_12.addLayout(self.verticalLayout_8)
        self.user_add_btn = QtWidgets.QPushButton(self.layoutWidget3)
        self.user_add_btn.setObjectName("user_add_btn")
        self.horizontalLayout_12.addWidget(self.user_add_btn)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_12)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.username_label = QtWidgets.QLabel(self.layoutWidget3)
        self.username_label.setObjectName("username_label")
        self.horizontalLayout_14.addWidget(self.username_label)
        self.username_lineEdit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.username_lineEdit.setObjectName("username_lineEdit")
        self.horizontalLayout_14.addWidget(self.username_lineEdit)
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.password_label = QtWidgets.QLabel(self.layoutWidget3)
        self.password_label.setObjectName("password_label")
        self.horizontalLayout_13.addWidget(self.password_label)
        self.password_lineEdit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.horizontalLayout_13.addWidget(self.password_lineEdit)
        self.verticalLayout_9.addLayout(self.horizontalLayout_13)
        self.user_save_btn = QtWidgets.QPushButton(self.layoutWidget3)
        self.user_save_btn.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.user_save_btn.setObjectName("user_save_btn")
        self.verticalLayout_9.addWidget(self.user_save_btn)
        self.horizontalLayout_15.addLayout(self.verticalLayout_9)
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setGeometry(QtCore.QRect(30, 20, 541, 121))
        self.groupBox_4.setStyleSheet("QPushButton{\n"
"background-color: rgb(189, 218, 255);\n"
"}")
        self.groupBox_4.setObjectName("groupBox_4")
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBox_4)
        self.layoutWidget4.setGeometry(QtCore.QRect(4, 30, 521, 79))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.principal_edit_btn = QtWidgets.QPushButton(self.layoutWidget4)
        self.principal_edit_btn.setObjectName("principal_edit_btn")
        self.horizontalLayout_17.addWidget(self.principal_edit_btn)
        self.principal_edit_lineEdit = QtWidgets.QLineEdit(self.layoutWidget4)
        self.principal_edit_lineEdit.setText("")
        self.principal_edit_lineEdit.setObjectName("principal_edit_lineEdit")
        self.horizontalLayout_17.addWidget(self.principal_edit_lineEdit)
        self.principal_update_btn = QtWidgets.QPushButton(self.layoutWidget4)
        self.principal_update_btn.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.principal_update_btn.setObjectName("principal_update_btn")
        self.horizontalLayout_17.addWidget(self.principal_update_btn)
        self.verticalLayout_10.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.headmaster_edit_btn = QtWidgets.QPushButton(self.layoutWidget4)
        self.headmaster_edit_btn.setObjectName("headmaster_edit_btn")
        self.horizontalLayout_16.addWidget(self.headmaster_edit_btn)
        self.headmaster_edit_lineEdit = QtWidgets.QLineEdit(self.layoutWidget4)
        self.headmaster_edit_lineEdit.setText("")
        self.headmaster_edit_lineEdit.setObjectName("headmaster_edit_lineEdit")
        self.horizontalLayout_16.addWidget(self.headmaster_edit_lineEdit)
        self.headmaster_update_btn = QtWidgets.QPushButton(self.layoutWidget4)
        self.headmaster_update_btn.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.headmaster_update_btn.setObjectName("headmaster_update_btn")
        self.horizontalLayout_16.addWidget(self.headmaster_update_btn)
        self.verticalLayout_10.addLayout(self.horizontalLayout_16)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Administration Form"))
        self.label.setText(_translate("Form", "WELCOME TO THE ADMIN PANEL"))
        self.groupBox_5.setTitle(_translate("Form", "Term and Session Management"))
        self.mgmt_edit_btn.setText(_translate("Form", "Edit"))
        self.session_label.setText(_translate("Form", "Session:"))
        self.next_term_label.setText(_translate("Form", "Next Term Begins Date:"))
        self.fees_label.setText(_translate("Form", "Next Term Fees:"))
        self.mgmt_update_btn.setText(_translate("Form", "Update"))
        self.groupBox_2.setTitle(_translate("Form", "Classes and Masters Management"))
        self.class_delete_btn.setText(_translate("Form", "Delete"))
        self.add_new_btn.setText(_translate("Form", "Add New Class"))
        self.class_add_label.setText(_translate("Form", "Class:"))
        self.form_master_add_label.setText(_translate("Form", "Form Master:"))
        self.class_save_btn.setText(_translate("Form", "Save"))
        self.class_edit_btn.setText(_translate("Form", "Edit Class"))
        self.class_edit_label.setText(_translate("Form", "Class:"))
        self.form_master_edit_label.setText(_translate("Form", "Form Master:"))
        self.class_update_btn.setText(_translate("Form", "Update"))
        self.groupBox.setTitle(_translate("Form", "Students Management"))
        self.stud_del_btn.setText(_translate("Form", "Delete"))
        self.stud_edit_btn.setText(_translate("Form", "Edit"))
        self.groupBox_3.setTitle(_translate("Form", "Users Management"))
        self.user_delete_btn.setText(_translate("Form", "Delete"))
        self.user_add_btn.setText(_translate("Form", "Add New"))
        self.username_label.setText(_translate("Form", "Username:"))
        self.password_label.setText(_translate("Form", "Password:"))
        self.user_save_btn.setText(_translate("Form", "Save"))
        self.groupBox_4.setTitle(_translate("Form", "Principal and Headmaster Management"))
        self.principal_edit_btn.setText(_translate("Form", "Edit Principal"))
        self.principal_update_btn.setText(_translate("Form", "Update"))
        self.headmaster_edit_btn.setText(_translate("Form", "Edit Headmaster"))
        self.headmaster_update_btn.setText(_translate("Form", "Update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())