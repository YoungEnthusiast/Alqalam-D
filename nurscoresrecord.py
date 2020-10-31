# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nurscoresrecord.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NurScoreRecForm(object):
    def setupUi(self, NurScoreRecForm):
        NurScoreRecForm.setObjectName("NurScoreRecForm")
        NurScoreRecForm.resize(985, 704)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("score_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NurScoreRecForm.setWindowIcon(icon)
        NurScoreRecForm.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"\n"
"QPushButton{\n"
"background-color: rgb(170, 255, 127);\n"
"}\n"
"")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(NurScoreRecForm)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(NurScoreRecForm)
        self.groupBox.setStyleSheet("QComboBox{\n"
"background-color: rgb(165, 209, 255);\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.class_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.class_comboBox.setObjectName("class_comboBox")
        self.horizontalLayout.addWidget(self.class_comboBox)
        self.stud_adm_no_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.stud_adm_no_comboBox.setObjectName("stud_adm_no_comboBox")
        self.horizontalLayout.addWidget(self.stud_adm_no_comboBox)
        self.name_label = QtWidgets.QLabel(self.groupBox)
        self.name_label.setStyleSheet("QComboBox{\n"
"background-color: rgb(166, 180, 255);\n"
"}")
        self.name_label.setText("")
        self.name_label.setObjectName("name_label")
        self.horizontalLayout.addWidget(self.name_label)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.nur_sc_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.nur_sc_ass_spin.setDecimals(0)
        self.nur_sc_ass_spin.setObjectName("nur_sc_ass_spin")
        self.gridLayout.addWidget(self.nur_sc_ass_spin, 19, 3, 1, 1)
        self.label_28 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_28.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_28.setObjectName("label_28")
        self.gridLayout.addWidget(self.label_28, 27, 0, 1, 1)
        self.nur_sc_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.nur_sc_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.nur_sc_score_btn.setObjectName("nur_sc_score_btn")
        self.gridLayout.addWidget(self.nur_sc_score_btn, 19, 5, 1, 1)
        self.social_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.social_c2_spin.setDecimals(0)
        self.social_c2_spin.setObjectName("social_c2_spin")
        self.gridLayout.addWidget(self.social_c2_spin, 22, 2, 1, 1)
        self.social_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.social_c1_spin.setDecimals(0)
        self.social_c1_spin.setObjectName("social_c1_spin")
        self.gridLayout.addWidget(self.social_c1_spin, 22, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 19, 0, 1, 1)
        self.nur_sc_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.nur_sc_c1_spin.setDecimals(0)
        self.nur_sc_c1_spin.setObjectName("nur_sc_c1_spin")
        self.gridLayout.addWidget(self.nur_sc_c1_spin, 19, 1, 1, 1)
        self.nur_sc_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.nur_sc_c2_spin.setDecimals(0)
        self.nur_sc_c2_spin.setObjectName("nur_sc_c2_spin")
        self.gridLayout.addWidget(self.nur_sc_c2_spin, 19, 2, 1, 1)
        self.nur_sc_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.nur_sc_exam_spin.setDecimals(0)
        self.nur_sc_exam_spin.setObjectName("nur_sc_exam_spin")
        self.gridLayout.addWidget(self.nur_sc_exam_spin, 19, 4, 1, 1)
        self.handwriting_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.handwriting_ass_spin.setDecimals(0)
        self.handwriting_ass_spin.setObjectName("handwriting_ass_spin")
        self.gridLayout.addWidget(self.handwriting_ass_spin, 27, 3, 1, 1)
        self.label_16 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 22, 0, 1, 1)
        self.handwriting_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.handwriting_exam_spin.setDecimals(0)
        self.handwriting_exam_spin.setObjectName("handwriting_exam_spin")
        self.gridLayout.addWidget(self.handwriting_exam_spin, 27, 4, 1, 1)
        self.math_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.math_exam_spin.setDecimals(0)
        self.math_exam_spin.setObjectName("math_exam_spin")
        self.gridLayout.addWidget(self.math_exam_spin, 15, 4, 1, 1)
        self.math_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.math_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.math_score_btn.setObjectName("math_score_btn")
        self.gridLayout.addWidget(self.math_score_btn, 15, 5, 1, 1)
        self.social_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.social_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.social_score_btn.setObjectName("social_score_btn")
        self.gridLayout.addWidget(self.social_score_btn, 22, 5, 1, 1)
        self.handwriting_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.handwriting_c1_spin.setDecimals(0)
        self.handwriting_c1_spin.setObjectName("handwriting_c1_spin")
        self.gridLayout.addWidget(self.handwriting_c1_spin, 27, 1, 1, 1)
        self.handwriting_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.handwriting_c2_spin.setDecimals(0)
        self.handwriting_c2_spin.setObjectName("handwriting_c2_spin")
        self.gridLayout.addWidget(self.handwriting_c2_spin, 27, 2, 1, 1)
        self.handwriting_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.handwriting_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.handwriting_score_btn.setObjectName("handwriting_score_btn")
        self.gridLayout.addWidget(self.handwriting_score_btn, 27, 5, 1, 1)
        self.social_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.social_ass_spin.setDecimals(0)
        self.social_ass_spin.setObjectName("social_ass_spin")
        self.gridLayout.addWidget(self.social_ass_spin, 22, 3, 1, 1)
        self.tot_avg_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.tot_avg_btn.setStyleSheet("background-color: rgb(170, 255, 127);\n"
"")
        self.tot_avg_btn.setObjectName("tot_avg_btn")
        self.gridLayout.addWidget(self.tot_avg_btn, 30, 1, 1, 4)
        self.social_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.social_exam_spin.setDecimals(0)
        self.social_exam_spin.setObjectName("social_exam_spin")
        self.gridLayout.addWidget(self.social_exam_spin, 22, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 25, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 14, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 8, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 10, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 26, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 21, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 28, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem9, 11, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem10, 20, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem11, 18, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem12, 17, 1, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem13, 13, 1, 1, 1)
        self.qur_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.qur_c2_spin.setDecimals(0)
        self.qur_c2_spin.setObjectName("qur_c2_spin")
        self.gridLayout.addWidget(self.qur_c2_spin, 1, 2, 1, 1)
        self.ibadat_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.ibadat_exam_spin.setDecimals(0)
        self.ibadat_exam_spin.setObjectName("ibadat_exam_spin")
        self.gridLayout.addWidget(self.ibadat_exam_spin, 5, 4, 1, 1)
        self.arabic_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.arabic_c2_spin.setDecimals(0)
        self.arabic_c2_spin.setObjectName("arabic_c2_spin")
        self.gridLayout.addWidget(self.arabic_c2_spin, 9, 2, 1, 1)
        self.qur_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.qur_c1_spin.setDecimals(0)
        self.qur_c1_spin.setObjectName("qur_c1_spin")
        self.gridLayout.addWidget(self.qur_c1_spin, 1, 1, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem14, 29, 1, 1, 1)
        self.ibadat_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.ibadat_c2_spin.setDecimals(0)
        self.ibadat_c2_spin.setObjectName("ibadat_c2_spin")
        self.gridLayout.addWidget(self.ibadat_c2_spin, 5, 2, 1, 1)
        self.arabic_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.arabic_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.arabic_score_btn.setObjectName("arabic_score_btn")
        self.gridLayout.addWidget(self.arabic_score_btn, 9, 5, 1, 1)
        self.eng_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.eng_ass_spin.setDecimals(0)
        self.eng_ass_spin.setObjectName("eng_ass_spin")
        self.gridLayout.addWidget(self.eng_ass_spin, 12, 3, 1, 1)
        self.eng_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.eng_exam_spin.setDecimals(0)
        self.eng_exam_spin.setObjectName("eng_exam_spin")
        self.gridLayout.addWidget(self.eng_exam_spin, 12, 4, 1, 1)
        self.eng_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.eng_c2_spin.setDecimals(0)
        self.eng_c2_spin.setObjectName("eng_c2_spin")
        self.gridLayout.addWidget(self.eng_c2_spin, 12, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 12, 0, 1, 1)
        self.eng_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.eng_c1_spin.setDecimals(0)
        self.eng_c1_spin.setObjectName("eng_c1_spin")
        self.gridLayout.addWidget(self.eng_c1_spin, 12, 1, 1, 1)
        self.label = QtWidgets.QLabel(NurScoreRecForm)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 9, 0, 1, 1)
        self.qur_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.qur_ass_spin.setDecimals(0)
        self.qur_ass_spin.setObjectName("qur_ass_spin")
        self.gridLayout.addWidget(self.qur_ass_spin, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.arabic_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.arabic_ass_spin.setDecimals(0)
        self.arabic_ass_spin.setObjectName("arabic_ass_spin")
        self.gridLayout.addWidget(self.arabic_ass_spin, 9, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 4, 1, 1)
        self.qur_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.qur_exam_spin.setDecimals(0)
        self.qur_exam_spin.setObjectName("qur_exam_spin")
        self.gridLayout.addWidget(self.qur_exam_spin, 1, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.qur_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.qur_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.qur_score_btn.setObjectName("qur_score_btn")
        self.gridLayout.addWidget(self.qur_score_btn, 1, 5, 1, 1)
        self.ibadat_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.ibadat_c1_spin.setDecimals(0)
        self.ibadat_c1_spin.setObjectName("ibadat_c1_spin")
        self.gridLayout.addWidget(self.ibadat_c1_spin, 5, 1, 1, 1)
        self.ibadat_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.ibadat_ass_spin.setDecimals(0)
        self.ibadat_ass_spin.setObjectName("ibadat_ass_spin")
        self.gridLayout.addWidget(self.ibadat_ass_spin, 5, 3, 1, 1)
        self.ibadat_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.ibadat_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.ibadat_score_btn.setObjectName("ibadat_score_btn")
        self.gridLayout.addWidget(self.ibadat_score_btn, 5, 5, 1, 1)
        self.arabic_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.arabic_c1_spin.setDecimals(0)
        self.arabic_c1_spin.setObjectName("arabic_c1_spin")
        self.gridLayout.addWidget(self.arabic_c1_spin, 9, 1, 1, 1)
        self.arabic_exam_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.arabic_exam_spin.setDecimals(0)
        self.arabic_exam_spin.setObjectName("arabic_exam_spin")
        self.gridLayout.addWidget(self.arabic_exam_spin, 9, 4, 1, 1)
        self.label_20 = QtWidgets.QLabel(NurScoreRecForm)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 15, 0, 1, 1)
        self.math_c2_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.math_c2_spin.setDecimals(0)
        self.math_c2_spin.setObjectName("math_c2_spin")
        self.gridLayout.addWidget(self.math_c2_spin, 15, 2, 1, 1)
        self.math_ass_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.math_ass_spin.setDecimals(0)
        self.math_ass_spin.setObjectName("math_ass_spin")
        self.gridLayout.addWidget(self.math_ass_spin, 15, 3, 1, 1)
        self.eng_score_btn = QtWidgets.QPushButton(NurScoreRecForm)
        self.eng_score_btn.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.eng_score_btn.setObjectName("eng_score_btn")
        self.gridLayout.addWidget(self.eng_score_btn, 12, 5, 1, 1)
        self.math_c1_spin = QtWidgets.QDoubleSpinBox(NurScoreRecForm)
        self.math_c1_spin.setDecimals(0)
        self.math_c1_spin.setObjectName("math_c1_spin")
        self.gridLayout.addWidget(self.math_c1_spin, 15, 1, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(123, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem15, 3, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.retranslateUi(NurScoreRecForm)
        QtCore.QMetaObject.connectSlotsByName(NurScoreRecForm)

    def retranslateUi(self, NurScoreRecForm):
        _translate = QtCore.QCoreApplication.translate
        NurScoreRecForm.setWindowTitle(_translate("NurScoreRecForm", "Nursery Scores (First Term)"))
        self.groupBox.setTitle(_translate("NurScoreRecForm", "Record Nursery Pupils\' Scores"))
        self.label_28.setText(_translate("NurScoreRecForm", "Handwriting"))
        self.nur_sc_score_btn.setText(_translate("NurScoreRecForm", "Save"))
        self.label_19.setText(_translate("NurScoreRecForm", "Nursery Science"))
        self.label_16.setText(_translate("NurScoreRecForm", "Social Norms"))
        self.math_score_btn.setText(_translate("NurScoreRecForm", "Save"))
        self.social_score_btn.setText(_translate("NurScoreRecForm", "Save"))
        self.handwriting_score_btn.setText(_translate("NurScoreRecForm", "Save"))
        self.tot_avg_btn.setText(_translate("NurScoreRecForm", "Compute Total and Average for All"))
        self.arabic_score_btn.setText(_translate("NurScoreRecForm", "Save"))
        self.label_21.setText(_translate("NurScoreRecForm", "English"))
        self.label.setText(_translate("NurScoreRecForm", "Quran"))
        self.label_3.setText(_translate("NurScoreRecForm", "Arabic Language"))
        self.label_6.setText(_translate("NurScoreRecForm", "1ST CA"))
        self.label_5.setText(_translate("NurScoreRecForm", "2ND CA"))
        self.label_7.setText(_translate("NurScoreRecForm", "ASS"))
        self.label_4.setText(_translate("NurScoreRecForm", "EXAM"))
        self.label_2.setText(_translate("NurScoreRecForm", "Ibadat"))
        self.qur_score_btn.setText(_translate("NurScoreRecForm", "Save"))
        self.ibadat_score_btn.setText(_translate("NurScoreRecForm", "Save"))
        self.label_20.setText(_translate("NurScoreRecForm", "Mathematics"))
        self.eng_score_btn.setText(_translate("NurScoreRecForm", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NurScoreRecForm = QtWidgets.QWidget()
    ui = Ui_NurScoreRecForm()
    ui.setupUi(NurScoreRecForm)
    NurScoreRecForm.show()
    sys.exit(app.exec_())