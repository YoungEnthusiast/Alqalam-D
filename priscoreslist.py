# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'priscoreslist.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PriScoreForm(object):
    def setupUi(self, PriScoreForm):
        PriScoreForm.setObjectName("PriScoreForm")
        PriScoreForm.resize(1074, 721)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("score2_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PriScoreForm.setWindowIcon(icon)
        PriScoreForm.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"\n"
"QPushButton{\n"
"background-color: rgb(170, 255, 127);\n"
"}")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(PriScoreForm)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.switch_back_btn = QtWidgets.QPushButton(PriScoreForm)
        self.switch_back_btn.setStyleSheet("background-color: rgb(84, 210, 255);")
        self.switch_back_btn.setObjectName("switch_back_btn")
        self.verticalLayout_3.addWidget(self.switch_back_btn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(PriScoreForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(45)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(24, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(25, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(26, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(27, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(28, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(29, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(30, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(31, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(32, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(33, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(34, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(35, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(36, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(37, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(38, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(39, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(40, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(41, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(42, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(43, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(44, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.tableWidget_2 = QtWidgets.QTableWidget(PriScoreForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy)
        self.tableWidget_2.setAutoFillBackground(False)
        self.tableWidget_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(45)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(24, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(25, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(26, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(27, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(28, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(29, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(30, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(31, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(32, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(33, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(34, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(35, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(36, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(37, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(38, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(39, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(40, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(41, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(42, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(43, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(44, item)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_2.verticalHeader().setVisible(True)
        self.horizontalLayout.addWidget(self.tableWidget_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.del_btn = QtWidgets.QPushButton(PriScoreForm)
        self.del_btn.setStyleSheet("background-color: rgb(255, 37, 51);")
        self.del_btn.setObjectName("del_btn")
        self.verticalLayout_3.addWidget(self.del_btn)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.class_comboBox = QtWidgets.QComboBox(PriScoreForm)
        self.class_comboBox.setStyleSheet("background-color: rgb(84, 210, 255);")
        self.class_comboBox.setObjectName("class_comboBox")
        self.verticalLayout.addWidget(self.class_comboBox)
        self.stud_adm_no_comboBox = QtWidgets.QComboBox(PriScoreForm)
        self.stud_adm_no_comboBox.setStyleSheet("background-color: rgb(84, 210, 255);")
        self.stud_adm_no_comboBox.setObjectName("stud_adm_no_comboBox")
        self.verticalLayout.addWidget(self.stud_adm_no_comboBox)
        self.name_label = QtWidgets.QLabel(PriScoreForm)
        self.name_label.setText("")
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.groupBox = QtWidgets.QGroupBox(PriScoreForm)
        self.groupBox.setObjectName("groupBox")
        self.att_a_radio = QtWidgets.QRadioButton(self.groupBox)
        self.att_a_radio.setGeometry(QtCore.QRect(10, 30, 224, 28))
        self.att_a_radio.setObjectName("att_a_radio")
        self.att_e_radio = QtWidgets.QRadioButton(self.groupBox)
        self.att_e_radio.setGeometry(QtCore.QRect(10, 110, 38, 28))
        self.att_e_radio.setObjectName("att_e_radio")
        self.att_d_radio = QtWidgets.QRadioButton(self.groupBox)
        self.att_d_radio.setGeometry(QtCore.QRect(10, 90, 50, 28))
        self.att_d_radio.setObjectName("att_d_radio")
        self.att_c_radio = QtWidgets.QRadioButton(self.groupBox)
        self.att_c_radio.setGeometry(QtCore.QRect(10, 70, 70, 28))
        self.att_c_radio.setObjectName("att_c_radio")
        self.att_b_radio = QtWidgets.QRadioButton(self.groupBox)
        self.att_b_radio.setGeometry(QtCore.QRect(10, 50, 108, 28))
        self.att_b_radio.setObjectName("att_b_radio")
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(PriScoreForm)
        self.groupBox_2.setObjectName("groupBox_2")
        self.con_a_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.con_a_radio.setGeometry(QtCore.QRect(11, 30, 39, 28))
        self.con_a_radio.setObjectName("con_a_radio")
        self.con_b_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.con_b_radio.setGeometry(QtCore.QRect(11, 50, 39, 28))
        self.con_b_radio.setObjectName("con_b_radio")
        self.con_c_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.con_c_radio.setGeometry(QtCore.QRect(11, 70, 39, 28))
        self.con_c_radio.setObjectName("con_c_radio")
        self.con_d_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.con_d_radio.setGeometry(QtCore.QRect(11, 90, 41, 28))
        self.con_d_radio.setObjectName("con_d_radio")
        self.con_e_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.con_e_radio.setGeometry(QtCore.QRect(11, 110, 38, 28))
        self.con_e_radio.setObjectName("con_e_radio")
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(PriScoreForm)
        self.groupBox_3.setObjectName("groupBox_3")
        self.neat_a_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.neat_a_radio.setGeometry(QtCore.QRect(10, 30, 39, 28))
        self.neat_a_radio.setObjectName("neat_a_radio")
        self.neat_b_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.neat_b_radio.setGeometry(QtCore.QRect(10, 50, 39, 28))
        self.neat_b_radio.setObjectName("neat_b_radio")
        self.neat_c_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.neat_c_radio.setGeometry(QtCore.QRect(10, 70, 39, 28))
        self.neat_c_radio.setObjectName("neat_c_radio")
        self.neat_d_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.neat_d_radio.setGeometry(QtCore.QRect(10, 90, 41, 28))
        self.neat_d_radio.setObjectName("neat_d_radio")
        self.neat_e_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.neat_e_radio.setGeometry(QtCore.QRect(10, 110, 38, 28))
        self.neat_e_radio.setObjectName("neat_e_radio")
        self.verticalLayout.addWidget(self.groupBox_3)
        self.report_gen_btn = QtWidgets.QPushButton(PriScoreForm)
        self.report_gen_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.report_gen_btn.setObjectName("report_gen_btn")
        self.verticalLayout.addWidget(self.report_gen_btn)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(PriScoreForm)
        QtCore.QMetaObject.connectSlotsByName(PriScoreForm)

    def retranslateUi(self, PriScoreForm):
        _translate = QtCore.QCoreApplication.translate
        PriScoreForm.setWindowTitle(_translate("PriScoreForm", "Primary Classes Scores (First Term)"))
        self.switch_back_btn.setText(_translate("PriScoreForm", "Switch back to all classes"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("PriScoreForm", "Row/No"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("PriScoreForm", "Admission No"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("PriScoreForm", "Class"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("PriScoreForm", "Quran(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("PriScoreForm", "Quran(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("PriScoreForm", "Quran(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("PriScoreForm", "Quran(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("PriScoreForm", "Quran(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("PriScoreForm", "Ibadat(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("PriScoreForm", "Ibadat(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("PriScoreForm", "Ibadat(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("PriScoreForm", "Ibadat(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("PriScoreForm", "Ibadat(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("PriScoreForm", "Arabic(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(14)
        item.setText(_translate("PriScoreForm", "Arabic(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(15)
        item.setText(_translate("PriScoreForm", "Arabic(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(16)
        item.setText(_translate("PriScoreForm", "Arabic(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(17)
        item.setText(_translate("PriScoreForm", "Arabic(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(18)
        item.setText(_translate("PriScoreForm", "English(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(19)
        item.setText(_translate("PriScoreForm", "English(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(20)
        item.setText(_translate("PriScoreForm", "English(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(21)
        item.setText(_translate("PriScoreForm", "English(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(22)
        item.setText(_translate("PriScoreForm", "English(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(23)
        item.setText(_translate("PriScoreForm", "Maths(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(24)
        item.setText(_translate("PriScoreForm", "Maths(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(25)
        item.setText(_translate("PriScoreForm", "Maths(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(26)
        item.setText(_translate("PriScoreForm", "Maths(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(27)
        item.setText(_translate("PriScoreForm", "Maths(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(28)
        item.setText(_translate("PriScoreForm", "Science(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(29)
        item.setText(_translate("PriScoreForm", "Science(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(30)
        item.setText(_translate("PriScoreForm", "Science(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(31)
        item.setText(_translate("PriScoreForm", "Science(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(32)
        item.setText(_translate("PriScoreForm", "Science(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(33)
        item.setText(_translate("PriScoreForm", "Social Norm(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(34)
        item.setText(_translate("PriScoreForm", "Social Norm(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(35)
        item.setText(_translate("PriScoreForm", "Social Norm(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(36)
        item.setText(_translate("PriScoreForm", "Social Norm(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(37)
        item.setText(_translate("PriScoreForm", "Social Norm(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(38)
        item.setText(_translate("PriScoreForm", "Handwriting(CA1)"))
        item = self.tableWidget.horizontalHeaderItem(39)
        item.setText(_translate("PriScoreForm", "Handwriting(CA2)"))
        item = self.tableWidget.horizontalHeaderItem(40)
        item.setText(_translate("PriScoreForm", "Handwriting(ASS)"))
        item = self.tableWidget.horizontalHeaderItem(41)
        item.setText(_translate("PriScoreForm", "Handwriting(EXAM)"))
        item = self.tableWidget.horizontalHeaderItem(42)
        item.setText(_translate("PriScoreForm", "Handwriting(TOTAL)"))
        item = self.tableWidget.horizontalHeaderItem(43)
        item.setText(_translate("PriScoreForm", "All Total"))
        item = self.tableWidget.horizontalHeaderItem(44)
        item.setText(_translate("PriScoreForm", "Average"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("PriScoreForm", "Row/No"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("PriScoreForm", "Admission No"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("PriScoreForm", "Class"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("PriScoreForm", "Quran(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("PriScoreForm", "Quran(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("PriScoreForm", "Quran(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText(_translate("PriScoreForm", "Quran(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(7)
        item.setText(_translate("PriScoreForm", "Quran(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(8)
        item.setText(_translate("PriScoreForm", "Ibadat(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(9)
        item.setText(_translate("PriScoreForm", "Ibadat(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(10)
        item.setText(_translate("PriScoreForm", "Ibadat(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(11)
        item.setText(_translate("PriScoreForm", "Ibadat(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(12)
        item.setText(_translate("PriScoreForm", "Ibadat(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(13)
        item.setText(_translate("PriScoreForm", "Arabic(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(14)
        item.setText(_translate("PriScoreForm", "Arabic(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(15)
        item.setText(_translate("PriScoreForm", "Arabic(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(16)
        item.setText(_translate("PriScoreForm", "Arabic(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(17)
        item.setText(_translate("PriScoreForm", "Arabic(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(18)
        item.setText(_translate("PriScoreForm", "English(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(19)
        item.setText(_translate("PriScoreForm", "English(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(20)
        item.setText(_translate("PriScoreForm", "English(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(21)
        item.setText(_translate("PriScoreForm", "English(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(22)
        item.setText(_translate("PriScoreForm", "English(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(23)
        item.setText(_translate("PriScoreForm", "Maths(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(24)
        item.setText(_translate("PriScoreForm", "Maths(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(25)
        item.setText(_translate("PriScoreForm", "Maths(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(26)
        item.setText(_translate("PriScoreForm", "Maths(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(27)
        item.setText(_translate("PriScoreForm", "Maths(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(28)
        item.setText(_translate("PriScoreForm", "Science(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(29)
        item.setText(_translate("PriScoreForm", "Science(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(30)
        item.setText(_translate("PriScoreForm", "Science(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(31)
        item.setText(_translate("PriScoreForm", "Science(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(32)
        item.setText(_translate("PriScoreForm", "Science(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(33)
        item.setText(_translate("PriScoreForm", "Social Norm(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(34)
        item.setText(_translate("PriScoreForm", "Social Norm(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(35)
        item.setText(_translate("PriScoreForm", "Social Norm(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(36)
        item.setText(_translate("PriScoreForm", "Social Norm(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(37)
        item.setText(_translate("PriScoreForm", "Social Norm(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(38)
        item.setText(_translate("PriScoreForm", "Handwriting(CA1)"))
        item = self.tableWidget_2.horizontalHeaderItem(39)
        item.setText(_translate("PriScoreForm", "Handwriting(CA2)"))
        item = self.tableWidget_2.horizontalHeaderItem(40)
        item.setText(_translate("PriScoreForm", "Handwriting(ASS)"))
        item = self.tableWidget_2.horizontalHeaderItem(41)
        item.setText(_translate("PriScoreForm", "Handwriting(EXAM)"))
        item = self.tableWidget_2.horizontalHeaderItem(42)
        item.setText(_translate("PriScoreForm", "Handwriting(TOTAL)"))
        item = self.tableWidget_2.horizontalHeaderItem(43)
        item.setText(_translate("PriScoreForm", "All Total"))
        item = self.tableWidget_2.horizontalHeaderItem(44)
        item.setText(_translate("PriScoreForm", "Average"))
        self.del_btn.setText(_translate("PriScoreForm", "Delete Student"))
        self.groupBox.setTitle(_translate("PriScoreForm", "Attendance"))
        self.att_a_radio.setText(_translate("PriScoreForm", "A"))
        self.att_e_radio.setText(_translate("PriScoreForm", "E"))
        self.att_d_radio.setText(_translate("PriScoreForm", "D"))
        self.att_c_radio.setText(_translate("PriScoreForm", "C"))
        self.att_b_radio.setText(_translate("PriScoreForm", "B"))
        self.groupBox_2.setTitle(_translate("PriScoreForm", "Conduct"))
        self.con_a_radio.setText(_translate("PriScoreForm", "A"))
        self.con_b_radio.setText(_translate("PriScoreForm", "B"))
        self.con_c_radio.setText(_translate("PriScoreForm", "C"))
        self.con_d_radio.setText(_translate("PriScoreForm", "D"))
        self.con_e_radio.setText(_translate("PriScoreForm", "E"))
        self.groupBox_3.setTitle(_translate("PriScoreForm", "Neatness"))
        self.neat_a_radio.setText(_translate("PriScoreForm", "A"))
        self.neat_b_radio.setText(_translate("PriScoreForm", "B"))
        self.neat_c_radio.setText(_translate("PriScoreForm", "C"))
        self.neat_d_radio.setText(_translate("PriScoreForm", "D"))
        self.neat_e_radio.setText(_translate("PriScoreForm", "E"))
        self.report_gen_btn.setText(_translate("PriScoreForm", "Generate selected student report"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PriScoreForm = QtWidgets.QWidget()
    ui = Ui_PriScoreForm()
    ui.setupUi(PriScoreForm)
    PriScoreForm.show()
    sys.exit(app.exec_())
