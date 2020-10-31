import sys
from PyQt5 import QtWidgets, QtPrintSupport, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QDateTime, QByteArray
from nurreport import Ui_NurReportForm
from nurreport2nd import Ui_NurReport2ndForm
from nurreport3rd import Ui_NurReport3rdForm

from nurscoresrecord import Ui_NurScoreRecForm
from nurscoresrecord2nd import Ui_NurScoreRec2ndForm
from nurscoresrecord3rd import Ui_NurScoreRec3Form
from nurscoreslist import Ui_NurScoreForm
from nurscoreslist2nd import Ui_NurScore2ndForm
from nurscoreslist3rd import Ui_NurScore3rdForm

import sqlite3
from sqlite3 import Error

class NurScoresRecord(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurScoreRecForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)
        #self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displaySpinVals)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic_score_btn.clicked.connect(self.saveArabicScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.nur_sc_score_btn.clicked.connect(self.saveNurScScores)
        self.ui.social_score_btn.clicked.connect(self.saveSocialScores)
        self.ui.handwriting_score_btn.clicked.connect(self.saveHandwiritingScores)
        self.ui.tot_avg_btn.clicked.connect(self.computeTotAvg)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_classes ORDER BY class_name')
        rows = cur.fetchall()
        classes = ["Select a class"]
        self.ui.class_comboBox.clear()
        for row in rows:
            classes.append(row[0])
        self.ui.class_comboBox.addItems(classes)
        con.commit()
        con.close()

    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ? ORDER BY admission_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select a student"]
        self.ui.stud_adm_no_comboBox.clear()
        for row in rows:
            adm_nos.append(row[0])
        self.ui.stud_adm_no_comboBox.addItems(adm_nos)
        con.close()

    def displayName(self):
        self.ui.name_label.setText("")
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no_combo = self.ui.stud_adm_no_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd, (stud_no_combo,))
        row = cur.fetchone()
        if row == None:
            self.ui.name_label.setText("")
        else:
            self.ui.name_label.setText("Name: " + row[1])

    # def displaySpinVals(self):
    #     self.ui.qur_c1_spin.setValue(0)
    #     con = sqlite3.connect("alqalamdb.db")
    #     con.execute("PRAGMA foreign_keys = 1")
    #     cur = con.cursor()
    #     score_class = self.ui.class_comboBox.currentText()
    #     stud_no = self.ui.stud_adm_no_comboBox.currentText()
    #     cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
    #     cur.execute(cmd1, (stud_no,))
    #     row = cur.fetchone()
    #     if row != None:
    #         self.ui.qur_c1_spin.setValue(row[3])

    def saveQurScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        score_class = self.ui.class_comboBox.currentText()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        qur_c1 = self.ui.qur_c1_spin.value()
        qur_c2 = self.ui.qur_c2_spin.value()
        qur_ass = self.ui.qur_ass_spin.value()
        qur_exam = self.ui.qur_exam_spin.value()
        qur_total = qur_c1 + qur_c2 + qur_ass + qur_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveIbadatScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        ibadat_c1 = self.ui.ibadat_c1_spin.value()
        ibadat_c2 = self.ui.ibadat_c2_spin.value()
        ibadat_ass = self.ui.ibadat_ass_spin.value()
        ibadat_exam = self.ui.ibadat_exam_spin.value()
        ibadat_total = ibadat_c1 + ibadat_c2 + ibadat_ass + ibadat_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no,  ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabicScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic_c1 = self.ui.arabic_c1_spin.value()
        arabic_c2 = self.ui.arabic_c2_spin.value()
        arabic_ass = self.ui.arabic_ass_spin.value()
        arabic_exam = self.ui.arabic_exam_spin.value()
        arabic_total = arabic_c1 + arabic_c2 + arabic_ass + arabic_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic_c1 == 0 and arabic_c2 == 0 and arabic_ass == 0 and arabic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, arabic_c1 = ?, arabic_c2 = ?, arabic_ass = ?, arabic_exam = ?, arabic_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveEnglishScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        eng_c1 = self.ui.eng_c1_spin.value()
        eng_c2 = self.ui.eng_c2_spin.value()
        eng_ass = self.ui.eng_ass_spin.value()
        eng_exam = self.ui.eng_exam_spin.value()
        eng_total = eng_c1 + eng_c2 + eng_ass + eng_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveMathScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        math_c1 = self.ui.math_c1_spin.value()
        math_c2 = self.ui.math_c2_spin.value()
        math_ass = self.ui.math_ass_spin.value()
        math_exam = self.ui.math_exam_spin.value()
        math_total = math_c1 + math_c2 + math_ass + math_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveNurScScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        nur_sc_c1 = self.ui.nur_sc_c1_spin.value()
        nur_sc_c2 = self.ui.nur_sc_c2_spin.value()
        nur_sc_ass = self.ui.nur_sc_ass_spin.value()
        nur_sc_exam = self.ui.nur_sc_exam_spin.value()
        nur_sc_total = nur_sc_c1 + nur_sc_c2 + nur_sc_ass + nur_sc_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if nur_sc_c1 == 0 and nur_sc_c2 == 0 and nur_sc_ass == 0 and nur_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, nur_sc_c1 = ?, nur_sc_c2 = ?, nur_sc_ass = ?, nur_sc_exam = ?, nur_sc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveSocialScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        social_c1 = self.ui.social_c1_spin.value()
        social_c2 = self.ui.social_c2_spin.value()
        social_ass = self.ui.social_ass_spin.value()
        social_exam = self.ui.social_exam_spin.value()
        social_total = social_c1 + social_c2 + social_ass + social_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if social_c1 == 0 and social_c2 == 0 and social_ass == 0 and social_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, social_c1, social_c2, social_ass, social_exam, social_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, social_c1, social_c2, social_ass, social_exam, social_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, social_c1 = ?, social_c2 = ?, social_ass = ?, social_exam = ?, social_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, social_c1, social_c2, social_ass, social_exam, social_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveHandwiritingScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        handwriting_c1 = self.ui.handwriting_c1_spin.value()
        handwriting_c2 = self.ui.handwriting_c2_spin.value()
        handwriting_ass = self.ui.handwriting_ass_spin.value()
        handwriting_exam = self.ui.handwriting_exam_spin.value()
        handwriting_total = handwriting_c1 + handwriting_c2 + handwriting_ass + handwriting_exam

        cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if handwriting_c1 == 0 and handwriting_c2 == 0 and handwriting_ass == 0 and handwriting_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_first(stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_first SET stud_no = ?, handwriting_c1 = ?, handwriting_c2 = ?, handwriting_ass = ?, handwriting_exam = ?, handwriting_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def computeTotAvg(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()
        try:
            cmd1 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42]
            avg = round((all_total/800)*100, 4)
            cmd2 = "UPDATE t_nur_scores_first SET stud_no = ?, all_total = ?, avg = ?  WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no, all_total, avg, stud_no,))
            con.commit()
            QMessageBox.information(self, "Computing Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Computing Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "Computing Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()


class NurScoresView(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurScoreForm()
        self.ui.setupUi(self)

        self.nur_report = NurReport()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()



        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generateNurReport)

        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_nur_scores_first ORDER BY score_class')
        classes = ["Select a class"]
        rows = cur.fetchall()
        for row in rows:
            if row[2] not in classes:
                classes.append(row[2])
        self.ui.class_comboBox.addItems(classes)
        con.commit()
        con.close()

    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox2.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ? ORDER BY admission_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select an admission number"]
        self.ui.stud_name_comboBox.clear()
        for row in rows:
            adm_nos.append(row[0])
        self.ui.stud_name_comboBox.addItems(adm_nos)
        con.close()

    def listStudsScores(self):
        self.ui.switch_back_btn.hide()
        self.ui.tableWidget_2.hide()
        self.ui.tableWidget.setRowCount(0)
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        cmd = "SELECT * FROM t_nur_scores_first ORDER BY stud_no"
        cur.execute(cmd)
        rows = cur.fetchall()
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                it.setText(str(column_data))
                self.ui.tableWidget.setItem(row_number, column_number, it)
        self.ui.tableWidget.show()
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(180)
        self.ui.tableWidget.setColumnWidth(0,0)
        con.close()

    def listClass(self):
        self.ui.switch_back_btn.show()
        self.ui.tableWidget.hide()
        self.ui.tableWidget_2.setRowCount(0)
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_nur_scores_first WHERE score_class = ? ORDER BY stud_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget_2.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                it.setText(str(column_data))
                self.ui.tableWidget_2.setItem(row_number, column_number, it)
        self.ui.tableWidget_2.show()
        self.ui.tableWidget_2.horizontalHeader().setDefaultSectionSize(180)
        self.ui.tableWidget_2.setColumnWidth(0,0)
        self.ui.class_comboBox.show()
        con.close()

    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_nur_scores_first WHERE score_class = ? ORDER BY stud_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select an admission number"]
        self.ui.stud_adm_no_comboBox.clear()
        for row in rows:
            adm_nos.append(row[1])
        self.ui.stud_adm_no_comboBox.addItems(adm_nos)
        con.close()

    def displayName(self):
        self.ui.name_label.setText("")
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no_combo = self.ui.stud_adm_no_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd, (stud_no_combo,))
        row = cur.fetchone()
        if row == None:
            self.ui.name_label.setText("")
        else:
            self.ui.name_label.setText("Name: \n" + row[1])

    def deleteStud(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()
        if stud_no == "Select an admission number":
            QMessageBox.critical(self, "Deleting Pupil", "ERROR: Please select pupil's admission number before pressing delete", QMessageBox.Ok)
        elif stud_no == "":
            QMessageBox.critical(self, "Deleting Pupil", "ERROR: Please select a class and pupil's admission number before pressing delete", QMessageBox.Ok)
        else:
            cmd = "DELETE FROM t_nur_scores_first WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting Pupil', "WARNING: Deleting will remove all the pupil's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generateNurReport(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        #print_date = self.nur_report.ui.dateTimeEdit.text()
        classes_combo = self.ui.class_comboBox.currentText()
        admission_no = self.ui.stud_adm_no_comboBox.currentText()
        cmd1 = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd1, (admission_no,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Printing Report", "ERROR: Please select a class and pupil's admission number before generating report", QMessageBox.Ok)
        else:
            self.nur_report.ui.name_label.setText(row[1])
            self.nur_report.ui.class_label.setText(row[3])
            self.nur_report.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.nur_report.ui.photo_label.setPixmap(QPixmap(pixmap))

            try:
                cmd3 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.nur_report.ui.qur_c1_label.setText(str(row[3]))
                self.nur_report.ui.qur_c2_label.setText(str(row[4]))
                self.nur_report.ui.qur_ass_label.setText(str(row[5]))
                self.nur_report.ui.qur_exam_label.setText(str(row[6]))
                self.nur_report.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.nur_report.ui.qur_grade_label.setText("F")
                    self.nur_report.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.nur_report.ui.qur_grade_label.setText("D")
                    self.nur_report.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.nur_report.ui.qur_grade_label.setText("C")
                    self.nur_report.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.nur_report.ui.qur_grade_label.setText("B")
                    self.nur_report.ui.qur_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.qur_grade_label.setText("A")
                    self.nur_report.ui.qur_remark_label.setText("Excellent")

                self.nur_report.ui.ibadat_c1_label.setText(str(row[8]))
                self.nur_report.ui.ibadat_c2_label.setText(str(row[9]))
                self.nur_report.ui.ibadat_ass_label.setText(str(row[10]))
                self.nur_report.ui.ibadat_exam_label.setText(str(row[11]))
                self.nur_report.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.nur_report.ui.ibadat_grade_label.setText("F")
                    self.nur_report.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.nur_report.ui.ibadat_grade_label.setText("D")
                    self.nur_report.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.nur_report.ui.ibadat_grade_label.setText("C")
                    self.nur_report.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.nur_report.ui.ibadat_grade_label.setText("B")
                    self.nur_report.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.ibadat_grade_label.setText("A")
                    self.nur_report.ui.ibadat_remark_label.setText("Excellent")

                self.nur_report.ui.arabic_c1_label.setText(str(row[13]))
                self.nur_report.ui.arabic_c2_label.setText(str(row[14]))
                self.nur_report.ui.arabic_ass_label.setText(str(row[15]))
                self.nur_report.ui.arabic_exam_label.setText(str(row[16]))
                self.nur_report.ui.arabic_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.nur_report.ui.arabic_grade_label.setText("F")
                    self.nur_report.ui.arabic_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.nur_report.ui.arabic_grade_label.setText("D")
                    self.nur_report.ui.arabic_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.nur_report.ui.arabic_grade_label.setText("C")
                    self.nur_report.ui.arabic_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.nur_report.ui.arabic_grade_label.setText("B")
                    self.nur_report.ui.arabic_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.arabic_grade_label.setText("A")
                    self.nur_report.ui.arabic_remark_label.setText("Excellent")

                self.nur_report.ui.eng_c1_label.setText(str(row[18]))
                self.nur_report.ui.eng_c2_label.setText(str(row[19]))
                self.nur_report.ui.eng_ass_label.setText(str(row[20]))
                self.nur_report.ui.eng_exam_label.setText(str(row[21]))
                self.nur_report.ui.eng_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.nur_report.ui.eng_grade_label.setText("F")
                    self.nur_report.ui.eng_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.nur_report.ui.eng_grade_label.setText("D")
                    self.nur_report.ui.eng_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.nur_report.ui.eng_grade_label.setText("C")
                    self.nur_report.ui.eng_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.nur_report.ui.eng_grade_label.setText("B")
                    self.nur_report.ui.eng_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.eng_grade_label.setText("A")
                    self.nur_report.ui.eng_remark_label.setText("Excellent")

                self.nur_report.ui.math_c1_label.setText(str(row[23]))
                self.nur_report.ui.math_c2_label.setText(str(row[24]))
                self.nur_report.ui.math_ass_label.setText(str(row[25]))
                self.nur_report.ui.math_exam_label.setText(str(row[26]))
                self.nur_report.ui.math_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.nur_report.ui.math_grade_label.setText("F")
                    self.nur_report.ui.math_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.nur_report.ui.math_grade_label.setText("D")
                    self.nur_report.ui.math_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.nur_report.ui.math_grade_label.setText("C")
                    self.nur_report.ui.math_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.nur_report.ui.math_grade_label.setText("B")
                    self.nur_report.ui.math_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.math_grade_label.setText("A")
                    self.nur_report.ui.math_remark_label.setText("Excellent")

                self.nur_report.ui.nur_sc_c1_label.setText(str(row[28]))
                self.nur_report.ui.nur_sc_c2_label.setText(str(row[29]))
                self.nur_report.ui.nur_sc_ass_label.setText(str(row[30]))
                self.nur_report.ui.nur_sc_exam_label.setText(str(row[31]))
                self.nur_report.ui.nur_sc_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.nur_report.ui.nur_sc_grade_label.setText("F")
                    self.nur_report.ui.nur_sc_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.nur_report.ui.nur_sc_grade_label.setText("D")
                    self.nur_report.ui.nur_sc_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.nur_report.ui.nur_sc_grade_label.setText("C")
                    self.nur_report.ui.nur_sc_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.nur_report.ui.nur_sc_grade_label.setText("B")
                    self.nur_report.ui.nur_sc_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.nur_sc_grade_label.setText("A")
                    self.nur_report.ui.nur_sc_remark_label.setText("Excellent")

                self.nur_report.ui.social_c1_label.setText(str(row[33]))
                self.nur_report.ui.social_c2_label.setText(str(row[34]))
                self.nur_report.ui.social_ass_label.setText(str(row[35]))
                self.nur_report.ui.social_exam_label.setText(str(row[36]))
                self.nur_report.ui.social_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.nur_report.ui.social_grade_label.setText("F")
                    self.nur_report.ui.social_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.nur_report.ui.social_grade_label.setText("D")
                    self.nur_report.ui.social_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.nur_report.ui.social_grade_label.setText("C")
                    self.nur_report.ui.social_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.nur_report.ui.social_grade_label.setText("B")
                    self.nur_report.ui.social_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.social_grade_label.setText("A")
                    self.nur_report.ui.social_remark_label.setText("Excellent")

                self.nur_report.ui.handwriting_c1_label.setText(str(row[38]))
                self.nur_report.ui.handwriting_c2_label.setText(str(row[39]))
                self.nur_report.ui.handwriting_ass_label.setText(str(row[40]))
                self.nur_report.ui.handwriting_exam_label.setText(str(row[41]))
                self.nur_report.ui.handwriting_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.nur_report.ui.handwriting_grade_label.setText("F")
                    self.nur_report.ui.handwriting_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.nur_report.ui.handwriting_grade_label.setText("D")
                    self.nur_report.ui.handwriting_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.nur_report.ui.handwriting_grade_label.setText("C")
                    self.nur_report.ui.handwriting_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.nur_report.ui.handwriting_grade_label.setText("B")
                    self.nur_report.ui.handwriting_remark_label.setText("Very Good")
                else:
                    self.nur_report.ui.handwriting_grade_label.setText("A")
                    self.nur_report.ui.handwriting_remark_label.setText("Excellent")


                self.nur_report.ui.total_scores_label.setText(str(row[43]))
                self.nur_report.ui.avg_label.setText(str(row[44]))

                if row[44] < 40:
                    self.nur_report.ui.master_com_label.setText("Bad result. Be careful.")
                    self.nur_report.ui.head_com_label.setText("Bad result.")
                elif row[44] >= 40 and row[44] < 50:
                    self.nur_report.ui.master_com_label.setText("Weak result. Work hard.")
                    self.nur_report.ui.head_com_label.setText("Weak result.")
                elif row[44] >= 50 and row[44] < 60:
                    self.nur_report.ui.master_com_label.setText("Fair result. Work hard.")
                    self.nur_report.ui.head_com_label.setText("Fair result.")
                elif row[44] >= 60 and row[44] < 70:
                    self.nur_report.ui.master_com_label.setText("Good result. Put more effort.")
                    self.nur_report.ui.head_com_label.setText("Good result.")
                else:
                    self.nur_report.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.nur_report.ui.head_com_label.setText("Excellent result.")
                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.nur_report.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.nur_report.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.nur_report.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.nur_report.ui.fees_label.setText(row[4])

                cmd8 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd8)
                row = cur.fetchone()
                self.nur_report.ui.session_label.setText(row[2])

                if self.ui.att_a_radio.isChecked() == False and self.ui.att_b_radio.isChecked() == False and self.ui.att_c_radio.isChecked() == False and self.ui.att_d_radio.isChecked() == False and self.ui.att_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grade in attendance", QMessageBox.Ok)

                elif self.ui.con_a_radio.isChecked() == False and self.ui.con_b_radio.isChecked() == False and self.ui.con_c_radio.isChecked() == False and self.ui.con_d_radio.isChecked() == False and self.ui.con_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in conduct", QMessageBox.Ok)

                elif self.ui.neat_a_radio.isChecked() == False and self.ui.neat_b_radio.isChecked() == False and self.ui.neat_c_radio.isChecked() == False and self.ui.neat_d_radio.isChecked() == False and self.ui.neat_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in neatness", QMessageBox.Ok)

                else:
                    #self.nur_report.showMaximized()
                    #self.printReport()
                    self.printPDF()
            except Error:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)
            except TypeError:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)


    def displayRadios(self):
        if self.ui.att_a_radio.isChecked():
            self.nur_report.ui.att_a_label.setText("v")
            self.nur_report.ui.att_b_label.setText("")
            self.nur_report.ui.att_c_label.setText("")
            self.nur_report.ui.att_d_label.setText("")
            self.nur_report.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.nur_report.ui.att_a_label.setText("")
            self.nur_report.ui.att_b_label.setText("v")
            self.nur_report.ui.att_c_label.setText("")
            self.nur_report.ui.att_d_label.setText("")
            self.nur_report.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.nur_report.ui.att_a_label.setText("")
            self.nur_report.ui.att_b_label.setText("")
            self.nur_report.ui.att_c_label.setText("v")
            self.nur_report.ui.att_d_label.setText("")
            self.nur_report.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.nur_report.ui.att_a_label.setText("")
            self.nur_report.ui.att_b_label.setText("")
            self.nur_report.ui.att_c_label.setText("")
            self.nur_report.ui.att_d_label.setText("v")
            self.nur_report.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.nur_report.ui.att_a_label.setText("")
            self.nur_report.ui.att_b_label.setText("")
            self.nur_report.ui.att_c_label.setText("")
            self.nur_report.ui.att_d_label.setText("")
            self.nur_report.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.nur_report.ui.con_a_label.setText("v")
            self.nur_report.ui.con_b_label.setText("")
            self.nur_report.ui.con_c_label.setText("")
            self.nur_report.ui.con_d_label.setText("")
            self.nur_report.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.nur_report.ui.con_a_label.setText("")
            self.nur_report.ui.con_b_label.setText("v")
            self.nur_report.ui.con_c_label.setText("")
            self.nur_report.ui.con_d_label.setText("")
            self.nur_report.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.nur_report.ui.con_a_label.setText("")
            self.nur_report.ui.con_b_label.setText("")
            self.nur_report.ui.con_c_label.setText("v")
            self.nur_report.ui.con_d_label.setText("")
            self.nur_report.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.nur_report.ui.con_a_label.setText("")
            self.nur_report.ui.con_b_label.setText("")
            self.nur_report.ui.con_c_label.setText("")
            self.nur_report.ui.con_d_label.setText("v")
            self.nur_report.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.nur_report.ui.con_a_label.setText("")
            self.nur_report.ui.con_b_label.setText("")
            self.nur_report.ui.con_c_label.setText("")
            self.nur_report.ui.con_d_label.setText("")
            self.nur_report.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.nur_report.ui.neat_a_label.setText("v")
            self.nur_report.ui.neat_b_label.setText("")
            self.nur_report.ui.neat_c_label.setText("")
            self.nur_report.ui.neat_d_label.setText("")
            self.nur_report.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.nur_report.ui.neat_a_label.setText("")
            self.nur_report.ui.neat_b_label.setText("v")
            self.nur_report.ui.neat_c_label.setText("")
            self.nur_report.ui.neat_d_label.setText("")
            self.nur_report.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.nur_report.ui.neat_a_label.setText("")
            self.nur_report.ui.neat_b_label.setText("v")
            self.nur_report.ui.neat_c_label.setText("")
            self.nur_report.ui.neat_d_label.setText("")
            self.nur_report.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.nur_report.ui.neat_a_label.setText("")
            self.nur_report.ui.neat_b_label.setText("")
            self.nur_report.ui.neat_c_label.setText("v")
            self.nur_report.ui.neat_d_label.setText("")
            self.nur_report.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.nur_report.ui.neat_a_label.setText("")
            self.nur_report.ui.neat_b_label.setText("")
            self.nur_report.ui.neat_c_label.setText("")
            self.nur_report.ui.neat_d_label.setText("v")
            self.nur_report.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.nur_report.ui.neat_a_label.setText("")
            self.nur_report.ui.neat_b_label.setText("")
            self.nur_report.ui.neat_c_label.setText("")
            self.nur_report.ui.neat_d_label.setText("")
            self.nur_report.ui.neat_e_label.setText("v")

    def printReport(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.nur_report.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

    def print_widget(self, widget, filename):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setOutputFileName(filename)
        painter = QtGui.QPainter(printer)

        # start scale
        xscale = printer.pageRect().width() * 1.0 / widget.width()
        yscale = printer.pageRect().height() * 1.0 / widget.height()
        scale = min(xscale, yscale)
        painter.translate(printer.paperRect().center())
        painter.scale(scale, scale)
        painter.translate(-widget.width() / 2, -widget.height() / 2)
        # end scale

        widget.render(painter)
        painter.end()

    def printPDF(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export PDF", None, "PDF files (.pdf);;All Files()"
        )
        if fn:
            if QtCore.QFileInfo(fn).suffix() == "":
                fn += ".pdf"

            #print_widget(self.label, fn)
            self.print_widget(self.nur_report, fn)

class NurReport(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurReportForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())


class NurScoresRecord2nd(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurScoreRec2ndForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic_score_btn.clicked.connect(self.saveArabicScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.nur_sc_score_btn.clicked.connect(self.saveNurScScores)
        self.ui.social_score_btn.clicked.connect(self.saveSocialScores)
        self.ui.handwriting_score_btn.clicked.connect(self.saveHandwiritingScores)
        self.ui.tot_avg_btn.clicked.connect(self.computeTotAvg)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_classes ORDER BY class_name')
        rows = cur.fetchall()
        classes = ["Select a class"]
        self.ui.class_comboBox.clear()
        for row in rows:
            classes.append(row[0])

        self.ui.class_comboBox.addItems(classes)
        con.commit()
        con.close()

    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ? ORDER BY admission_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select a student"]
        self.ui.stud_adm_no_comboBox.clear()
        for row in rows:
            adm_nos.append(row[0])
        self.ui.stud_adm_no_comboBox.addItems(adm_nos)
        con.close()

    def displayName(self):
        self.ui.name_label.setText("")
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no_combo = self.ui.stud_adm_no_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd, (stud_no_combo,))
        row = cur.fetchone()
        if row == None:
            self.ui.name_label.setText("")
        else:
            self.ui.name_label.setText("Name: " + row[1])

    def saveQurScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        score_class = self.ui.class_comboBox.currentText()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        qur_c1 = self.ui.qur_c1_spin.value()
        qur_c2 = self.ui.qur_c2_spin.value()
        qur_ass = self.ui.qur_ass_spin.value()
        qur_exam = self.ui.qur_exam_spin.value()
        qur_total = qur_c1 + qur_c2 + qur_ass + qur_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveIbadatScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        ibadat_c1 = self.ui.ibadat_c1_spin.value()
        ibadat_c2 = self.ui.ibadat_c2_spin.value()
        ibadat_ass = self.ui.ibadat_ass_spin.value()
        ibadat_exam = self.ui.ibadat_exam_spin.value()
        ibadat_total = ibadat_c1 + ibadat_c2 + ibadat_ass + ibadat_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no,  ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabicScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic_c1 = self.ui.arabic_c1_spin.value()
        arabic_c2 = self.ui.arabic_c2_spin.value()
        arabic_ass = self.ui.arabic_ass_spin.value()
        arabic_exam = self.ui.arabic_exam_spin.value()
        arabic_total = arabic_c1 + arabic_c2 + arabic_ass + arabic_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic_c1 == 0 and arabic_c2 == 0 and arabic_ass == 0 and arabic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, arabic_c1 = ?, arabic_c2 = ?, arabic_ass = ?, arabic_exam = ?, arabic_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveEnglishScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        eng_c1 = self.ui.eng_c1_spin.value()
        eng_c2 = self.ui.eng_c2_spin.value()
        eng_ass = self.ui.eng_ass_spin.value()
        eng_exam = self.ui.eng_exam_spin.value()
        eng_total = eng_c1 + eng_c2 + eng_ass + eng_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveMathScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        math_c1 = self.ui.math_c1_spin.value()
        math_c2 = self.ui.math_c2_spin.value()
        math_ass = self.ui.math_ass_spin.value()
        math_exam = self.ui.math_exam_spin.value()
        math_total = math_c1 + math_c2 + math_ass + math_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveNurScScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        nur_sc_c1 = self.ui.nur_sc_c1_spin.value()
        nur_sc_c2 = self.ui.nur_sc_c2_spin.value()
        nur_sc_ass = self.ui.nur_sc_ass_spin.value()
        nur_sc_exam = self.ui.nur_sc_exam_spin.value()
        nur_sc_total = nur_sc_c1 + nur_sc_c2 + nur_sc_ass + nur_sc_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if nur_sc_c1 == 0 and nur_sc_c2 == 0 and nur_sc_ass == 0 and nur_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, nur_sc_c1 = ?, nur_sc_c2 = ?, nur_sc_ass = ?, nur_sc_exam = ?, nur_sc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveSocialScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        social_c1 = self.ui.social_c1_spin.value()
        social_c2 = self.ui.social_c2_spin.value()
        social_ass = self.ui.social_ass_spin.value()
        social_exam = self.ui.social_exam_spin.value()
        social_total = social_c1 + social_c2 + social_ass + social_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if social_c1 == 0 and social_c2 == 0 and social_ass == 0 and social_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, social_c1, social_c2, social_ass, social_exam, social_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, social_c1, social_c2, social_ass, social_exam, social_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, social_c1 = ?, social_c2 = ?, social_ass = ?, social_exam = ?, social_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, social_c1, social_c2, social_ass, social_exam, social_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveHandwiritingScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        handwriting_c1 = self.ui.handwriting_c1_spin.value()
        handwriting_c2 = self.ui.handwriting_c2_spin.value()
        handwriting_ass = self.ui.handwriting_ass_spin.value()
        handwriting_exam = self.ui.handwriting_exam_spin.value()
        handwriting_total = handwriting_c1 + handwriting_c2 + handwriting_ass + handwriting_exam

        cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if handwriting_c1 == 0 and handwriting_c2 == 0 and handwriting_ass == 0 and handwriting_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_second(stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, handwriting_c1 = ?, handwriting_c2 = ?, handwriting_ass = ?, handwriting_exam = ?, handwriting_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def computeTotAvg(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()
        try:
            cmd1 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42]
            avg = round((all_total/800)*100, 4)

            cmd2 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum = all_total
                avg_cum = round((total_cum/800)*100, 4)
            elif row[43] == None:
                total_cum = all_total
                avg_cum = round((total_cum/800)*100, 4)
            else:
                total_cum = row[43] + all_total
                avg_cum = round((total_cum/1600)*100, 4)
            cmd3 = "UPDATE t_nur_scores_second SET stud_no = ?, all_total = ?, avg = ?, total_cum = ?, avg_cum = ?  WHERE stud_no = ?"
            cur.execute(cmd3, (stud_no, all_total, avg, total_cum, avg_cum, stud_no,))
            con.commit()
            QMessageBox.information(self, "Computing Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error as e:
            QMessageBox.critical(self, "Computing Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError as e:
            print(e)
            QMessageBox.critical(self, "Computing Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()


class NurScoresView2(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurScore2ndForm()
        self.ui.setupUi(self)

        self.nur_report2 = NurReport2()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()

        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generateNurReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)


    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_nur_scores_second ORDER BY score_class')
        classes = ["Select a class"]
        rows = cur.fetchall()
        for row in rows:
            if row[2] not in classes:
                classes.append(row[2])
        self.ui.class_comboBox.addItems(classes)
        con.commit()
        con.close()


    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox2.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ? ORDER BY admission_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select an admission number"]
        self.ui.stud_name_comboBox.clear()
        for row in rows:
            adm_nos.append(row[0])
        self.ui.stud_name_comboBox.addItems(adm_nos)
        con.close()

    def listStudsScores(self):
        self.ui.switch_back_btn.hide()
        self.ui.tableWidget_2.hide()
        self.ui.tableWidget.setRowCount(0)
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        cmd = "SELECT * FROM t_nur_scores_second ORDER BY stud_no"
        cur.execute(cmd)
        rows = cur.fetchall()
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                it.setText(str(column_data))
                self.ui.tableWidget.setItem(row_number, column_number, it)
        self.ui.tableWidget.show()
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(180)
        self.ui.tableWidget.setColumnWidth(0,0)
        con.close()

    def listClass(self):
        self.ui.switch_back_btn.show()
        self.ui.tableWidget.hide()
        self.ui.tableWidget_2.setRowCount(0)
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_nur_scores_second WHERE score_class = ? ORDER BY stud_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget_2.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                it.setText(str(column_data))
                self.ui.tableWidget_2.setItem(row_number, column_number, it)
        self.ui.tableWidget_2.show()
        self.ui.tableWidget_2.horizontalHeader().setDefaultSectionSize(180)
        self.ui.tableWidget_2.setColumnWidth(0,0)
        self.ui.class_comboBox.show()
        con.close()

    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_nur_scores_second WHERE score_class = ? ORDER BY stud_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select an admission number"]
        self.ui.stud_adm_no_comboBox.clear()
        for row in rows:
            adm_nos.append(row[1])
        self.ui.stud_adm_no_comboBox.addItems(adm_nos)
        con.close()

    def displayName(self):
        self.ui.name_label.setText("")
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no_combo = self.ui.stud_adm_no_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd, (stud_no_combo,))
        row = cur.fetchone()
        if row == None:
            self.ui.name_label.setText("")
        else:
            self.ui.name_label.setText("Name: \n" + row[1])

    def deleteStud(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()
        if stud_no == "Select an admission number":
            QMessageBox.critical(self, "Deleting Pupil", "ERROR: Please select pupil's admission number before pressing delete", QMessageBox.Ok)
        elif stud_no == "":
            QMessageBox.critical(self, "Deleting Pupil", "ERROR: Please select a class and pupil's admission number before pressing delete", QMessageBox.Ok)
        else:
            cmd = "DELETE FROM t_nur_scores_second WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting Pupil', "WARNING: Deleting will remove all the pupil's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generateNurReport(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        #print_date = self.nur_report2.ui.dateTimeEdit.text()
        classes_combo = self.ui.class_comboBox.currentText()
        admission_no = self.ui.stud_adm_no_comboBox.currentText()
        cmd1 = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd1, (admission_no,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Printing Report", "ERROR: Please select a class and pupil's admission number before generating report", QMessageBox.Ok)
        else:

            self.nur_report2.ui.name_label.setText(row[1])
            self.nur_report2.ui.class_label.setText(row[3])
            self.nur_report2.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.nur_report2.ui.photo_label.setPixmap(QPixmap(pixmap))

            cmd2 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
            cur.execute(cmd2)
            row = cur.fetchone()
            self.nur_report2.ui.session_label.setText(str(row[2]))

            try:
                cmd3 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.nur_report2.ui.qur_c1_label.setText(str(row[3]))
                self.nur_report2.ui.qur_c2_label.setText(str(row[4]))
                self.nur_report2.ui.qur_ass_label.setText(str(row[5]))
                self.nur_report2.ui.qur_exam_label.setText(str(row[6]))
                self.nur_report2.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.nur_report2.ui.qur_grade_label.setText("F")
                    self.nur_report2.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.nur_report2.ui.qur_grade_label.setText("D")
                    self.nur_report2.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.nur_report2.ui.qur_grade_label.setText("C")
                    self.nur_report2.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.nur_report2.ui.qur_grade_label.setText("B")
                    self.nur_report2.ui.qur_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.qur_grade_label.setText("A")
                    self.nur_report2.ui.qur_remark_label.setText("Excellent")

                self.nur_report2.ui.ibadat_c1_label.setText(str(row[8]))
                self.nur_report2.ui.ibadat_c2_label.setText(str(row[9]))
                self.nur_report2.ui.ibadat_ass_label.setText(str(row[10]))
                self.nur_report2.ui.ibadat_exam_label.setText(str(row[11]))
                self.nur_report2.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.nur_report2.ui.ibadat_grade_label.setText("F")
                    self.nur_report2.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.nur_report2.ui.ibadat_grade_label.setText("D")
                    self.nur_report2.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.nur_report2.ui.ibadat_grade_label.setText("C")
                    self.nur_report2.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.nur_report2.ui.ibadat_grade_label.setText("B")
                    self.nur_report2.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.ibadat_grade_label.setText("A")
                    self.nur_report2.ui.ibadat_remark_label.setText("Excellent")

                self.nur_report2.ui.arabic_c1_label.setText(str(row[13]))
                self.nur_report2.ui.arabic_c2_label.setText(str(row[14]))
                self.nur_report2.ui.arabic_ass_label.setText(str(row[15]))
                self.nur_report2.ui.arabic_exam_label.setText(str(row[16]))
                self.nur_report2.ui.arabic_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.nur_report2.ui.arabic_grade_label.setText("F")
                    self.nur_report2.ui.arabic_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.nur_report2.ui.arabic_grade_label.setText("D")
                    self.nur_report2.ui.arabic_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.nur_report2.ui.arabic_grade_label.setText("C")
                    self.nur_report2.ui.arabic_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.nur_report2.ui.arabic_grade_label.setText("B")
                    self.nur_report2.ui.arabic_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.arabic_grade_label.setText("A")
                    self.nur_report2.ui.arabic_remark_label.setText("Excellent")

                self.nur_report2.ui.eng_c1_label.setText(str(row[18]))
                self.nur_report2.ui.eng_c2_label.setText(str(row[19]))
                self.nur_report2.ui.eng_ass_label.setText(str(row[20]))
                self.nur_report2.ui.eng_exam_label.setText(str(row[21]))
                self.nur_report2.ui.eng_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.nur_report2.ui.eng_grade_label.setText("F")
                    self.nur_report2.ui.eng_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.nur_report2.ui.eng_grade_label.setText("D")
                    self.nur_report2.ui.eng_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.nur_report2.ui.eng_grade_label.setText("C")
                    self.nur_report2.ui.eng_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.nur_report2.ui.eng_grade_label.setText("B")
                    self.nur_report2.ui.eng_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.eng_grade_label.setText("A")
                    self.nur_report2.ui.eng_remark_label.setText("Excellent")

                self.nur_report2.ui.math_c1_label.setText(str(row[23]))
                self.nur_report2.ui.math_c2_label.setText(str(row[24]))
                self.nur_report2.ui.math_ass_label.setText(str(row[25]))
                self.nur_report2.ui.math_exam_label.setText(str(row[26]))
                self.nur_report2.ui.math_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.nur_report2.ui.math_grade_label.setText("F")
                    self.nur_report2.ui.math_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.nur_report2.ui.math_grade_label.setText("D")
                    self.nur_report2.ui.math_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.nur_report2.ui.math_grade_label.setText("C")
                    self.nur_report2.ui.math_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.nur_report2.ui.math_grade_label.setText("B")
                    self.nur_report2.ui.math_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.math_grade_label.setText("A")
                    self.nur_report2.ui.math_remark_label.setText("Excellent")

                self.nur_report2.ui.nur_sc_c1_label.setText(str(row[28]))
                self.nur_report2.ui.nur_sc_c2_label.setText(str(row[29]))
                self.nur_report2.ui.nur_sc_ass_label.setText(str(row[30]))
                self.nur_report2.ui.nur_sc_exam_label.setText(str(row[31]))
                self.nur_report2.ui.nur_sc_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.nur_report2.ui.nur_sc_grade_label.setText("F")
                    self.nur_report2.ui.nur_sc_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.nur_report2.ui.nur_sc_grade_label.setText("D")
                    self.nur_report2.ui.nur_sc_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.nur_report2.ui.nur_sc_grade_label.setText("C")
                    self.nur_report2.ui.nur_sc_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.nur_report2.ui.nur_sc_grade_label.setText("B")
                    self.nur_report2.ui.nur_sc_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.nur_sc_grade_label.setText("A")
                    self.nur_report2.ui.nur_sc_remark_label.setText("Excellent")

                self.nur_report2.ui.social_c1_label.setText(str(row[33]))
                self.nur_report2.ui.social_c2_label.setText(str(row[34]))
                self.nur_report2.ui.social_ass_label.setText(str(row[35]))
                self.nur_report2.ui.social_exam_label.setText(str(row[36]))
                self.nur_report2.ui.social_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.nur_report2.ui.social_grade_label.setText("F")
                    self.nur_report2.ui.social_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.nur_report2.ui.social_grade_label.setText("D")
                    self.nur_report2.ui.social_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.nur_report2.ui.social_grade_label.setText("C")
                    self.nur_report2.ui.social_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.nur_report2.ui.social_grade_label.setText("B")
                    self.nur_report2.ui.social_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.social_grade_label.setText("A")
                    self.nur_report2.ui.social_remark_label.setText("Excellent")

                self.nur_report2.ui.handwriting_c1_label.setText(str(row[38]))
                self.nur_report2.ui.handwriting_c2_label.setText(str(row[39]))
                self.nur_report2.ui.handwriting_ass_label.setText(str(row[40]))
                self.nur_report2.ui.handwriting_exam_label.setText(str(row[41]))
                self.nur_report2.ui.handwriting_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.nur_report2.ui.handwriting_grade_label.setText("F")
                    self.nur_report2.ui.handwriting_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.nur_report2.ui.handwriting_grade_label.setText("D")
                    self.nur_report2.ui.handwriting_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.nur_report2.ui.handwriting_grade_label.setText("C")
                    self.nur_report2.ui.handwriting_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.nur_report2.ui.handwriting_grade_label.setText("B")
                    self.nur_report2.ui.handwriting_remark_label.setText("Very Good")
                else:
                    self.nur_report2.ui.handwriting_grade_label.setText("A")
                    self.nur_report2.ui.handwriting_remark_label.setText("Excellent")

                self.nur_report2.ui.total_scores2_label.setText(str(row[43]))
                self.nur_report2.ui.avg2_label.setText(str(row[44]))
                self.nur_report2.ui.total_cum_label.setText(str(row[45]))
                self.nur_report2.ui.avg_cum_label.setText(str(row[46]))

                if row[44] < 40:
                    self.nur_report2.ui.master_com_label.setText("Bad result. Be careful.")
                    self.nur_report2.ui.head_com_label.setText("Bad result.")
                elif row[44] >= 40 and row[44] < 50:
                    self.nur_report2.ui.master_com_label.setText("Weak result. Work hard.")
                    self.nur_report2.ui.head_com_label.setText("Weak result.")
                elif row[44] >= 50 and row[44] < 60:
                    self.nur_report2.ui.master_com_label.setText("Fair result. Work hard.")
                    self.nur_report2.ui.head_com_label.setText("Fair result.")
                elif row[44] >= 60 and row[44] < 70:
                    self.nur_report2.ui.master_com_label.setText("Good result. Put more effort.")
                    self.nur_report2.ui.head_com_label.setText("Good result.")
                else:
                    self.nur_report2.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.nur_report2.ui.head_com_label.setText("Excellent result.")

                cmd8 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
                cur.execute(cmd8, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.nur_report2.ui.total_scores_label.setText("None")
                    self.nur_report2.ui.avg_label.setText("None")
                elif row[43] == None and row[44] == None:
                    self.nur_report2.ui.total_scores_label.setText("None")
                    self.nur_report2.ui.avg_label.setText("None")
                else:
                    self.nur_report2.ui.total_scores_label.setText(str(row[43]))
                    self.nur_report2.ui.avg_label.setText(str(row[44]))

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.nur_report2.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.nur_report2.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.nur_report2.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.nur_report2.ui.fees_label.setText(row[4])

                if self.ui.att_a_radio.isChecked() == False and self.ui.att_b_radio.isChecked() == False and self.ui.att_c_radio.isChecked() == False and self.ui.att_d_radio.isChecked() == False and self.ui.att_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grade in attendance", QMessageBox.Ok)

                elif self.ui.con_a_radio.isChecked() == False and self.ui.con_b_radio.isChecked() == False and self.ui.con_c_radio.isChecked() == False and self.ui.con_d_radio.isChecked() == False and self.ui.con_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in conduct", QMessageBox.Ok)

                elif self.ui.neat_a_radio.isChecked() == False and self.ui.neat_b_radio.isChecked() == False and self.ui.neat_c_radio.isChecked() == False and self.ui.neat_d_radio.isChecked() == False and self.ui.neat_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in neatness", QMessageBox.Ok)
                else:
                    self.printReport2()
            except Error:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)
            except TypeError:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)

    def displayRadios(self):
        if self.ui.att_a_radio.isChecked():
            self.nur_report2.ui.att_a_label.setText("v")
            self.nur_report2.ui.att_b_label.setText("")
            self.nur_report2.ui.att_c_label.setText("")
            self.nur_report2.ui.att_d_label.setText("")
            self.nur_report2.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.nur_report2.ui.att_a_label.setText("")
            self.nur_report2.ui.att_b_label.setText("v")
            self.nur_report2.ui.att_c_label.setText("")
            self.nur_report2.ui.att_d_label.setText("")
            self.nur_report2.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.nur_report2.ui.att_a_label.setText("")
            self.nur_report2.ui.att_b_label.setText("")
            self.nur_report2.ui.att_c_label.setText("v")
            self.nur_report2.ui.att_d_label.setText("")
            self.nur_report2.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.nur_report2.ui.att_a_label.setText("")
            self.nur_report2.ui.att_b_label.setText("")
            self.nur_report2.ui.att_c_label.setText("")
            self.nur_report2.ui.att_d_label.setText("v")
            self.nur_report2.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.nur_report2.ui.att_a_label.setText("")
            self.nur_report2.ui.att_b_label.setText("")
            self.nur_report2.ui.att_c_label.setText("")
            self.nur_report2.ui.att_d_label.setText("")
            self.nur_report2.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.nur_report2.ui.con_a_label.setText("v")
            self.nur_report2.ui.con_b_label.setText("")
            self.nur_report2.ui.con_c_label.setText("")
            self.nur_report2.ui.con_d_label.setText("")
            self.nur_report2.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.nur_report2.ui.con_a_label.setText("")
            self.nur_report2.ui.con_b_label.setText("v")
            self.nur_report2.ui.con_c_label.setText("")
            self.nur_report2.ui.con_d_label.setText("")
            self.nur_report2.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.nur_report2.ui.con_a_label.setText("")
            self.nur_report2.ui.con_b_label.setText("")
            self.nur_report2.ui.con_c_label.setText("v")
            self.nur_report2.ui.con_d_label.setText("")
            self.nur_report2.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.nur_report2.ui.con_a_label.setText("")
            self.nur_report2.ui.con_b_label.setText("")
            self.nur_report2.ui.con_c_label.setText("")
            self.nur_report2.ui.con_d_label.setText("v")
            self.nur_report2.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.nur_report2.ui.con_a_label.setText("")
            self.nur_report2.ui.con_b_label.setText("")
            self.nur_report2.ui.con_c_label.setText("")
            self.nur_report2.ui.con_d_label.setText("")
            self.nur_report2.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.nur_report2.ui.neat_a_label.setText("v")
            self.nur_report2.ui.neat_b_label.setText("")
            self.nur_report2.ui.neat_c_label.setText("")
            self.nur_report2.ui.neat_d_label.setText("")
            self.nur_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.nur_report2.ui.neat_a_label.setText("")
            self.nur_report2.ui.neat_b_label.setText("v")
            self.nur_report2.ui.neat_c_label.setText("")
            self.nur_report2.ui.neat_d_label.setText("")
            self.nur_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.nur_report2.ui.neat_a_label.setText("")
            self.nur_report2.ui.neat_b_label.setText("v")
            self.nur_report2.ui.neat_c_label.setText("")
            self.nur_report2.ui.neat_d_label.setText("")
            self.nur_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.nur_report2.ui.neat_a_label.setText("")
            self.nur_report2.ui.neat_b_label.setText("")
            self.nur_report2.ui.neat_c_label.setText("v")
            self.nur_report2.ui.neat_d_label.setText("")
            self.nur_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.nur_report2.ui.neat_a_label.setText("")
            self.nur_report2.ui.neat_b_label.setText("")
            self.nur_report2.ui.neat_c_label.setText("")
            self.nur_report2.ui.neat_d_label.setText("v")
            self.nur_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.nur_report2.ui.neat_a_label.setText("")
            self.nur_report2.ui.neat_b_label.setText("")
            self.nur_report2.ui.neat_c_label.setText("")
            self.nur_report2.ui.neat_d_label.setText("")
            self.nur_report2.ui.neat_e_label.setText("v")


    def printReport2(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.nur_report2.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

class NurReport2(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurReport2ndForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())


class NurScoresRecord3rd(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurScoreRec3Form()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic_score_btn.clicked.connect(self.saveArabicScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.nur_sc_score_btn.clicked.connect(self.saveNurScScores)
        self.ui.social_score_btn.clicked.connect(self.saveSocialScores)
        self.ui.handwriting_score_btn.clicked.connect(self.saveHandwiritingScores)
        self.ui.tot_avg_btn.clicked.connect(self.computeTotAvg)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_classes ORDER BY class_name')
        rows = cur.fetchall()
        classes = ["Select a class"]
        self.ui.class_comboBox.clear()
        for row in rows:
            classes.append(row[0])
        self.ui.class_comboBox.addItems(classes)
        con.commit()
        con.close()

    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ? ORDER BY admission_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select a student"]
        self.ui.stud_adm_no_comboBox.clear()
        for row in rows:
            adm_nos.append(row[0])
        self.ui.stud_adm_no_comboBox.addItems(adm_nos)
        con.close()

    def displayName(self):
        self.ui.name_label.setText("")
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no_combo = self.ui.stud_adm_no_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd, (stud_no_combo,))
        row = cur.fetchone()
        if row == None:
            self.ui.name_label.setText("")
        else:
            self.ui.name_label.setText("Name: " + row[1])

    def saveQurScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        score_class = self.ui.class_comboBox.currentText()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        qur_c1 = self.ui.qur_c1_spin.value()
        qur_c2 = self.ui.qur_c2_spin.value()
        qur_ass = self.ui.qur_ass_spin.value()
        qur_exam = self.ui.qur_exam_spin.value()
        qur_total = qur_c1 + qur_c2 + qur_ass + qur_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveIbadatScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        ibadat_c1 = self.ui.ibadat_c1_spin.value()
        ibadat_c2 = self.ui.ibadat_c2_spin.value()
        ibadat_ass = self.ui.ibadat_ass_spin.value()
        ibadat_exam = self.ui.ibadat_exam_spin.value()
        ibadat_total = ibadat_c1 + ibadat_c2 + ibadat_ass + ibadat_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no,  ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabicScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic_c1 = self.ui.arabic_c1_spin.value()
        arabic_c2 = self.ui.arabic_c2_spin.value()
        arabic_ass = self.ui.arabic_ass_spin.value()
        arabic_exam = self.ui.arabic_exam_spin.value()
        arabic_total = arabic_c1 + arabic_c2 + arabic_ass + arabic_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic_c1 == 0 and arabic_c2 == 0 and arabic_ass == 0 and arabic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, arabic_c1 = ?, arabic_c2 = ?, arabic_ass = ?, arabic_exam = ?, arabic_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic_c1, arabic_c2, arabic_ass, arabic_exam, arabic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveEnglishScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        eng_c1 = self.ui.eng_c1_spin.value()
        eng_c2 = self.ui.eng_c2_spin.value()
        eng_ass = self.ui.eng_ass_spin.value()
        eng_exam = self.ui.eng_exam_spin.value()
        eng_total = eng_c1 + eng_c2 + eng_ass + eng_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveMathScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        math_c1 = self.ui.math_c1_spin.value()
        math_c2 = self.ui.math_c2_spin.value()
        math_ass = self.ui.math_ass_spin.value()
        math_exam = self.ui.math_exam_spin.value()
        math_total = math_c1 + math_c2 + math_ass + math_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveNurScScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        nur_sc_c1 = self.ui.nur_sc_c1_spin.value()
        nur_sc_c2 = self.ui.nur_sc_c2_spin.value()
        nur_sc_ass = self.ui.nur_sc_ass_spin.value()
        nur_sc_exam = self.ui.nur_sc_exam_spin.value()
        nur_sc_total = nur_sc_c1 + nur_sc_c2 + nur_sc_ass + nur_sc_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if nur_sc_c1 == 0 and nur_sc_c2 == 0 and nur_sc_ass == 0 and nur_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, nur_sc_c1 = ?, nur_sc_c2 = ?, nur_sc_ass = ?, nur_sc_exam = ?, nur_sc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, nur_sc_c1, nur_sc_c2, nur_sc_ass, nur_sc_exam, nur_sc_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveSocialScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        social_c1 = self.ui.social_c1_spin.value()
        social_c2 = self.ui.social_c2_spin.value()
        social_ass = self.ui.social_ass_spin.value()
        social_exam = self.ui.social_exam_spin.value()
        social_total = social_c1 + social_c2 + social_ass + social_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if social_c1 == 0 and social_c2 == 0 and social_ass == 0 and social_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, social_c1, social_c2, social_ass, social_exam, social_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, social_c1, social_c2, social_ass, social_exam, social_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, social_c1 = ?, social_c2 = ?, social_ass = ?, social_exam = ?, social_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, social_c1, social_c2, social_ass, social_exam, social_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveHandwiritingScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        handwriting_c1 = self.ui.handwriting_c1_spin.value()
        handwriting_c2 = self.ui.handwriting_c2_spin.value()
        handwriting_ass = self.ui.handwriting_ass_spin.value()
        handwriting_exam = self.ui.handwriting_exam_spin.value()
        handwriting_total = handwriting_c1 + handwriting_c2 + handwriting_ass + handwriting_exam

        cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if handwriting_c1 == 0 and handwriting_c2 == 0 and handwriting_ass == 0 and handwriting_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_nur_scores_third(stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, handwriting_c1 = ?, handwriting_c2 = ?, handwriting_ass = ?, handwriting_exam = ?, handwriting_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def computeTotAvg(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()
        try:
            cmd1 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42]
            avg = round((all_total/800)*100, 4)

            cmd0 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
            cur.execute(cmd0, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum0 = all_total
            elif row[43] == None:
                total_cum0 = all_total
            else:
                total_cum0 = row[43] + all_total

            cmd2 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum = total_cum0
                avg_cum = round((total_cum/1600)*100, 4)
            elif row[43] == row[45]:
                total_cum = row[43] + total_cum0
                avg_cum = round((total_cum/1600)*100, 4)
            else:
                total_cum = row[43] + total_cum0
                avg_cum = round((total_cum/2400)*100, 4)


            cmd3 = "UPDATE t_nur_scores_third SET stud_no = ?, all_total = ?, avg = ?, total_cum = ?, avg_cum = ?  WHERE stud_no = ?"
            cur.execute(cmd3, (stud_no, all_total, avg, total_cum, avg_cum, stud_no,))
            con.commit()
            QMessageBox.information(self, "Computing Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Computing Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "Computing Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()



class NurScoresView3(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_NurScore3rdForm()
        self.ui.setupUi(self)

        self.nur_report3 = NurReport3()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()



        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generateNurReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)


    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_nur_scores_third ORDER BY score_class')
        classes = ["Select a class"]
        rows = cur.fetchall()
        for row in rows:
            if row[2] not in classes:
                classes.append(row[2])
        self.ui.class_comboBox.addItems(classes)
        con.commit()
        con.close()


    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox2.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ? ORDER BY admission_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select an admission number"]
        self.ui.stud_name_comboBox.clear()
        for row in rows:
            adm_nos.append(row[0])
        self.ui.stud_name_comboBox.addItems(adm_nos)
        con.close()

    def listStudsScores(self):
        self.ui.switch_back_btn.hide()
        self.ui.tableWidget_2.hide()
        self.ui.tableWidget.setRowCount(0)
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        cmd = "SELECT * FROM t_nur_scores_third ORDER BY stud_no"
        cur.execute(cmd)
        rows = cur.fetchall()
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                it.setText(str(column_data))
                self.ui.tableWidget.setItem(row_number, column_number, it)
        self.ui.tableWidget.show()
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(180)
        self.ui.tableWidget.setColumnWidth(0,0)
        con.close()

    def listClass(self):
        self.ui.switch_back_btn.show()
        self.ui.tableWidget.hide()
        self.ui.tableWidget_2.setRowCount(0)
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_nur_scores_third WHERE score_class = ? ORDER BY stud_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget_2.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                it.setText(str(column_data))
                self.ui.tableWidget_2.setItem(row_number, column_number, it)
        self.ui.tableWidget_2.show()
        self.ui.tableWidget_2.horizontalHeader().setDefaultSectionSize(180)
        self.ui.tableWidget_2.setColumnWidth(0,0)
        self.ui.class_comboBox.show()
        con.close()

    def displayStuds(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_nur_scores_third WHERE score_class = ? ORDER BY stud_no"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        adm_nos = ["Select an admission number"]
        self.ui.stud_adm_no_comboBox.clear()
        for row in rows:
            adm_nos.append(row[1])
        self.ui.stud_adm_no_comboBox.addItems(adm_nos)
        con.close()

    def displayName(self):
        self.ui.name_label.setText("")
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no_combo = self.ui.stud_adm_no_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd, (stud_no_combo,))
        row = cur.fetchone()
        if row == None:
            self.ui.name_label.setText("")
        else:
            self.ui.name_label.setText("Name: \n" + row[1])

    def deleteStud(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()
        if stud_no == "Select an admission number":
            QMessageBox.critical(self, "Deleting Pupil", "ERROR: Please select pupil's admission number before pressing delete", QMessageBox.Ok)
        elif stud_no == "":
            QMessageBox.critical(self, "Deleting Pupil", "ERROR: Please select a class and pupil's admission number before pressing delete", QMessageBox.Ok)
        else:
            cmd = "DELETE FROM t_nur_scores_third WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting Pupil', "WARNING: Deleting will remove all the pupil's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generateNurReport(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        admission_no = self.ui.stud_adm_no_comboBox.currentText()
        cmd1 = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd1, (admission_no,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Printing Report", "ERROR: Please select a class and pupil's admission number before generating report", QMessageBox.Ok)
        else:
            self.nur_report3.hide()
            self.nur_report3.ui.name_label.setText(row[1])
            self.nur_report3.ui.class_label.setText(row[3])
            self.nur_report3.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.nur_report3.ui.photo_label.setPixmap(QPixmap(pixmap))

            cmd2 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
            cur.execute(cmd2)
            row = cur.fetchone()
            self.nur_report3.ui.session_label.setText(str(row[2]))

            try:
                cmd3 = "SELECT * FROM t_nur_scores_third WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.nur_report3.ui.qur_c1_label.setText(str(row[3]))
                self.nur_report3.ui.qur_c2_label.setText(str(row[4]))
                self.nur_report3.ui.qur_ass_label.setText(str(row[5]))
                self.nur_report3.ui.qur_exam_label.setText(str(row[6]))
                self.nur_report3.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.nur_report3.ui.qur_grade_label.setText("F")
                    self.nur_report3.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.nur_report3.ui.qur_grade_label.setText("D")
                    self.nur_report3.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.nur_report3.ui.qur_grade_label.setText("C")
                    self.nur_report3.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.nur_report3.ui.qur_grade_label.setText("B")
                    self.nur_report3.ui.qur_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.qur_grade_label.setText("A")
                    self.nur_report3.ui.qur_remark_label.setText("Excellent")

                self.nur_report3.ui.ibadat_c1_label.setText(str(row[8]))
                self.nur_report3.ui.ibadat_c2_label.setText(str(row[9]))
                self.nur_report3.ui.ibadat_ass_label.setText(str(row[10]))
                self.nur_report3.ui.ibadat_exam_label.setText(str(row[11]))
                self.nur_report3.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.nur_report3.ui.ibadat_grade_label.setText("F")
                    self.nur_report3.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.nur_report3.ui.ibadat_grade_label.setText("D")
                    self.nur_report3.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.nur_report3.ui.ibadat_grade_label.setText("C")
                    self.nur_report3.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.nur_report3.ui.ibadat_grade_label.setText("B")
                    self.nur_report3.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.ibadat_grade_label.setText("A")
                    self.nur_report3.ui.ibadat_remark_label.setText("Excellent")

                self.nur_report3.ui.arabic_c1_label.setText(str(row[13]))
                self.nur_report3.ui.arabic_c2_label.setText(str(row[14]))
                self.nur_report3.ui.arabic_ass_label.setText(str(row[15]))
                self.nur_report3.ui.arabic_exam_label.setText(str(row[16]))
                self.nur_report3.ui.arabic_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.nur_report3.ui.arabic_grade_label.setText("F")
                    self.nur_report3.ui.arabic_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.nur_report3.ui.arabic_grade_label.setText("D")
                    self.nur_report3.ui.arabic_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.nur_report3.ui.arabic_grade_label.setText("C")
                    self.nur_report3.ui.arabic_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.nur_report3.ui.arabic_grade_label.setText("B")
                    self.nur_report3.ui.arabic_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.arabic_grade_label.setText("A")
                    self.nur_report3.ui.arabic_remark_label.setText("Excellent")

                self.nur_report3.ui.eng_c1_label.setText(str(row[18]))
                self.nur_report3.ui.eng_c2_label.setText(str(row[19]))
                self.nur_report3.ui.eng_ass_label.setText(str(row[20]))
                self.nur_report3.ui.eng_exam_label.setText(str(row[21]))
                self.nur_report3.ui.eng_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.nur_report3.ui.eng_grade_label.setText("F")
                    self.nur_report3.ui.eng_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.nur_report3.ui.eng_grade_label.setText("D")
                    self.nur_report3.ui.eng_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.nur_report3.ui.eng_grade_label.setText("C")
                    self.nur_report3.ui.eng_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.nur_report3.ui.eng_grade_label.setText("B")
                    self.nur_report3.ui.eng_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.eng_grade_label.setText("A")
                    self.nur_report3.ui.eng_remark_label.setText("Excellent")

                self.nur_report3.ui.math_c1_label.setText(str(row[23]))
                self.nur_report3.ui.math_c2_label.setText(str(row[24]))
                self.nur_report3.ui.math_ass_label.setText(str(row[25]))
                self.nur_report3.ui.math_exam_label.setText(str(row[26]))
                self.nur_report3.ui.math_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.nur_report3.ui.math_grade_label.setText("F")
                    self.nur_report3.ui.math_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.nur_report3.ui.math_grade_label.setText("D")
                    self.nur_report3.ui.math_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.nur_report3.ui.math_grade_label.setText("C")
                    self.nur_report3.ui.math_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.nur_report3.ui.math_grade_label.setText("B")
                    self.nur_report3.ui.math_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.math_grade_label.setText("A")
                    self.nur_report3.ui.math_remark_label.setText("Excellent")

                self.nur_report3.ui.nur_sc_c1_label.setText(str(row[28]))
                self.nur_report3.ui.nur_sc_c2_label.setText(str(row[29]))
                self.nur_report3.ui.nur_sc_ass_label.setText(str(row[30]))
                self.nur_report3.ui.nur_sc_exam_label.setText(str(row[31]))
                self.nur_report3.ui.nur_sc_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.nur_report3.ui.nur_sc_grade_label.setText("F")
                    self.nur_report3.ui.nur_sc_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.nur_report3.ui.nur_sc_grade_label.setText("D")
                    self.nur_report3.ui.nur_sc_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.nur_report3.ui.nur_sc_grade_label.setText("C")
                    self.nur_report3.ui.nur_sc_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.nur_report3.ui.nur_sc_grade_label.setText("B")
                    self.nur_report3.ui.nur_sc_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.nur_sc_grade_label.setText("A")
                    self.nur_report3.ui.nur_sc_remark_label.setText("Excellent")


                self.nur_report3.ui.social_c1_label.setText(str(row[33]))
                self.nur_report3.ui.social_c2_label.setText(str(row[34]))
                self.nur_report3.ui.social_ass_label.setText(str(row[35]))
                self.nur_report3.ui.social_exam_label.setText(str(row[36]))
                self.nur_report3.ui.social_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.nur_report3.ui.social_grade_label.setText("F")
                    self.nur_report3.ui.social_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.nur_report3.ui.social_grade_label.setText("D")
                    self.nur_report3.ui.social_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.nur_report3.ui.social_grade_label.setText("C")
                    self.nur_report3.ui.social_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.nur_report3.ui.social_grade_label.setText("B")
                    self.nur_report3.ui.social_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.social_grade_label.setText("A")
                    self.nur_report3.ui.social_remark_label.setText("Excellent")

                self.nur_report3.ui.handwriting_c1_label.setText(str(row[38]))
                self.nur_report3.ui.handwriting_c2_label.setText(str(row[39]))
                self.nur_report3.ui.handwriting_ass_label.setText(str(row[40]))
                self.nur_report3.ui.handwriting_exam_label.setText(str(row[41]))
                self.nur_report3.ui.handwriting_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.nur_report3.ui.handwriting_grade_label.setText("F")
                    self.nur_report3.ui.handwriting_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.nur_report3.ui.handwriting_grade_label.setText("D")
                    self.nur_report3.ui.handwriting_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.nur_report3.ui.handwriting_grade_label.setText("C")
                    self.nur_report3.ui.handwriting_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.nur_report3.ui.handwriting_grade_label.setText("B")
                    self.nur_report3.ui.handwriting_remark_label.setText("Very Good")
                else:
                    self.nur_report3.ui.handwriting_grade_label.setText("A")
                    self.nur_report3.ui.handwriting_remark_label.setText("Excellent")

                self.nur_report3.ui.total_scores3_label.setText(str(row[43]))
                self.nur_report3.ui.avg3_label.setText(str(row[44]))
                self.nur_report3.ui.total_cum_label.setText(str(row[45]))
                self.nur_report3.ui.avg_cum_label.setText(str(row[46]))

                if row[44] < 40:
                    self.nur_report3.ui.master_com_label.setText("Bad result. Be careful.")
                    self.nur_report3.ui.head_com_label.setText("Bad result.")
                elif row[44] >= 40 and row[44] < 50:
                    self.nur_report3.ui.master_com_label.setText("Weak result. Work hard.")
                    self.nur_report3.ui.head_com_label.setText("Weak result.")
                elif row[44] >= 50 and row[44] < 60:
                    self.nur_report3.ui.master_com_label.setText("Fair result. Work hard.")
                    self.nur_report3.ui.head_com_label.setText("Fair result.")
                elif row[44] >= 60 and row[44] < 70:
                    self.nur_report3.ui.master_com_label.setText("Good result. Put more effort.")
                    self.nur_report3.ui.head_com_label.setText("Good result.")
                else:
                    self.nur_report3.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.nur_report3.ui.head_com_label.setText("Excellent result.")

                cmd8 = "SELECT * FROM t_nur_scores_first WHERE stud_no = ?"
                cur.execute(cmd8, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.nur_report3.ui.total_scores_label.setText("None")
                    self.nur_report3.ui.avg_label.setText("None")
                elif row[43] == None and row[44] == None:
                     self.nur_report3.ui.total_scores_label.setText("None")
                     self.nur_report3.ui.avg_label.setText("None")
                else:
                    self.nur_report3.ui.total_scores_label.setText(str(row[43]))
                    self.nur_report3.ui.avg_label.setText(str(row[44]))

                cmd9 = "SELECT * FROM t_nur_scores_second WHERE stud_no = ?"
                cur.execute(cmd9, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.nur_report3.ui.total_scores2_label.setText("None")
                    self.nur_report3.ui.avg2_label.setText("None")
                elif row[43] and row[44] == None:
                     self.nur_report3.ui.total_scores2_label.setText("None")
                     self.nur_report3.ui.avg2_label.setText("None")
                else:
                    self.nur_report3.ui.total_scores2_label.setText(str(row[43]))
                    self.nur_report3.ui.avg2_label.setText(str(row[44]))

                positions = []
                cmd10 = "SELECT * FROM t_nur_scores_third WHERE score_class = ? ORDER BY avg DESC"
                cur.execute(cmd10, (classes_combo,))
                rows = cur.fetchall()
                for row in rows:
                    positions.append(row[1])
                self.nur_report3.ui.out_of_label.setText(str(len(positions)))
                for i in range(len(positions)):
                    if admission_no == positions[i]:
                        if i in range (10, len(positions), 100):
                            self.nur_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (11, len(positions), 100):
                            self.nur_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (12, len(positions), 100):
                            self.nur_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (0, len(positions), 10):
                            self.nur_report3.ui.position_label.setText(str(i+1)+"st")
                        elif i in range (1, len(positions), 10):
                            self.nur_report3.ui.position_label.setText(str(i+1)+"nd")
                        elif i in range (2, len(positions), 10):
                            self.nur_report3.ui.position_label.setText(str(i+1)+"rd")
                        else:
                            self.nur_report3.ui.position_label.setText(str(i+1)+"th")

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.nur_report3.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.nur_report3.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.nur_report3.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.nur_report3.ui.fees_label.setText(row[4])

                if self.ui.att_a_radio.isChecked() == False and self.ui.att_b_radio.isChecked() == False and self.ui.att_c_radio.isChecked() == False and self.ui.att_d_radio.isChecked() == False and self.ui.att_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grade in attendance", QMessageBox.Ok)

                elif self.ui.con_a_radio.isChecked() == False and self.ui.con_b_radio.isChecked() == False and self.ui.con_c_radio.isChecked() == False and self.ui.con_d_radio.isChecked() == False and self.ui.con_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in conduct", QMessageBox.Ok)

                elif self.ui.neat_a_radio.isChecked() == False and self.ui.neat_b_radio.isChecked() == False and self.ui.neat_c_radio.isChecked() == False and self.ui.neat_d_radio.isChecked() == False and self.ui.neat_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in neatness", QMessageBox.Ok)

                else:
                    self.printReport3()
            except Error:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)
            except TypeError:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)

    def displayRadios(self):
        if self.ui.att_a_radio.isChecked():
            self.nur_report3.ui.att_a_label.setText("v")
            self.nur_report3.ui.att_b_label.setText("")
            self.nur_report3.ui.att_c_label.setText("")
            self.nur_report3.ui.att_d_label.setText("")
            self.nur_report3.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.nur_report3.ui.att_a_label.setText("")
            self.nur_report3.ui.att_b_label.setText("v")
            self.nur_report3.ui.att_c_label.setText("")
            self.nur_report3.ui.att_d_label.setText("")
            self.nur_report3.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.nur_report3.ui.att_a_label.setText("")
            self.nur_report3.ui.att_b_label.setText("")
            self.nur_report3.ui.att_c_label.setText("v")
            self.nur_report3.ui.att_d_label.setText("")
            self.nur_report3.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.nur_report3.ui.att_a_label.setText("")
            self.nur_report3.ui.att_b_label.setText("")
            self.nur_report3.ui.att_c_label.setText("")
            self.nur_report3.ui.att_d_label.setText("v")
            self.nur_report3.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.nur_report3.ui.att_a_label.setText("")
            self.nur_report3.ui.att_b_label.setText("")
            self.nur_report3.ui.att_c_label.setText("")
            self.nur_report3.ui.att_d_label.setText("")
            self.nur_report3.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.nur_report3.ui.con_a_label.setText("v")
            self.nur_report3.ui.con_b_label.setText("")
            self.nur_report3.ui.con_c_label.setText("")
            self.nur_report3.ui.con_d_label.setText("")
            self.nur_report3.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.nur_report3.ui.con_a_label.setText("")
            self.nur_report3.ui.con_b_label.setText("v")
            self.nur_report3.ui.con_c_label.setText("")
            self.nur_report3.ui.con_d_label.setText("")
            self.nur_report3.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.nur_report3.ui.con_a_label.setText("")
            self.nur_report3.ui.con_b_label.setText("")
            self.nur_report3.ui.con_c_label.setText("v")
            self.nur_report3.ui.con_d_label.setText("")
            self.nur_report3.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.nur_report3.ui.con_a_label.setText("")
            self.nur_report3.ui.con_b_label.setText("")
            self.nur_report3.ui.con_c_label.setText("")
            self.nur_report3.ui.con_d_label.setText("v")
            self.nur_report3.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.nur_report3.ui.con_a_label.setText("")
            self.nur_report3.ui.con_b_label.setText("")
            self.nur_report3.ui.con_c_label.setText("")
            self.nur_report3.ui.con_d_label.setText("")
            self.nur_report3.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.nur_report3.ui.neat_a_label.setText("v")
            self.nur_report3.ui.neat_b_label.setText("")
            self.nur_report3.ui.neat_c_label.setText("")
            self.nur_report3.ui.neat_d_label.setText("")
            self.nur_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.nur_report3.ui.neat_a_label.setText("")
            self.nur_report3.ui.neat_b_label.setText("v")
            self.nur_report3.ui.neat_c_label.setText("")
            self.nur_report3.ui.neat_d_label.setText("")
            self.nur_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.nur_report3.ui.neat_a_label.setText("")
            self.nur_report3.ui.neat_b_label.setText("v")
            self.nur_report3.ui.neat_c_label.setText("")
            self.nur_report3.ui.neat_d_label.setText("")
            self.nur_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.nur_report3.ui.neat_a_label.setText("")
            self.nur_report3.ui.neat_b_label.setText("")
            self.nur_report3.ui.neat_c_label.setText("v")
            self.nur_report3.ui.neat_d_label.setText("")
            self.nur_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.nur_report3.ui.neat_a_label.setText("")
            self.nur_report3.ui.neat_b_label.setText("")
            self.nur_report3.ui.neat_c_label.setText("")
            self.nur_report3.ui.neat_d_label.setText("v")
            self.nur_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.nur_report3.ui.neat_a_label.setText("")
            self.nur_report3.ui.neat_b_label.setText("")
            self.nur_report3.ui.neat_c_label.setText("")
            self.nur_report3.ui.neat_d_label.setText("")
            self.nur_report3.ui.neat_e_label.setText("v")


    def printReport3(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.nur_report3.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()


class NurReport3(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NurReport3rdForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    nur_scores_record = NurScoresRecord()
    nur_scores_record.show()
    sys.exit(app.exec_())
