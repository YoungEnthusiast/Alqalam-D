# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'studregform.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StudRegForm(object):
    def setupUi(self, StudRegForm):
        StudRegForm.setObjectName("StudRegForm")
        StudRegForm.resize(896, 716)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("add_user_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StudRegForm.setWindowIcon(icon)
        StudRegForm.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.groupBox = QtWidgets.QGroupBox(StudRegForm)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 871, 711))
        self.groupBox.setStyleSheet("QPushButton{\n"
"background-color: rgb(187, 217, 255);\n"
"}\n"
"\n"
"QComboBox{\n"
"background-color: rgb(187, 217, 255);\n"
"}")
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(270, 20, 175, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(450, 20, 411, 69))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.admission_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.admission_edit.setObjectName("admission_edit")
        self.verticalLayout_2.addWidget(self.admission_edit)
        self.name_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.name_edit.setObjectName("name_edit")
        self.verticalLayout_2.addWidget(self.name_edit)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.groupBox)
        self.calendarWidget.setGeometry(QtCore.QRect(450, 90, 411, 201))
        self.calendarWidget.setToolTipDuration(-2)
        self.calendarWidget.setSelectedDate(QtCore.QDate(2013, 1, 1))
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(290, 327, 151, 101))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(450, 330, 411, 341))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.class_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.class_comboBox.setEnabled(True)
        self.class_comboBox.setCurrentText("")
        self.class_comboBox.setObjectName("class_comboBox")
        self.verticalLayout_6.addWidget(self.class_comboBox)
        self.sex_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.sex_comboBox.setObjectName("sex_comboBox")
        self.sex_comboBox.addItem("")
        self.sex_comboBox.addItem("")
        self.verticalLayout_6.addWidget(self.sex_comboBox)
        self.browse_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.browse_btn.setToolTipDuration(-2)
        self.browse_btn.setObjectName("browse_btn")
        self.verticalLayout_6.addWidget(self.browse_btn)
        self.image_label = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.image_label.setMaximumSize(QtCore.QSize(389, 219))
        self.image_label.setText("")
        self.image_label.setScaledContents(True)
        self.image_label.setObjectName("image_label")
        self.verticalLayout_6.addWidget(self.image_label)
        self.address_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.address_lineEdit.setObjectName("address_lineEdit")
        self.verticalLayout_6.addWidget(self.address_lineEdit)
        self.parent_no_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.parent_no_lineEdit.setObjectName("parent_no_lineEdit")
        self.verticalLayout_6.addWidget(self.parent_no_lineEdit)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget_4)
        self.dateTimeEdit.setReadOnly(True)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.verticalLayout_6.addWidget(self.dateTimeEdit)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(-290, 20, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(530, 300, 261, 31))
        self.dateEdit.setToolTipDuration(-2)
        self.dateEdit.setReadOnly(True)
        self.dateEdit.setDate(QtCore.QDate(2000, 7, 1))
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(280, 570, 165, 101))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_7.addWidget(self.label_13)
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_7.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_7.addWidget(self.label_15)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(24, 25, 221, 671))
        self.label_7.setStyleSheet("QPushButton{\n"
"background-color: rgb(187, 217, 255);\n"
"}\n"
"\n"
"QComboBox{\n"
"background-color: rgb(187, 217, 255);\n"
"}")
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("studreg_pic.jpg"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.horizontalLayoutWidget = QtWidgets.QWidget(StudRegForm)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(550, 670, 231, 35))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.save_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.save_btn.setStyleSheet("background-color: rgb(147, 255, 196);")
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout_2.addWidget(self.save_btn)
        self.clear_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clear_btn.setStyleSheet("background-color: rgb(255, 89, 97);")
        self.clear_btn.setObjectName("clear_btn")
        self.horizontalLayout_2.addWidget(self.clear_btn)

        self.retranslateUi(StudRegForm)
        QtCore.QMetaObject.connectSlotsByName(StudRegForm)
        StudRegForm.setTabOrder(self.admission_edit, self.name_edit)
        StudRegForm.setTabOrder(self.name_edit, self.calendarWidget)
        StudRegForm.setTabOrder(self.calendarWidget, self.class_comboBox)
        StudRegForm.setTabOrder(self.class_comboBox, self.sex_comboBox)
        StudRegForm.setTabOrder(self.sex_comboBox, self.browse_btn)
        StudRegForm.setTabOrder(self.browse_btn, self.address_lineEdit)
        StudRegForm.setTabOrder(self.address_lineEdit, self.parent_no_lineEdit)
        StudRegForm.setTabOrder(self.parent_no_lineEdit, self.dateTimeEdit)
        StudRegForm.setTabOrder(self.dateTimeEdit, self.save_btn)
        StudRegForm.setTabOrder(self.save_btn, self.clear_btn)
        StudRegForm.setTabOrder(self.clear_btn, self.dateEdit)
        StudRegForm.setTabOrder(self.dateEdit, self.pushButton_2)

    def retranslateUi(self, StudRegForm):
        _translate = QtCore.QCoreApplication.translate
        StudRegForm.setWindowTitle(_translate("StudRegForm", "Registration"))
        self.groupBox.setTitle(_translate("StudRegForm", "Fill in registration details"))
        self.label_5.setText(_translate("StudRegForm", "Admission Number:"))
        self.label_4.setText(_translate("StudRegForm", "Name:"))
        self.label_3.setText(_translate("StudRegForm", "Date of Birth:"))
        self.calendarWidget.setToolTip(_translate("StudRegForm", "Use the green arrows to select months and year, then click on day"))
        self.label.setText(_translate("StudRegForm", "Class:"))
        self.label_2.setText(_translate("StudRegForm", "Sex:"))
        self.label_6.setText(_translate("StudRegForm", "Photograph:"))
        self.sex_comboBox.setItemText(0, _translate("StudRegForm", "Male"))
        self.sex_comboBox.setItemText(1, _translate("StudRegForm", "Female"))
        self.browse_btn.setToolTip(_translate("StudRegForm", "Click to open pictures location in computer"))
        self.browse_btn.setText(_translate("StudRegForm", "Browse..."))
        self.dateTimeEdit.setToolTip(_translate("StudRegForm", "It will automatically correct to the date of saving"))
        self.dateTimeEdit.setDisplayFormat(_translate("StudRegForm", "dddd, MMMM d,  yyyy hh:mm AP"))
        self.pushButton_2.setText(_translate("StudRegForm", "PushButton"))
        self.dateEdit.setToolTip(_translate("StudRegForm", "You can only select date from calendar above"))
        self.dateEdit.setDisplayFormat(_translate("StudRegForm", "MMMM d,  yyyy"))
        self.label_13.setText(_translate("StudRegForm", "Address:"))
        self.label_14.setText(_translate("StudRegForm", "Parent Number:"))
        self.label_15.setText(_translate("StudRegForm", "Registration Date:"))
        self.save_btn.setText(_translate("StudRegForm", "Save"))
        self.clear_btn.setText(_translate("StudRegForm", "Clear All"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StudRegForm = QtWidgets.QWidget()
    ui = Ui_StudRegForm()
    ui.setupUi(StudRegForm)
    StudRegForm.show()
    sys.exit(app.exec_())