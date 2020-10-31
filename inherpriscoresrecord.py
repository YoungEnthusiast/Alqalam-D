import sys
from PyQt5 import QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QDateTime, QByteArray
from prireport import Ui_PriReportForm
from prireport2nd import Ui_PriReport2ndForm
from prireport3rd import Ui_PriReport3rdForm

from priscoresrecord import Ui_PriScoreRecForm
from priscoresrecord2nd import Ui_PriScoreRec2ndForm
from priscoresrecord3rd import Ui_PriScoreRec3rdForm
from priscoreslist import Ui_PriScoreForm
from priscoreslist2nd import Ui_PriScore2ndForm
from priscoreslist3rd import Ui_PriScore3rdForm

import sqlite3
from sqlite3 import Error


class PriScoresRecord(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PriScoreRecForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic1_score_btn.clicked.connect(self.saveArabic1Scores)
        self.ui.arabic2_score_btn.clicked.connect(self.saveArabic2Scores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.comp_score_btn.clicked.connect(self.saveCompScores)
        self.ui.bas_sc_score_btn.clicked.connect(self.saveBasScScores)
        self.ui.religion_score_btn.clicked.connect(self.saveReligionScores)
        self.ui.civic_score_btn.clicked.connect(self.saveCivicScores)
        self.ui.verbal_score_btn.clicked.connect(self.saveVerbalScores)
        self.ui.quant_score_btn.clicked.connect(self.saveQuantScores)
        self.ui.handwriting_score_btn.clicked.connect(self.saveHandwiritingScores)
        self.ui.french_score_btn.clicked.connect(self.saveFrenchScores)
        self.ui.jolly_score_btn.clicked.connect(self.saveJollyScores)

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

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no,  ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabic1Scores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic1_c1 = self.ui.arabic1_c1_spin.value()
        arabic1_c2 = self.ui.arabic1_c2_spin.value()
        arabic1_ass = self.ui.arabic1_ass_spin.value()
        arabic1_exam = self.ui.arabic1_exam_spin.value()
        arabic1_total = arabic1_c1 + arabic1_c2 + arabic1_ass + arabic1_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic1_c1 == 0 and arabic1_c2 == 0 and arabic1_ass == 0 and arabic1_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, arabic1_c1 = ?, arabic1_c2 = ?, arabic1_ass = ?, arabic1_exam = ?, arabic1_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabic2Scores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic2_c1 = self.ui.arabic2_c1_spin.value()
        arabic2_c2 = self.ui.arabic2_c2_spin.value()
        arabic2_ass = self.ui.arabic2_ass_spin.value()
        arabic2_exam = self.ui.arabic2_exam_spin.value()
        arabic2_total = arabic2_c1 + arabic2_c2 + arabic2_ass + arabic2_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic2_c1 == 0 and arabic2_c2 == 0 and arabic2_ass == 0 and arabic2_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, arabic2_c1 = ?, arabic2_c2 = ?, arabic2_ass = ?, arabic2_exam = ?, arabic2_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveCompScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        comp_c1 = self.ui.comp_c1_spin.value()
        comp_c2 = self.ui.comp_c2_spin.value()
        comp_ass = self.ui.comp_ass_spin.value()
        comp_exam = self.ui.comp_exam_spin.value()
        comp_total = comp_c1 + comp_c2 + comp_ass + comp_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if comp_c1 == 0 and comp_c2 == 0 and comp_ass == 0 and comp_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, comp_c1 = ?, comp_c2 = ?, comp_ass = ?, comp_exam = ?, comp_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveBasScScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        bas_sc_c1 = self.ui.bas_sc_c1_spin.value()
        bas_sc_c2 = self.ui.bas_sc_c2_spin.value()
        bas_sc_ass = self.ui.bas_sc_ass_spin.value()
        bas_sc_exam = self.ui.bas_sc_exam_spin.value()
        bas_sc_total = bas_sc_c1 + bas_sc_c2 + bas_sc_ass + bas_sc_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if bas_sc_c1 == 0 and bas_sc_c2 == 0 and bas_sc_ass == 0 and bas_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, bas_sc_c1 = ?, bas_sc_c2 = ?, bas_sc_ass = ?, bas_sc_exam = ?, bas_sc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveReligionScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        religion_c1 = self.ui.religion_c1_spin.value()
        religion_c2 = self.ui.religion_c2_spin.value()
        religion_ass = self.ui.religion_ass_spin.value()
        religion_exam = self.ui.religion_exam_spin.value()
        religion_total = religion_c1 + religion_c2 + religion_ass + religion_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if religion_c1 == 0 and religion_c2 == 0 and religion_ass == 0 and religion_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, religion_c1 = ?, religion_c2 = ?, religion_ass = ?, religion_exam = ?, religion_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveCivicScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        civic_c1 = self.ui.civic_c1_spin.value()
        civic_c2 = self.ui.civic_c2_spin.value()
        civic_ass = self.ui.civic_ass_spin.value()
        civic_exam = self.ui.civic_exam_spin.value()
        civic_total = civic_c1 + civic_c2 + civic_ass + civic_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if civic_c1 == 0 and civic_c2 == 0 and civic_ass == 0 and civic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, civic_c1 = ?, civic_c2 = ?, civic_ass = ?, civic_exam = ?, civic_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveVerbalScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        verbal_c1 = self.ui.verbal_c1_spin.value()
        verbal_c2 = self.ui.verbal_c2_spin.value()
        verbal_ass = self.ui.verbal_ass_spin.value()
        verbal_exam = self.ui.verbal_exam_spin.value()
        verbal_total = verbal_c1 + verbal_c2 + verbal_ass + verbal_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if verbal_c1 == 0 and verbal_c2 == 0 and verbal_ass == 0 and verbal_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, verbal_c1 = ?, verbal_c2 = ?, verbal_ass = ?, verbal_exam = ?, verbal_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveQuantScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        quant_c1 = self.ui.quant_c1_spin.value()
        quant_c2 = self.ui.quant_c2_spin.value()
        quant_ass = self.ui.quant_ass_spin.value()
        quant_exam = self.ui.quant_exam_spin.value()
        quant_total = quant_c1 + quant_c2 + quant_ass + quant_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if quant_c1 == 0 and quant_c2 == 0 and quant_ass == 0 and quant_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, quant_c1 = ?, quant_c2 = ?, quant_ass = ?, quant_exam = ?, quant_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if handwriting_c1 == 0 and handwriting_c2 == 0 and handwriting_ass == 0 and handwriting_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, handwriting_c1 = ?, handwriting_c2 = ?, handwriting_ass = ?, handwriting_exam = ?, handwriting_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveFrenchScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        french_c1 = self.ui.french_c1_spin.value()
        french_c2 = self.ui.french_c2_spin.value()
        french_ass = self.ui.french_ass_spin.value()
        french_exam = self.ui.french_exam_spin.value()
        french_total = french_c1 + french_c2 + french_ass + french_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if french_c1 == 0 and french_c2 == 0 and french_ass == 0 and french_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, french_c1, french_c2, french_ass, french_exam, french_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, french_c1 = ?, french_c2 = ?, french_ass = ?, french_exam = ?, french_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveJollyScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        jolly_c1 = self.ui.jolly_c1_spin.value()
        jolly_c2 = self.ui.jolly_c2_spin.value()
        jolly_ass = self.ui.jolly_ass_spin.value()
        jolly_exam = self.ui.jolly_exam_spin.value()
        jolly_total = jolly_c1 + jolly_c2 + jolly_ass + jolly_exam

        cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if jolly_c1 == 0 and jolly_c2 == 0 and jolly_ass == 0 and jolly_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_first(stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_first SET stud_no = ?, jolly_c1 = ?, jolly_c2 = ?, jolly_ass = ?, jolly_exam = ?, jolly_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total, stud_no,))
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
            cmd1 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42]+ row[47] + row[52] + row[57] + row[62] + row[67] + row[72] + row[77]
            avg = round((all_total/1500)*100, 4)
            cmd2 = "UPDATE t_pri_scores_first SET stud_no = ?, all_total = ?, avg = ?  WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no, all_total, avg, stud_no,))
            con.commit()
            QMessageBox.information(self, "Computing Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Computing Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "Computing Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()


class PriScoresView(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PriScoreForm()
        self.ui.setupUi(self)

        self.pri_report = PriReport()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()


        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generatePriReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)


    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_pri_scores_first ORDER BY score_class')
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
        cmd = "SELECT * FROM t_pri_scores_first ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_pri_scores_first WHERE score_class = ? ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_pri_scores_first WHERE score_class = ? ORDER BY stud_no"
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
            cmd = "DELETE FROM t_pri_scores_first WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting Pupil', "WARNING: Deleting will remove all the pupil's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generatePriReport(self):
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
            self.pri_report.ui.name_label.setText(row[1])
            self.pri_report.ui.class_label.setText(row[3])
            self.pri_report.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.pri_report.ui.photo_label.setPixmap(QPixmap(pixmap))

            try:
                cmd3 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.pri_report.ui.qur_c1_label.setText(str(row[3]))
                self.pri_report.ui.qur_c2_label.setText(str(row[4]))
                self.pri_report.ui.qur_ass_label.setText(str(row[5]))
                self.pri_report.ui.qur_exam_label.setText(str(row[6]))
                self.pri_report.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.pri_report.ui.qur_grade_label.setText("F")
                    self.pri_report.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.pri_report.ui.qur_grade_label.setText("D")
                    self.pri_report.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.pri_report.ui.qur_grade_label.setText("C")
                    self.pri_report.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.pri_report.ui.qur_grade_label.setText("B")
                    self.pri_report.ui.qur_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.qur_grade_label.setText("A")
                    self.pri_report.ui.qur_remark_label.setText("Excellent")

                self.pri_report.ui.ibadat_c1_label.setText(str(row[8]))
                self.pri_report.ui.ibadat_c2_label.setText(str(row[9]))
                self.pri_report.ui.ibadat_ass_label.setText(str(row[10]))
                self.pri_report.ui.ibadat_exam_label.setText(str(row[11]))
                self.pri_report.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.pri_report.ui.ibadat_grade_label.setText("F")
                    self.pri_report.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.pri_report.ui.ibadat_grade_label.setText("D")
                    self.pri_report.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.pri_report.ui.ibadat_grade_label.setText("C")
                    self.pri_report.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.pri_report.ui.ibadat_grade_label.setText("B")
                    self.pri_report.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.ibadat_grade_label.setText("A")
                    self.pri_report.ui.ibadat_remark_label.setText("Excellent")

                self.pri_report.ui.arabic1_c1_label.setText(str(row[13]))
                self.pri_report.ui.arabic1_c2_label.setText(str(row[14]))
                self.pri_report.ui.arabic1_ass_label.setText(str(row[15]))
                self.pri_report.ui.arabic1_exam_label.setText(str(row[16]))
                self.pri_report.ui.arabic1_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.pri_report.ui.arabic1_grade_label.setText("F")
                    self.pri_report.ui.arabic1_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.pri_report.ui.arabic1_grade_label.setText("D")
                    self.pri_report.ui.arabic1_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.pri_report.ui.arabic1_grade_label.setText("C")
                    self.pri_report.ui.arabic1_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.pri_report.ui.arabic1_grade_label.setText("B")
                    self.pri_report.ui.arabic1_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.arabic1_grade_label.setText("A")
                    self.pri_report.ui.arabic1_remark_label.setText("Excellent")

                self.pri_report.ui.arabic2_c1_label.setText(str(row[18]))
                self.pri_report.ui.arabic2_c2_label.setText(str(row[19]))
                self.pri_report.ui.arabic2_ass_label.setText(str(row[20]))
                self.pri_report.ui.arabic2_exam_label.setText(str(row[21]))
                self.pri_report.ui.arabic2_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.pri_report.ui.arabic2_grade_label.setText("F")
                    self.pri_report.ui.arabic2_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.pri_report.ui.arabic2_grade_label.setText("D")
                    self.pri_report.ui.arabic2_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.pri_report.ui.arabic2_grade_label.setText("C")
                    self.pri_report.ui.arabic2_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.pri_report.ui.arabic2_grade_label.setText("B")
                    self.pri_report.ui.arabic2_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.arabic2_grade_label.setText("A")
                    self.pri_report.ui.arabic2_remark_label.setText("Excellent")

                self.pri_report.ui.math_c1_label.setText(str(row[23]))
                self.pri_report.ui.math_c2_label.setText(str(row[24]))
                self.pri_report.ui.math_ass_label.setText(str(row[25]))
                self.pri_report.ui.math_exam_label.setText(str(row[26]))
                self.pri_report.ui.math_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.pri_report.ui.math_grade_label.setText("F")
                    self.pri_report.ui.math_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.pri_report.ui.math_grade_label.setText("D")
                    self.pri_report.ui.math_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.pri_report.ui.math_grade_label.setText("C")
                    self.pri_report.ui.math_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.pri_report.ui.math_grade_label.setText("B")
                    self.pri_report.ui.math_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.math_grade_label.setText("A")
                    self.pri_report.ui.math_remark_label.setText("Excellent")

                self.pri_report.ui.eng_c1_label.setText(str(row[28]))
                self.pri_report.ui.eng_c2_label.setText(str(row[29]))
                self.pri_report.ui.eng_ass_label.setText(str(row[30]))
                self.pri_report.ui.eng_exam_label.setText(str(row[31]))
                self.pri_report.ui.eng_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.pri_report.ui.eng_grade_label.setText("F")
                    self.pri_report.ui.eng_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.pri_report.ui.eng_grade_label.setText("D")
                    self.pri_report.ui.eng_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.pri_report.ui.eng_grade_label.setText("C")
                    self.pri_report.ui.eng_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.pri_report.ui.eng_grade_label.setText("B")
                    self.pri_report.ui.eng_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.eng_grade_label.setText("A")
                    self.pri_report.ui.eng_remark_label.setText("Excellent")

                self.pri_report.ui.comp_c1_label.setText(str(row[33]))
                self.pri_report.ui.comp_c2_label.setText(str(row[34]))
                self.pri_report.ui.comp_ass_label.setText(str(row[35]))
                self.pri_report.ui.comp_exam_label.setText(str(row[36]))
                self.pri_report.ui.comp_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.pri_report.ui.comp_grade_label.setText("F")
                    self.pri_report.ui.comp_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.pri_report.ui.comp_grade_label.setText("D")
                    self.pri_report.ui.comp_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.pri_report.ui.comp_grade_label.setText("C")
                    self.pri_report.ui.comp_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.pri_report.ui.comp_grade_label.setText("B")
                    self.pri_report.ui.comp_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.comp_grade_label.setText("A")
                    self.pri_report.ui.comp_remark_label.setText("Excellent")

                self.pri_report.ui.bas_sc_c1_label.setText(str(row[38]))
                self.pri_report.ui.bas_sc_c2_label.setText(str(row[39]))
                self.pri_report.ui.bas_sc_ass_label.setText(str(row[40]))
                self.pri_report.ui.bas_sc_exam_label.setText(str(row[41]))
                self.pri_report.ui.bas_sc_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.pri_report.ui.bas_sc_grade_label.setText("F")
                    self.pri_report.ui.bas_sc_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.pri_report.ui.bas_sc_grade_label.setText("D")
                    self.pri_report.ui.bas_sc_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.pri_report.ui.bas_sc_grade_label.setText("C")
                    self.pri_report.ui.bas_sc_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.pri_report.ui.bas_sc_grade_label.setText("B")
                    self.pri_report.ui.bas_sc_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.bas_sc_grade_label.setText("A")
                    self.pri_report.ui.bas_sc_remark_label.setText("Excellent")

                self.pri_report.ui.religion_c1_label.setText(str(row[43]))
                self.pri_report.ui.religion_c2_label.setText(str(row[44]))
                self.pri_report.ui.religion_ass_label.setText(str(row[45]))
                self.pri_report.ui.religion_exam_label.setText(str(row[46]))
                self.pri_report.ui.religion_total_label.setText(str(row[47]))

                if row[47] < 40:
                    self.pri_report.ui.religion_grade_label.setText("F")
                    self.pri_report.ui.religion_remark_label.setText("Fail")
                elif row[47] >= 40 and row[47] < 50:
                    self.pri_report.ui.religion_grade_label.setText("D")
                    self.pri_report.ui.religion_remark_label.setText("Pass")
                elif row[47] >= 50 and row[47] < 60:
                    self.pri_report.ui.religion_grade_label.setText("C")
                    self.pri_report.ui.religion_remark_label.setText("Good")
                elif row[47] >= 60 and row[47] < 70:
                    self.pri_report.ui.religion_grade_label.setText("B")
                    self.pri_report.ui.religion_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.religion_grade_label.setText("A")
                    self.pri_report.ui.religion_remark_label.setText("Excellent")

                self.pri_report.ui.civic_c1_label.setText(str(row[48]))
                self.pri_report.ui.civic_c2_label.setText(str(row[49]))
                self.pri_report.ui.civic_ass_label.setText(str(row[50]))
                self.pri_report.ui.civic_exam_label.setText(str(row[51]))
                self.pri_report.ui.civic_total_label.setText(str(row[52]))

                if row[52] < 40:
                    self.pri_report.ui.civic_grade_label.setText("F")
                    self.pri_report.ui.civic_remark_label.setText("Fail")
                elif row[52] >= 40 and row[52] < 50:
                    self.pri_report.ui.civic_grade_label.setText("D")
                    self.pri_report.ui.civic_remark_label.setText("Pass")
                elif row[52] >= 50 and row[52] < 60:
                    self.pri_report.ui.civic_grade_label.setText("C")
                    self.pri_report.ui.civic_remark_label.setText("Good")
                elif row[52] >= 60 and row[52] < 70:
                    self.pri_report.ui.civic_grade_label.setText("B")
                    self.pri_report.ui.civic_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.civic_grade_label.setText("A")
                    self.pri_report.ui.civic_remark_label.setText("Excellent")

                self.pri_report.ui.verbal_c1_label.setText(str(row[53]))
                self.pri_report.ui.verbal_c2_label.setText(str(row[54]))
                self.pri_report.ui.verbal_ass_label.setText(str(row[55]))
                self.pri_report.ui.verbal_exam_label.setText(str(row[56]))
                self.pri_report.ui.verbal_total_label.setText(str(row[57]))

                if row[57] < 40:
                    self.pri_report.ui.verbal_grade_label.setText("F")
                    self.pri_report.ui.verbal_remark_label.setText("Fail")
                elif row[57] >= 40 and row[57] < 50:
                    self.pri_report.ui.verbal_grade_label.setText("D")
                    self.pri_report.ui.verbal_remark_label.setText("Pass")
                elif row[57] >= 50 and row[57] < 60:
                    self.pri_report.ui.verbal_grade_label.setText("C")
                    self.pri_report.ui.verbal_remark_label.setText("Good")
                elif row[57] >= 60 and row[57] < 70:
                    self.pri_report.ui.verbal_grade_label.setText("B")
                    self.pri_report.ui.verbal_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.verbal_grade_label.setText("A")
                    self.pri_report.ui.verbal_remark_label.setText("Excellent")

                self.pri_report.ui.quant_c1_label.setText(str(row[58]))
                self.pri_report.ui.quant_c2_label.setText(str(row[59]))
                self.pri_report.ui.quant_ass_label.setText(str(row[60]))
                self.pri_report.ui.quant_exam_label.setText(str(row[61]))
                self.pri_report.ui.quant_total_label.setText(str(row[62]))

                if row[62] < 40:
                    self.pri_report.ui.quant_grade_label.setText("F")
                    self.pri_report.ui.quant_remark_label.setText("Fail")
                elif row[62] >= 40 and row[62] < 50:
                    self.pri_report.ui.quant_grade_label.setText("D")
                    self.pri_report.ui.quant_remark_label.setText("Pass")
                elif row[62] >= 50 and row[62] < 60:
                    self.pri_report.ui.quant_grade_label.setText("C")
                    self.pri_report.ui.quant_remark_label.setText("Good")
                elif row[62] >= 60 and row[62] < 70:
                    self.pri_report.ui.quant_grade_label.setText("B")
                    self.pri_report.ui.quant_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.quant_grade_label.setText("A")
                    self.pri_report.ui.quant_remark_label.setText("Excellent")

                self.pri_report.ui.handwriting_c1_label.setText(str(row[63]))
                self.pri_report.ui.handwriting_c2_label.setText(str(row[64]))
                self.pri_report.ui.handwriting_ass_label.setText(str(row[65]))
                self.pri_report.ui.handwriting_exam_label.setText(str(row[66]))
                self.pri_report.ui.handwriting_total_label.setText(str(row[67]))

                if row[67] < 40:
                    self.pri_report.ui.handwriting_grade_label.setText("F")
                    self.pri_report.ui.handwriting_remark_label.setText("Fail")
                elif row[67] >= 40 and row[67] < 50:
                    self.pri_report.ui.handwriting_grade_label.setText("D")
                    self.pri_report.ui.handwriting_remark_label.setText("Pass")
                elif row[67] >= 50 and row[67] < 60:
                    self.pri_report.ui.handwriting_grade_label.setText("C")
                    self.pri_report.ui.handwriting_remark_label.setText("Good")
                elif row[67] >= 60 and row[67] < 70:
                    self.pri_report.ui.handwriting_grade_label.setText("B")
                    self.pri_report.ui.handwriting_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.handwriting_grade_label.setText("A")
                    self.pri_report.ui.handwriting_remark_label.setText("Excellent")

                self.pri_report.ui.french_c1_label.setText(str(row[68]))
                self.pri_report.ui.french_c2_label.setText(str(row[69]))
                self.pri_report.ui.french_ass_label.setText(str(row[70]))
                self.pri_report.ui.french_exam_label.setText(str(row[71]))
                self.pri_report.ui.french_total_label.setText(str(row[72]))

                if row[72] < 40:
                    self.pri_report.ui.french_grade_label.setText("F")
                    self.pri_report.ui.french_remark_label.setText("Fail")
                elif row[72] >= 40 and row[72] < 50:
                    self.pri_report.ui.french_grade_label.setText("D")
                    self.pri_report.ui.french_remark_label.setText("Pass")
                elif row[72] >= 50 and row[72] < 60:
                    self.pri_report.ui.french_grade_label.setText("C")
                    self.pri_report.ui.french_remark_label.setText("Good")
                elif row[72] >= 60 and row[72] < 70:
                    self.pri_report.ui.french_grade_label.setText("B")
                    self.pri_report.ui.french_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.french_grade_label.setText("A")
                    self.pri_report.ui.french_remark_label.setText("Excellent")

                self.pri_report.ui.jolly_c1_label.setText(str(row[73]))
                self.pri_report.ui.jolly_c2_label.setText(str(row[74]))
                self.pri_report.ui.jolly_ass_label.setText(str(row[75]))
                self.pri_report.ui.jolly_exam_label.setText(str(row[76]))
                self.pri_report.ui.jolly_total_label.setText(str(row[77]))

                if row[77] < 40:
                    self.pri_report.ui.jolly_grade_label.setText("F")
                    self.pri_report.ui.jolly_remark_label.setText("Fail")
                elif row[77] >= 40 and row[77] < 50:
                    self.pri_report.ui.jolly_grade_label.setText("D")
                    self.pri_report.ui.jolly_remark_label.setText("Pass")
                elif row[77] >= 50 and row[77] < 60:
                    self.pri_report.ui.jolly_grade_label.setText("C")
                    self.pri_report.ui.jolly_remark_label.setText("Good")
                elif row[77] >= 60 and row[77] < 70:
                    self.pri_report.ui.jolly_grade_label.setText("B")
                    self.pri_report.ui.jolly_remark_label.setText("Very Good")
                else:
                    self.pri_report.ui.jolly_grade_label.setText("A")
                    self.pri_report.ui.jolly_remark_label.setText("Excellent")

                self.pri_report.ui.total_scores_label.setText(str(row[78]))
                self.pri_report.ui.avg_label.setText(str(row[79]))

                if row[79] < 40:
                    self.pri_report.ui.master_com_label.setText("Bad result. Be careful.")
                    self.pri_report.ui.head_com_label.setText("Bad result.")
                elif row[79] >= 40 and row[79] < 50:
                    self.pri_report.ui.master_com_label.setText("Weak result. Work hard.")
                    self.pri_report.ui.head_com_label.setText("Weak result.")
                elif row[79] >= 50 and row[79] < 60:
                    self.pri_report.ui.master_com_label.setText("Fair result. Work hard.")
                    self.pri_report.ui.head_com_label.setText("Fair result.")
                elif row[79] >= 60 and row[79] < 70:
                    self.pri_report.ui.master_com_label.setText("Good result. Put more effort.")
                    self.pri_report.ui.head_com_label.setText("Good result.")
                else:
                    self.pri_report.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.pri_report.ui.head_com_label.setText("Excellent result.")

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.pri_report.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.pri_report.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.pri_report.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.pri_report.ui.fees_label.setText(row[4])

                cmd8 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd8)
                row = cur.fetchone()
                self.pri_report.ui.session_label.setText(row[2])

                if self.ui.att_a_radio.isChecked() == False and self.ui.att_b_radio.isChecked() == False and self.ui.att_c_radio.isChecked() == False and self.ui.att_d_radio.isChecked() == False and self.ui.att_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grade in attendance", QMessageBox.Ok)

                elif self.ui.con_a_radio.isChecked() == False and self.ui.con_b_radio.isChecked() == False and self.ui.con_c_radio.isChecked() == False and self.ui.con_d_radio.isChecked() == False and self.ui.con_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in conduct", QMessageBox.Ok)

                elif self.ui.neat_a_radio.isChecked() == False and self.ui.neat_b_radio.isChecked() == False and self.ui.neat_c_radio.isChecked() == False and self.ui.neat_d_radio.isChecked() == False and self.ui.neat_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select pupil's grades in neatness", QMessageBox.Ok)
                else:
                    self.printReport()
            except Error:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)
            except TypeError:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all pupil's scores have been recorded in all subjects", QMessageBox.Ok)

    def displayRadios(self):
        if self.ui.att_a_radio.isChecked():
            self.pri_report.ui.att_a_label.setText("v")
            self.pri_report.ui.att_b_label.setText("")
            self.pri_report.ui.att_c_label.setText("")
            self.pri_report.ui.att_d_label.setText("")
            self.pri_report.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.pri_report.ui.att_a_label.setText("")
            self.pri_report.ui.att_b_label.setText("v")
            self.pri_report.ui.att_c_label.setText("")
            self.pri_report.ui.att_d_label.setText("")
            self.pri_report.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.pri_report.ui.att_a_label.setText("")
            self.pri_report.ui.att_b_label.setText("")
            self.pri_report.ui.att_c_label.setText("v")
            self.pri_report.ui.att_d_label.setText("")
            self.pri_report.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.pri_report.ui.att_a_label.setText("")
            self.pri_report.ui.att_b_label.setText("")
            self.pri_report.ui.att_c_label.setText("")
            self.pri_report.ui.att_d_label.setText("v")
            self.pri_report.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.pri_report.ui.att_a_label.setText("")
            self.pri_report.ui.att_b_label.setText("")
            self.pri_report.ui.att_c_label.setText("")
            self.pri_report.ui.att_d_label.setText("")
            self.pri_report.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.pri_report.ui.con_a_label.setText("v")
            self.pri_report.ui.con_b_label.setText("")
            self.pri_report.ui.con_c_label.setText("")
            self.pri_report.ui.con_d_label.setText("")
            self.pri_report.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.pri_report.ui.con_a_label.setText("")
            self.pri_report.ui.con_b_label.setText("v")
            self.pri_report.ui.con_c_label.setText("")
            self.pri_report.ui.con_d_label.setText("")
            self.pri_report.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.pri_report.ui.con_a_label.setText("")
            self.pri_report.ui.con_b_label.setText("")
            self.pri_report.ui.con_c_label.setText("v")
            self.pri_report.ui.con_d_label.setText("")
            self.pri_report.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.pri_report.ui.con_a_label.setText("")
            self.pri_report.ui.con_b_label.setText("")
            self.pri_report.ui.con_c_label.setText("")
            self.pri_report.ui.con_d_label.setText("v")
            self.pri_report.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.pri_report.ui.con_a_label.setText("")
            self.pri_report.ui.con_b_label.setText("")
            self.pri_report.ui.con_c_label.setText("")
            self.pri_report.ui.con_d_label.setText("")
            self.pri_report.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.pri_report.ui.neat_a_label.setText("v")
            self.pri_report.ui.neat_b_label.setText("")
            self.pri_report.ui.neat_c_label.setText("")
            self.pri_report.ui.neat_d_label.setText("")
            self.pri_report.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.pri_report.ui.neat_a_label.setText("")
            self.pri_report.ui.neat_b_label.setText("v")
            self.pri_report.ui.neat_c_label.setText("")
            self.pri_report.ui.neat_d_label.setText("")
            self.pri_report.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.pri_report.ui.neat_a_label.setText("")
            self.pri_report.ui.neat_b_label.setText("v")
            self.pri_report.ui.neat_c_label.setText("")
            self.pri_report.ui.neat_d_label.setText("")
            self.pri_report.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.pri_report.ui.neat_a_label.setText("")
            self.pri_report.ui.neat_b_label.setText("")
            self.pri_report.ui.neat_c_label.setText("v")
            self.pri_report.ui.neat_d_label.setText("")
            self.pri_report.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.pri_report.ui.neat_a_label.setText("")
            self.pri_report.ui.neat_b_label.setText("")
            self.pri_report.ui.neat_c_label.setText("")
            self.pri_report.ui.neat_d_label.setText("v")
            self.pri_report.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.pri_report.ui.neat_a_label.setText("")
            self.pri_report.ui.neat_b_label.setText("")
            self.pri_report.ui.neat_c_label.setText("")
            self.pri_report.ui.neat_d_label.setText("")
            self.pri_report.ui.neat_e_label.setText("v")


    def printReport(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.pri_report.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

class PriReport(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PriReportForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())


class PriScoresRecord2(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PriScoreRec2ndForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic1_score_btn.clicked.connect(self.saveArabic1Scores)
        self.ui.arabic2_score_btn.clicked.connect(self.saveArabic2Scores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.comp_score_btn.clicked.connect(self.saveCompScores)
        self.ui.bas_sc_score_btn.clicked.connect(self.saveBasScScores)
        self.ui.religion_score_btn.clicked.connect(self.saveReligionScores)
        self.ui.civic_score_btn.clicked.connect(self.saveCivicScores)
        self.ui.verbal_score_btn.clicked.connect(self.saveVerbalScores)
        self.ui.quant_score_btn.clicked.connect(self.saveQuantScores)
        self.ui.handwriting_score_btn.clicked.connect(self.saveHandwiritingScores)
        self.ui.french_score_btn.clicked.connect(self.saveFrenchScores)
        self.ui.jolly_score_btn.clicked.connect(self.saveJollyScores)

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

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no,  ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabic1Scores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic1_c1 = self.ui.arabic1_c1_spin.value()
        arabic1_c2 = self.ui.arabic1_c2_spin.value()
        arabic1_ass = self.ui.arabic1_ass_spin.value()
        arabic1_exam = self.ui.arabic1_exam_spin.value()
        arabic1_total = arabic1_c1 + arabic1_c2 + arabic1_ass + arabic1_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic1_c1 == 0 and arabic1_c2 == 0 and arabic1_ass == 0 and arabic1_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, arabic1_c1 = ?, arabic1_c2 = ?, arabic1_ass = ?, arabic1_exam = ?, arabic1_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabic2Scores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic2_c1 = self.ui.arabic2_c1_spin.value()
        arabic2_c2 = self.ui.arabic2_c2_spin.value()
        arabic2_ass = self.ui.arabic2_ass_spin.value()
        arabic2_exam = self.ui.arabic2_exam_spin.value()
        arabic2_total = arabic2_c1 + arabic2_c2 + arabic2_ass + arabic2_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic2_c1 == 0 and arabic2_c2 == 0 and arabic2_ass == 0 and arabic2_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, arabic2_c1 = ?, arabic2_c2 = ?, arabic2_ass = ?, arabic2_exam = ?, arabic2_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveCompScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        comp_c1 = self.ui.comp_c1_spin.value()
        comp_c2 = self.ui.comp_c2_spin.value()
        comp_ass = self.ui.comp_ass_spin.value()
        comp_exam = self.ui.comp_exam_spin.value()
        comp_total = comp_c1 + comp_c2 + comp_ass + comp_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if comp_c1 == 0 and comp_c2 == 0 and comp_ass == 0 and comp_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, comp_c1 = ?, comp_c2 = ?, comp_ass = ?, comp_exam = ?, comp_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveBasScScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        bas_sc_c1 = self.ui.bas_sc_c1_spin.value()
        bas_sc_c2 = self.ui.bas_sc_c2_spin.value()
        bas_sc_ass = self.ui.bas_sc_ass_spin.value()
        bas_sc_exam = self.ui.bas_sc_exam_spin.value()
        bas_sc_total = bas_sc_c1 + bas_sc_c2 + bas_sc_ass + bas_sc_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if bas_sc_c1 == 0 and bas_sc_c2 == 0 and bas_sc_ass == 0 and bas_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, bas_sc_c1 = ?, bas_sc_c2 = ?, bas_sc_ass = ?, bas_sc_exam = ?, bas_sc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveReligionScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        religion_c1 = self.ui.religion_c1_spin.value()
        religion_c2 = self.ui.religion_c2_spin.value()
        religion_ass = self.ui.religion_ass_spin.value()
        religion_exam = self.ui.religion_exam_spin.value()
        religion_total = religion_c1 + religion_c2 + religion_ass + religion_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if religion_c1 == 0 and religion_c2 == 0 and religion_ass == 0 and religion_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, religion_c1 = ?, religion_c2 = ?, religion_ass = ?, religion_exam = ?, religion_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveCivicScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        civic_c1 = self.ui.civic_c1_spin.value()
        civic_c2 = self.ui.civic_c2_spin.value()
        civic_ass = self.ui.civic_ass_spin.value()
        civic_exam = self.ui.civic_exam_spin.value()
        civic_total = civic_c1 + civic_c2 + civic_ass + civic_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if civic_c1 == 0 and civic_c2 == 0 and civic_ass == 0 and civic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, civic_c1 = ?, civic_c2 = ?, civic_ass = ?, civic_exam = ?, civic_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveVerbalScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        verbal_c1 = self.ui.verbal_c1_spin.value()
        verbal_c2 = self.ui.verbal_c2_spin.value()
        verbal_ass = self.ui.verbal_ass_spin.value()
        verbal_exam = self.ui.verbal_exam_spin.value()
        verbal_total = verbal_c1 + verbal_c2 + verbal_ass + verbal_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if verbal_c1 == 0 and verbal_c2 == 0 and verbal_ass == 0 and verbal_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, verbal_c1 = ?, verbal_c2 = ?, verbal_ass = ?, verbal_exam = ?, verbal_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveQuantScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        quant_c1 = self.ui.quant_c1_spin.value()
        quant_c2 = self.ui.quant_c2_spin.value()
        quant_ass = self.ui.quant_ass_spin.value()
        quant_exam = self.ui.quant_exam_spin.value()
        quant_total = quant_c1 + quant_c2 + quant_ass + quant_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if quant_c1 == 0 and quant_c2 == 0 and quant_ass == 0 and quant_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, quant_c1 = ?, quant_c2 = ?, quant_ass = ?, quant_exam = ?, quant_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if handwriting_c1 == 0 and handwriting_c2 == 0 and handwriting_ass == 0 and handwriting_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, handwriting_c1 = ?, handwriting_c2 = ?, handwriting_ass = ?, handwriting_exam = ?, handwriting_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveFrenchScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        french_c1 = self.ui.french_c1_spin.value()
        french_c2 = self.ui.french_c2_spin.value()
        french_ass = self.ui.french_ass_spin.value()
        french_exam = self.ui.french_exam_spin.value()
        french_total = french_c1 + french_c2 + french_ass + french_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if french_c1 == 0 and french_c2 == 0 and french_ass == 0 and french_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, french_c1, french_c2, french_ass, french_exam, french_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, french_c1 = ?, french_c2 = ?, french_ass = ?, french_exam = ?, french_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveJollyScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        jolly_c1 = self.ui.jolly_c1_spin.value()
        jolly_c2 = self.ui.jolly_c2_spin.value()
        jolly_ass = self.ui.jolly_ass_spin.value()
        jolly_exam = self.ui.jolly_exam_spin.value()
        jolly_total = jolly_c1 + jolly_c2 + jolly_ass + jolly_exam

        cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if jolly_c1 == 0 and jolly_c2 == 0 and jolly_ass == 0 and jolly_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_second(stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, jolly_c1 = ?, jolly_c2 = ?, jolly_ass = ?, jolly_exam = ?, jolly_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total, stud_no,))
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
            cmd1 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42]+ row[47] + row[52] + row[57] + row[62] + row[67] + row[72] + row[77]
            avg = round((all_total/1500)*100, 4)

            cmd2 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum = all_total
                avg_cum = round((total_cum/1500)*100, 4)
            elif row[78] == None:
                total_cum = all_total
                avg_cum = round((total_cum/1500)*100, 4)
            else:
                total_cum = row[78] + all_total
                avg_cum = round((total_cum/3000)*100, 4)
            cmd3 = "UPDATE t_pri_scores_second SET stud_no = ?, all_total = ?, avg = ?, total_cum = ?, avg_cum = ?  WHERE stud_no = ?"
            cur.execute(cmd3, (stud_no, all_total, avg, total_cum, avg_cum, stud_no,))
            con.commit()

            QMessageBox.information(self, "Computing Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Computing Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "Computing Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()


class PriScoresView2(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PriScore2ndForm()
        self.ui.setupUi(self)

        self.pri_report2 = PriReport2()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()


        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generatePriReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_pri_scores_second ORDER BY score_class')
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
        cmd = "SELECT * FROM t_pri_scores_second ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_pri_scores_second WHERE score_class = ? ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_pri_scores_second WHERE score_class = ? ORDER BY stud_no"
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
            cmd = "DELETE FROM t_pri_scores_second WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting Pupil', "WARNING: Deleting will remove all the pupil's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generatePriReport(self):
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

            self.pri_report2.ui.name_label.setText(row[1])
            self.pri_report2.ui.class_label.setText(row[3])
            self.pri_report2.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.pri_report2.ui.photo_label.setPixmap(QPixmap(pixmap))

            try:

                cmd3 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.pri_report2.ui.qur_c1_label.setText(str(row[3]))
                self.pri_report2.ui.qur_c2_label.setText(str(row[4]))
                self.pri_report2.ui.qur_ass_label.setText(str(row[5]))
                self.pri_report2.ui.qur_exam_label.setText(str(row[6]))
                self.pri_report2.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.pri_report2.ui.qur_grade_label.setText("F")
                    self.pri_report2.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.pri_report2.ui.qur_grade_label.setText("D")
                    self.pri_report2.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.pri_report2.ui.qur_grade_label.setText("C")
                    self.pri_report2.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.pri_report2.ui.qur_grade_label.setText("B")
                    self.pri_report2.ui.qur_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.qur_grade_label.setText("A")
                    self.pri_report2.ui.qur_remark_label.setText("Excellent")

                self.pri_report2.ui.ibadat_c1_label.setText(str(row[8]))
                self.pri_report2.ui.ibadat_c2_label.setText(str(row[9]))
                self.pri_report2.ui.ibadat_ass_label.setText(str(row[10]))
                self.pri_report2.ui.ibadat_exam_label.setText(str(row[11]))
                self.pri_report2.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.pri_report2.ui.ibadat_grade_label.setText("F")
                    self.pri_report2.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.pri_report2.ui.ibadat_grade_label.setText("D")
                    self.pri_report2.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.pri_report2.ui.ibadat_grade_label.setText("C")
                    self.pri_report2.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.pri_report2.ui.ibadat_grade_label.setText("B")
                    self.pri_report2.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.ibadat_grade_label.setText("A")
                    self.pri_report2.ui.ibadat_remark_label.setText("Excellent")

                self.pri_report2.ui.arabic1_c1_label.setText(str(row[13]))
                self.pri_report2.ui.arabic1_c2_label.setText(str(row[14]))
                self.pri_report2.ui.arabic1_ass_label.setText(str(row[15]))
                self.pri_report2.ui.arabic1_exam_label.setText(str(row[16]))
                self.pri_report2.ui.arabic1_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.pri_report2.ui.arabic1_grade_label.setText("F")
                    self.pri_report2.ui.arabic1_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.pri_report2.ui.arabic1_grade_label.setText("D")
                    self.pri_report2.ui.arabic1_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.pri_report2.ui.arabic1_grade_label.setText("C")
                    self.pri_report2.ui.arabic1_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.pri_report2.ui.arabic1_grade_label.setText("B")
                    self.pri_report2.ui.arabic1_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.arabic1_grade_label.setText("A")
                    self.pri_report2.ui.arabic1_remark_label.setText("Excellent")

                self.pri_report2.ui.arabic2_c1_label.setText(str(row[18]))
                self.pri_report2.ui.arabic2_c2_label.setText(str(row[19]))
                self.pri_report2.ui.arabic2_ass_label.setText(str(row[20]))
                self.pri_report2.ui.arabic2_exam_label.setText(str(row[21]))
                self.pri_report2.ui.arabic2_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.pri_report2.ui.arabic2_grade_label.setText("F")
                    self.pri_report2.ui.arabic2_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.pri_report2.ui.arabic2_grade_label.setText("D")
                    self.pri_report2.ui.arabic2_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.pri_report2.ui.arabic2_grade_label.setText("C")
                    self.pri_report2.ui.arabic2_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.pri_report2.ui.arabic2_grade_label.setText("B")
                    self.pri_report2.ui.arabic2_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.arabic2_grade_label.setText("A")
                    self.pri_report2.ui.arabic2_remark_label.setText("Excellent")

                self.pri_report2.ui.math_c1_label.setText(str(row[23]))
                self.pri_report2.ui.math_c2_label.setText(str(row[24]))
                self.pri_report2.ui.math_ass_label.setText(str(row[25]))
                self.pri_report2.ui.math_exam_label.setText(str(row[26]))
                self.pri_report2.ui.math_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.pri_report2.ui.math_grade_label.setText("F")
                    self.pri_report2.ui.math_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.pri_report2.ui.math_grade_label.setText("D")
                    self.pri_report2.ui.math_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.pri_report2.ui.math_grade_label.setText("C")
                    self.pri_report2.ui.math_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.pri_report2.ui.math_grade_label.setText("B")
                    self.pri_report2.ui.math_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.math_grade_label.setText("A")
                    self.pri_report2.ui.math_remark_label.setText("Excellent")

                self.pri_report2.ui.eng_c1_label.setText(str(row[28]))
                self.pri_report2.ui.eng_c2_label.setText(str(row[29]))
                self.pri_report2.ui.eng_ass_label.setText(str(row[30]))
                self.pri_report2.ui.eng_exam_label.setText(str(row[31]))
                self.pri_report2.ui.eng_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.pri_report2.ui.eng_grade_label.setText("F")
                    self.pri_report2.ui.eng_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.pri_report2.ui.eng_grade_label.setText("D")
                    self.pri_report2.ui.eng_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.pri_report2.ui.eng_grade_label.setText("C")
                    self.pri_report2.ui.eng_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.pri_report2.ui.eng_grade_label.setText("B")
                    self.pri_report2.ui.eng_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.eng_grade_label.setText("A")
                    self.pri_report2.ui.eng_remark_label.setText("Excellent")

                self.pri_report2.ui.comp_c1_label.setText(str(row[33]))
                self.pri_report2.ui.comp_c2_label.setText(str(row[34]))
                self.pri_report2.ui.comp_ass_label.setText(str(row[35]))
                self.pri_report2.ui.comp_exam_label.setText(str(row[36]))
                self.pri_report2.ui.comp_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.pri_report2.ui.comp_grade_label.setText("F")
                    self.pri_report2.ui.comp_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.pri_report2.ui.comp_grade_label.setText("D")
                    self.pri_report2.ui.comp_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.pri_report2.ui.comp_grade_label.setText("C")
                    self.pri_report2.ui.comp_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.pri_report2.ui.comp_grade_label.setText("B")
                    self.pri_report2.ui.comp_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.comp_grade_label.setText("A")
                    self.pri_report2.ui.comp_remark_label.setText("Excellent")

                self.pri_report2.ui.bas_sc_c1_label.setText(str(row[38]))
                self.pri_report2.ui.bas_sc_c2_label.setText(str(row[39]))
                self.pri_report2.ui.bas_sc_ass_label.setText(str(row[40]))
                self.pri_report2.ui.bas_sc_exam_label.setText(str(row[41]))
                self.pri_report2.ui.bas_sc_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.pri_report2.ui.bas_sc_grade_label.setText("F")
                    self.pri_report2.ui.bas_sc_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.pri_report2.ui.bas_sc_grade_label.setText("D")
                    self.pri_report2.ui.bas_sc_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.pri_report2.ui.bas_sc_grade_label.setText("C")
                    self.pri_report2.ui.bas_sc_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.pri_report2.ui.bas_sc_grade_label.setText("B")
                    self.pri_report2.ui.bas_sc_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.bas_sc_grade_label.setText("A")
                    self.pri_report2.ui.bas_sc_remark_label.setText("Excellent")

                self.pri_report2.ui.religion_c1_label.setText(str(row[43]))
                self.pri_report2.ui.religion_c2_label.setText(str(row[44]))
                self.pri_report2.ui.religion_ass_label.setText(str(row[45]))
                self.pri_report2.ui.religion_exam_label.setText(str(row[46]))
                self.pri_report2.ui.religion_total_label.setText(str(row[47]))

                if row[47] < 40:
                    self.pri_report2.ui.religion_grade_label.setText("F")
                    self.pri_report2.ui.religion_remark_label.setText("Fail")
                elif row[47] >= 40 and row[47] < 50:
                    self.pri_report2.ui.religion_grade_label.setText("D")
                    self.pri_report2.ui.religion_remark_label.setText("Pass")
                elif row[47] >= 50 and row[47] < 60:
                    self.pri_report2.ui.religion_grade_label.setText("C")
                    self.pri_report2.ui.religion_remark_label.setText("Good")
                elif row[47] >= 60 and row[47] < 70:
                    self.pri_report2.ui.religion_grade_label.setText("B")
                    self.pri_report2.ui.religion_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.religion_grade_label.setText("A")
                    self.pri_report2.ui.religion_remark_label.setText("Excellent")

                self.pri_report2.ui.civic_c1_label.setText(str(row[48]))
                self.pri_report2.ui.civic_c2_label.setText(str(row[49]))
                self.pri_report2.ui.civic_ass_label.setText(str(row[50]))
                self.pri_report2.ui.civic_exam_label.setText(str(row[51]))
                self.pri_report2.ui.civic_total_label.setText(str(row[52]))

                if row[52] < 40:
                    self.pri_report2.ui.civic_grade_label.setText("F")
                    self.pri_report2.ui.civic_remark_label.setText("Fail")
                elif row[52] >= 40 and row[52] < 50:
                    self.pri_report2.ui.civic_grade_label.setText("D")
                    self.pri_report2.ui.civic_remark_label.setText("Pass")
                elif row[52] >= 50 and row[52] < 60:
                    self.pri_report2.ui.civic_grade_label.setText("C")
                    self.pri_report2.ui.civic_remark_label.setText("Good")
                elif row[52] >= 60 and row[52] < 70:
                    self.pri_report2.ui.civic_grade_label.setText("B")
                    self.pri_report2.ui.civic_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.civic_grade_label.setText("A")
                    self.pri_report2.ui.civic_remark_label.setText("Excellent")

                self.pri_report2.ui.verbal_c1_label.setText(str(row[53]))
                self.pri_report2.ui.verbal_c2_label.setText(str(row[54]))
                self.pri_report2.ui.verbal_ass_label.setText(str(row[55]))
                self.pri_report2.ui.verbal_exam_label.setText(str(row[56]))
                self.pri_report2.ui.verbal_total_label.setText(str(row[57]))

                if row[57] < 40:
                    self.pri_report2.ui.verbal_grade_label.setText("F")
                    self.pri_report2.ui.verbal_remark_label.setText("Fail")
                elif row[57] >= 40 and row[57] < 50:
                    self.pri_report2.ui.verbal_grade_label.setText("D")
                    self.pri_report2.ui.verbal_remark_label.setText("Pass")
                elif row[57] >= 50 and row[57] < 60:
                    self.pri_report2.ui.verbal_grade_label.setText("C")
                    self.pri_report2.ui.verbal_remark_label.setText("Good")
                elif row[57] >= 60 and row[57] < 70:
                    self.pri_report2.ui.verbal_grade_label.setText("B")
                    self.pri_report2.ui.verbal_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.verbal_grade_label.setText("A")
                    self.pri_report2.ui.verbal_remark_label.setText("Excellent")

                self.pri_report2.ui.quant_c1_label.setText(str(row[58]))
                self.pri_report2.ui.quant_c2_label.setText(str(row[59]))
                self.pri_report2.ui.quant_ass_label.setText(str(row[60]))
                self.pri_report2.ui.quant_exam_label.setText(str(row[61]))
                self.pri_report2.ui.quant_total_label.setText(str(row[62]))

                if row[62] < 40:
                    self.pri_report2.ui.quant_grade_label.setText("F")
                    self.pri_report2.ui.quant_remark_label.setText("Fail")
                elif row[62] >= 40 and row[62] < 50:
                    self.pri_report2.ui.quant_grade_label.setText("D")
                    self.pri_report2.ui.quant_remark_label.setText("Pass")
                elif row[62] >= 50 and row[62] < 60:
                    self.pri_report2.ui.quant_grade_label.setText("C")
                    self.pri_report2.ui.quant_remark_label.setText("Good")
                elif row[62] >= 60 and row[62] < 70:
                    self.pri_report2.ui.quant_grade_label.setText("B")
                    self.pri_report2.ui.quant_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.quant_grade_label.setText("A")
                    self.pri_report2.ui.quant_remark_label.setText("Excellent")

                self.pri_report2.ui.handwriting_c1_label.setText(str(row[63]))
                self.pri_report2.ui.handwriting_c2_label.setText(str(row[64]))
                self.pri_report2.ui.handwriting_ass_label.setText(str(row[65]))
                self.pri_report2.ui.handwriting_exam_label.setText(str(row[66]))
                self.pri_report2.ui.handwriting_total_label.setText(str(row[67]))

                if row[67] < 40:
                    self.pri_report2.ui.handwriting_grade_label.setText("F")
                    self.pri_report2.ui.handwriting_remark_label.setText("Fail")
                elif row[67] >= 40 and row[67] < 50:
                    self.pri_report2.ui.handwriting_grade_label.setText("D")
                    self.pri_report2.ui.handwriting_remark_label.setText("Pass")
                elif row[67] >= 50 and row[67] < 60:
                    self.pri_report2.ui.handwriting_grade_label.setText("C")
                    self.pri_report2.ui.handwriting_remark_label.setText("Good")
                elif row[67] >= 60 and row[67] < 70:
                    self.pri_report2.ui.handwriting_grade_label.setText("B")
                    self.pri_report2.ui.handwriting_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.handwriting_grade_label.setText("A")
                    self.pri_report2.ui.handwriting_remark_label.setText("Excellent")

                self.pri_report2.ui.french_c1_label.setText(str(row[68]))
                self.pri_report2.ui.french_c2_label.setText(str(row[69]))
                self.pri_report2.ui.french_ass_label.setText(str(row[70]))
                self.pri_report2.ui.french_exam_label.setText(str(row[71]))
                self.pri_report2.ui.french_total_label.setText(str(row[72]))

                if row[72] < 40:
                    self.pri_report2.ui.french_grade_label.setText("F")
                    self.pri_report2.ui.french_remark_label.setText("Fail")
                elif row[72] >= 40 and row[72] < 50:
                    self.pri_report2.ui.french_grade_label.setText("D")
                    self.pri_report2.ui.french_remark_label.setText("Pass")
                elif row[72] >= 50 and row[72] < 60:
                    self.pri_report2.ui.french_grade_label.setText("C")
                    self.pri_report2.ui.french_remark_label.setText("Good")
                elif row[72] >= 60 and row[72] < 70:
                    self.pri_report2.ui.french_grade_label.setText("B")
                    self.pri_report2.ui.french_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.french_grade_label.setText("A")
                    self.pri_report2.ui.french_remark_label.setText("Excellent")

                self.pri_report2.ui.jolly_c1_label.setText(str(row[73]))
                self.pri_report2.ui.jolly_c2_label.setText(str(row[74]))
                self.pri_report2.ui.jolly_ass_label.setText(str(row[75]))
                self.pri_report2.ui.jolly_exam_label.setText(str(row[76]))
                self.pri_report2.ui.jolly_total_label.setText(str(row[77]))

                if row[77] < 40:
                    self.pri_report2.ui.jolly_grade_label.setText("F")
                    self.pri_report2.ui.jolly_remark_label.setText("Fail")
                elif row[77] >= 40 and row[77] < 50:
                    self.pri_report2.ui.jolly_grade_label.setText("D")
                    self.pri_report2.ui.jolly_remark_label.setText("Pass")
                elif row[77] >= 50 and row[77] < 60:
                    self.pri_report2.ui.jolly_grade_label.setText("C")
                    self.pri_report2.ui.jolly_remark_label.setText("Good")
                elif row[77] >= 60 and row[77] < 70:
                    self.pri_report2.ui.jolly_grade_label.setText("B")
                    self.pri_report2.ui.jolly_remark_label.setText("Very Good")
                else:
                    self.pri_report2.ui.jolly_grade_label.setText("A")
                    self.pri_report2.ui.jolly_remark_label.setText("Excellent")

                self.pri_report2.ui.total_scores2_label.setText(str(row[78]))
                self.pri_report2.ui.avg2_label.setText(str(row[79]))
                self.pri_report2.ui.total_cum_label.setText(str(row[80]))
                self.pri_report2.ui.avg_cum_label.setText(str(row[81]))

                if row[79] < 40:
                    self.pri_report2.ui.master_com_label.setText("Bad result. Be careful.")
                    self.pri_report2.ui.head_com_label.setText("Bad result.")
                elif row[79] >= 40 and row[79] < 50:
                    self.pri_report2.ui.master_com_label.setText("Weak result. Work hard.")
                    self.pri_report2.ui.head_com_label.setText("Weak result.")
                elif row[79] >= 50 and row[79] < 60:
                    self.pri_report2.ui.master_com_label.setText("Fair result. Work hard.")
                    self.pri_report2.ui.head_com_label.setText("Fair result.")
                elif row[79] >= 60 and row[79] < 70:
                    self.pri_report2.ui.master_com_label.setText("Good result. Put more effort.")
                    self.pri_report2.ui.head_com_label.setText("Good result.")
                else:
                    self.pri_report2.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.pri_report2.ui.head_com_label.setText("Excellent result.")

                cmd9 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
                cur.execute(cmd9, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.pri_report2.ui.total_scores_label.setText("None")
                    self.pri_report2.ui.avg_label.setText("None")
                elif row[78] == None and row[79] == None:
                    self.pri_report2.ui.total_scores_label.setText("None")
                    self.pri_report2.ui.avg_label.setText("None")
                else:
                    self.pri_report2.ui.total_scores_label.setText(str(row[78]))
                    self.pri_report2.ui.avg_label.setText(str(row[79]))

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.pri_report2.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.pri_report2.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.pri_report2.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.pri_report2.ui.fees_label.setText(row[4])

                cmd8 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd8)
                row = cur.fetchone()
                self.pri_report2.ui.session_label.setText(row[2])

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
            self.pri_report2.ui.att_a_label.setText("v")
            self.pri_report2.ui.att_b_label.setText("")
            self.pri_report2.ui.att_c_label.setText("")
            self.pri_report2.ui.att_d_label.setText("")
            self.pri_report2.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.pri_report2.ui.att_a_label.setText("")
            self.pri_report2.ui.att_b_label.setText("v")
            self.pri_report2.ui.att_c_label.setText("")
            self.pri_report2.ui.att_d_label.setText("")
            self.pri_report2.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.pri_report2.ui.att_a_label.setText("")
            self.pri_report2.ui.att_b_label.setText("")
            self.pri_report2.ui.att_c_label.setText("v")
            self.pri_report2.ui.att_d_label.setText("")
            self.pri_report2.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.pri_report2.ui.att_a_label.setText("")
            self.pri_report2.ui.att_b_label.setText("")
            self.pri_report2.ui.att_c_label.setText("")
            self.pri_report2.ui.att_d_label.setText("v")
            self.pri_report2.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.pri_report2.ui.att_a_label.setText("")
            self.pri_report2.ui.att_b_label.setText("")
            self.pri_report2.ui.att_c_label.setText("")
            self.pri_report2.ui.att_d_label.setText("")
            self.pri_report2.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.pri_report2.ui.con_a_label.setText("v")
            self.pri_report2.ui.con_b_label.setText("")
            self.pri_report2.ui.con_c_label.setText("")
            self.pri_report2.ui.con_d_label.setText("")
            self.pri_report2.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.pri_report2.ui.con_a_label.setText("")
            self.pri_report2.ui.con_b_label.setText("v")
            self.pri_report2.ui.con_c_label.setText("")
            self.pri_report2.ui.con_d_label.setText("")
            self.pri_report2.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.pri_report2.ui.con_a_label.setText("")
            self.pri_report2.ui.con_b_label.setText("")
            self.pri_report2.ui.con_c_label.setText("v")
            self.pri_report2.ui.con_d_label.setText("")
            self.pri_report2.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.pri_report2.ui.con_a_label.setText("")
            self.pri_report2.ui.con_b_label.setText("")
            self.pri_report2.ui.con_c_label.setText("")
            self.pri_report2.ui.con_d_label.setText("v")
            self.pri_report2.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.pri_report2.ui.con_a_label.setText("")
            self.pri_report2.ui.con_b_label.setText("")
            self.pri_report2.ui.con_c_label.setText("")
            self.pri_report2.ui.con_d_label.setText("")
            self.pri_report2.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.pri_report2.ui.neat_a_label.setText("v")
            self.pri_report2.ui.neat_b_label.setText("")
            self.pri_report2.ui.neat_c_label.setText("")
            self.pri_report2.ui.neat_d_label.setText("")
            self.pri_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.pri_report2.ui.neat_a_label.setText("")
            self.pri_report2.ui.neat_b_label.setText("v")
            self.pri_report2.ui.neat_c_label.setText("")
            self.pri_report2.ui.neat_d_label.setText("")
            self.pri_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.pri_report2.ui.neat_a_label.setText("")
            self.pri_report2.ui.neat_b_label.setText("v")
            self.pri_report2.ui.neat_c_label.setText("")
            self.pri_report2.ui.neat_d_label.setText("")
            self.pri_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.pri_report2.ui.neat_a_label.setText("")
            self.pri_report2.ui.neat_b_label.setText("")
            self.pri_report2.ui.neat_c_label.setText("v")
            self.pri_report2.ui.neat_d_label.setText("")
            self.pri_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.pri_report2.ui.neat_a_label.setText("")
            self.pri_report2.ui.neat_b_label.setText("")
            self.pri_report2.ui.neat_c_label.setText("")
            self.pri_report2.ui.neat_d_label.setText("v")
            self.pri_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.pri_report2.ui.neat_a_label.setText("")
            self.pri_report2.ui.neat_b_label.setText("")
            self.pri_report2.ui.neat_c_label.setText("")
            self.pri_report2.ui.neat_d_label.setText("")
            self.pri_report2.ui.neat_e_label.setText("v")


    def printReport2(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.pri_report2.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

class PriReport2(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PriReport2ndForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())


class PriScoresRecord3(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PriScoreRec3rdForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic1_score_btn.clicked.connect(self.saveArabic1Scores)
        self.ui.arabic2_score_btn.clicked.connect(self.saveArabic2Scores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.comp_score_btn.clicked.connect(self.saveCompScores)
        self.ui.bas_sc_score_btn.clicked.connect(self.saveBasScScores)
        self.ui.religion_score_btn.clicked.connect(self.saveReligionScores)
        self.ui.civic_score_btn.clicked.connect(self.saveCivicScores)
        self.ui.verbal_score_btn.clicked.connect(self.saveVerbalScores)
        self.ui.quant_score_btn.clicked.connect(self.saveQuantScores)
        self.ui.handwriting_score_btn.clicked.connect(self.saveHandwiritingScores)
        self.ui.french_score_btn.clicked.connect(self.saveFrenchScores)
        self.ui.jolly_score_btn.clicked.connect(self.saveJollyScores)

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

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no,  ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabic1Scores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic1_c1 = self.ui.arabic1_c1_spin.value()
        arabic1_c2 = self.ui.arabic1_c2_spin.value()
        arabic1_ass = self.ui.arabic1_ass_spin.value()
        arabic1_exam = self.ui.arabic1_exam_spin.value()
        arabic1_total = arabic1_c1 + arabic1_c2 + arabic1_ass + arabic1_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic1_c1 == 0 and arabic1_c2 == 0 and arabic1_ass == 0 and arabic1_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, arabic1_c1 = ?, arabic1_c2 = ?, arabic1_ass = ?, arabic1_exam = ?, arabic1_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveArabic2Scores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        arabic2_c1 = self.ui.arabic2_c1_spin.value()
        arabic2_c2 = self.ui.arabic2_c2_spin.value()
        arabic2_ass = self.ui.arabic2_ass_spin.value()
        arabic2_exam = self.ui.arabic2_exam_spin.value()
        arabic2_total = arabic2_c1 + arabic2_c2 + arabic2_ass + arabic2_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic2_c1 == 0 and arabic2_c2 == 0 and arabic2_ass == 0 and arabic2_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, arabic2_c1 = ?, arabic2_c2 = ?, arabic2_ass = ?, arabic2_exam = ?, arabic2_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic2_c1, arabic2_c2, arabic2_ass, arabic2_exam, arabic2_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveCompScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        comp_c1 = self.ui.comp_c1_spin.value()
        comp_c2 = self.ui.comp_c2_spin.value()
        comp_ass = self.ui.comp_ass_spin.value()
        comp_exam = self.ui.comp_exam_spin.value()
        comp_total = comp_c1 + comp_c2 + comp_ass + comp_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if comp_c1 == 0 and comp_c2 == 0 and comp_ass == 0 and comp_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, comp_c1 = ?, comp_c2 = ?, comp_ass = ?, comp_exam = ?, comp_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, comp_c1, comp_c2, comp_ass, comp_exam, comp_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveBasScScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        bas_sc_c1 = self.ui.bas_sc_c1_spin.value()
        bas_sc_c2 = self.ui.bas_sc_c2_spin.value()
        bas_sc_ass = self.ui.bas_sc_ass_spin.value()
        bas_sc_exam = self.ui.bas_sc_exam_spin.value()
        bas_sc_total = bas_sc_c1 + bas_sc_c2 + bas_sc_ass + bas_sc_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if bas_sc_c1 == 0 and bas_sc_c2 == 0 and bas_sc_ass == 0 and bas_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, bas_sc_c1 = ?, bas_sc_c2 = ?, bas_sc_ass = ?, bas_sc_exam = ?, bas_sc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveReligionScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        religion_c1 = self.ui.religion_c1_spin.value()
        religion_c2 = self.ui.religion_c2_spin.value()
        religion_ass = self.ui.religion_ass_spin.value()
        religion_exam = self.ui.religion_exam_spin.value()
        religion_total = religion_c1 + religion_c2 + religion_ass + religion_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if religion_c1 == 0 and religion_c2 == 0 and religion_ass == 0 and religion_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, religion_c1 = ?, religion_c2 = ?, religion_ass = ?, religion_exam = ?, religion_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveCivicScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        civic_c1 = self.ui.civic_c1_spin.value()
        civic_c2 = self.ui.civic_c2_spin.value()
        civic_ass = self.ui.civic_ass_spin.value()
        civic_exam = self.ui.civic_exam_spin.value()
        civic_total = civic_c1 + civic_c2 + civic_ass + civic_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if civic_c1 == 0 and civic_c2 == 0 and civic_ass == 0 and civic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, civic_c1 = ?, civic_c2 = ?, civic_ass = ?, civic_exam = ?, civic_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveVerbalScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        verbal_c1 = self.ui.verbal_c1_spin.value()
        verbal_c2 = self.ui.verbal_c2_spin.value()
        verbal_ass = self.ui.verbal_ass_spin.value()
        verbal_exam = self.ui.verbal_exam_spin.value()
        verbal_total = verbal_c1 + verbal_c2 + verbal_ass + verbal_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if verbal_c1 == 0 and verbal_c2 == 0 and verbal_ass == 0 and verbal_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, verbal_c1 = ?, verbal_c2 = ?, verbal_ass = ?, verbal_exam = ?, verbal_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, verbal_c1, verbal_c2, verbal_ass, verbal_exam, verbal_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveQuantScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        quant_c1 = self.ui.quant_c1_spin.value()
        quant_c2 = self.ui.quant_c2_spin.value()
        quant_ass = self.ui.quant_ass_spin.value()
        quant_exam = self.ui.quant_exam_spin.value()
        quant_total = quant_c1 + quant_c2 + quant_ass + quant_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if quant_c1 == 0 and quant_c2 == 0 and quant_ass == 0 and quant_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, quant_c1 = ?, quant_c2 = ?, quant_ass = ?, quant_exam = ?, quant_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, quant_c1, quant_c2, quant_ass, quant_exam, quant_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if handwriting_c1 == 0 and handwriting_c2 == 0 and handwriting_ass == 0 and handwriting_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, handwriting_c1 = ?, handwriting_c2 = ?, handwriting_ass = ?, handwriting_exam = ?, handwriting_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, handwriting_c1, handwriting_c2, handwriting_ass, handwriting_exam, handwriting_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveFrenchScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        french_c1 = self.ui.french_c1_spin.value()
        french_c2 = self.ui.french_c2_spin.value()
        french_ass = self.ui.french_ass_spin.value()
        french_exam = self.ui.french_exam_spin.value()
        french_total = french_c1 + french_c2 + french_ass + french_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if french_c1 == 0 and french_c2 == 0 and french_ass == 0 and french_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, french_c1, french_c2, french_ass, french_exam, french_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, french_c1 = ?, french_c2 = ?, french_ass = ?, french_exam = ?, french_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveJollyScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        jolly_c1 = self.ui.jolly_c1_spin.value()
        jolly_c2 = self.ui.jolly_c2_spin.value()
        jolly_ass = self.ui.jolly_ass_spin.value()
        jolly_exam = self.ui.jolly_exam_spin.value()
        jolly_total = jolly_c1 + jolly_c2 + jolly_ass + jolly_exam

        cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if jolly_c1 == 0 and jolly_c2 == 0 and jolly_ass == 0 and jolly_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_pri_scores_third(stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, jolly_c1 = ?, jolly_c2 = ?, jolly_ass = ?, jolly_exam = ?, jolly_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, jolly_c1, jolly_c2, jolly_ass, jolly_exam, jolly_total, stud_no,))
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
            cmd1 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42]+ row[47] + row[52] + row[57] + row[62] + row[67] + row[72] + row[77]
            avg = round((all_total/1500)*100, 4)

            cmd0 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
            cur.execute(cmd0, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum0 = all_total
            elif row[78] == None:
                total_cum0 = all_total
            else:
                total_cum0 = row[78] + all_total

            cmd2 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum = total_cum0
                avg_cum = round((total_cum/3000)*100, 4)
            elif row[78] == row[80]:
                total_cum = row[78] + total_cum0
                avg_cum = round((total_cum/3000)*100, 4)
            else:
                total_cum = row[78] + total_cum0
                avg_cum = round((total_cum/4500)*100, 4)

            cmd3 = "UPDATE t_pri_scores_third SET stud_no = ?, all_total = ?, avg = ?, total_cum = ?, avg_cum = ?  WHERE stud_no = ?"
            cur.execute(cmd3, (stud_no, all_total, avg, total_cum, avg_cum, stud_no,))
            con.commit()

            QMessageBox.information(self, "Computing Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Computing Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "Computing Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()


class PriScoresView3(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PriScore3rdForm()
        self.ui.setupUi(self)

        self.pri_report3 = PriReport3()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()


        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generatePriReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_pri_scores_third ORDER BY score_class')
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
        cmd = "SELECT * FROM t_pri_scores_third ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_pri_scores_third WHERE score_class = ? ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_pri_scores_third WHERE score_class = ? ORDER BY stud_no"
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
            cmd = "DELETE FROM t_pri_scores_third WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting Pupil', "WARNING: Deleting will remove all the pupil's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generatePriReport(self):
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

            self.pri_report3.ui.name_label.setText(row[1])
            self.pri_report3.ui.class_label.setText(row[3])
            self.pri_report3.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.pri_report3.ui.photo_label.setPixmap(QPixmap(pixmap))

            try:
                cmd3 = "SELECT * FROM t_pri_scores_third WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.pri_report3.ui.qur_c1_label.setText(str(row[3]))
                self.pri_report3.ui.qur_c2_label.setText(str(row[4]))
                self.pri_report3.ui.qur_ass_label.setText(str(row[5]))
                self.pri_report3.ui.qur_exam_label.setText(str(row[6]))
                self.pri_report3.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.pri_report3.ui.qur_grade_label.setText("F")
                    self.pri_report3.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.pri_report3.ui.qur_grade_label.setText("D")
                    self.pri_report3.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.pri_report3.ui.qur_grade_label.setText("C")
                    self.pri_report3.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.pri_report3.ui.qur_grade_label.setText("B")
                    self.pri_report3.ui.qur_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.qur_grade_label.setText("A")
                    self.pri_report3.ui.qur_remark_label.setText("Excellent")

                self.pri_report3.ui.ibadat_c1_label.setText(str(row[8]))
                self.pri_report3.ui.ibadat_c2_label.setText(str(row[9]))
                self.pri_report3.ui.ibadat_ass_label.setText(str(row[10]))
                self.pri_report3.ui.ibadat_exam_label.setText(str(row[11]))
                self.pri_report3.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.pri_report3.ui.ibadat_grade_label.setText("F")
                    self.pri_report3.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.pri_report3.ui.ibadat_grade_label.setText("D")
                    self.pri_report3.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.pri_report3.ui.ibadat_grade_label.setText("C")
                    self.pri_report3.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.pri_report3.ui.ibadat_grade_label.setText("B")
                    self.pri_report3.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.ibadat_grade_label.setText("A")
                    self.pri_report3.ui.ibadat_remark_label.setText("Excellent")

                self.pri_report3.ui.arabic1_c1_label.setText(str(row[13]))
                self.pri_report3.ui.arabic1_c2_label.setText(str(row[14]))
                self.pri_report3.ui.arabic1_ass_label.setText(str(row[15]))
                self.pri_report3.ui.arabic1_exam_label.setText(str(row[16]))
                self.pri_report3.ui.arabic1_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.pri_report3.ui.arabic1_grade_label.setText("F")
                    self.pri_report3.ui.arabic1_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.pri_report3.ui.arabic1_grade_label.setText("D")
                    self.pri_report3.ui.arabic1_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.pri_report3.ui.arabic1_grade_label.setText("C")
                    self.pri_report3.ui.arabic1_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.pri_report3.ui.arabic1_grade_label.setText("B")
                    self.pri_report3.ui.arabic1_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.arabic1_grade_label.setText("A")
                    self.pri_report3.ui.arabic1_remark_label.setText("Excellent")

                self.pri_report3.ui.arabic2_c1_label.setText(str(row[18]))
                self.pri_report3.ui.arabic2_c2_label.setText(str(row[19]))
                self.pri_report3.ui.arabic2_ass_label.setText(str(row[20]))
                self.pri_report3.ui.arabic2_exam_label.setText(str(row[21]))
                self.pri_report3.ui.arabic2_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.pri_report3.ui.arabic2_grade_label.setText("F")
                    self.pri_report3.ui.arabic2_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.pri_report3.ui.arabic2_grade_label.setText("D")
                    self.pri_report3.ui.arabic2_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.pri_report3.ui.arabic2_grade_label.setText("C")
                    self.pri_report3.ui.arabic2_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.pri_report3.ui.arabic2_grade_label.setText("B")
                    self.pri_report3.ui.arabic2_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.arabic2_grade_label.setText("A")
                    self.pri_report3.ui.arabic2_remark_label.setText("Excellent")

                self.pri_report3.ui.math_c1_label.setText(str(row[23]))
                self.pri_report3.ui.math_c2_label.setText(str(row[24]))
                self.pri_report3.ui.math_ass_label.setText(str(row[25]))
                self.pri_report3.ui.math_exam_label.setText(str(row[26]))
                self.pri_report3.ui.math_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.pri_report3.ui.math_grade_label.setText("F")
                    self.pri_report3.ui.math_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.pri_report3.ui.math_grade_label.setText("D")
                    self.pri_report3.ui.math_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.pri_report3.ui.math_grade_label.setText("C")
                    self.pri_report3.ui.math_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.pri_report3.ui.math_grade_label.setText("B")
                    self.pri_report3.ui.math_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.math_grade_label.setText("A")
                    self.pri_report3.ui.math_remark_label.setText("Excellent")

                self.pri_report3.ui.eng_c1_label.setText(str(row[28]))
                self.pri_report3.ui.eng_c2_label.setText(str(row[29]))
                self.pri_report3.ui.eng_ass_label.setText(str(row[30]))
                self.pri_report3.ui.eng_exam_label.setText(str(row[31]))
                self.pri_report3.ui.eng_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.pri_report3.ui.eng_grade_label.setText("F")
                    self.pri_report3.ui.eng_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.pri_report3.ui.eng_grade_label.setText("D")
                    self.pri_report3.ui.eng_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.pri_report3.ui.eng_grade_label.setText("C")
                    self.pri_report3.ui.eng_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.pri_report3.ui.eng_grade_label.setText("B")
                    self.pri_report3.ui.eng_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.eng_grade_label.setText("A")
                    self.pri_report3.ui.eng_remark_label.setText("Excellent")

                self.pri_report3.ui.comp_c1_label.setText(str(row[33]))
                self.pri_report3.ui.comp_c2_label.setText(str(row[34]))
                self.pri_report3.ui.comp_ass_label.setText(str(row[35]))
                self.pri_report3.ui.comp_exam_label.setText(str(row[36]))
                self.pri_report3.ui.comp_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.pri_report3.ui.comp_grade_label.setText("F")
                    self.pri_report3.ui.comp_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.pri_report3.ui.comp_grade_label.setText("D")
                    self.pri_report3.ui.comp_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.pri_report3.ui.comp_grade_label.setText("C")
                    self.pri_report3.ui.comp_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.pri_report3.ui.comp_grade_label.setText("B")
                    self.pri_report3.ui.comp_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.comp_grade_label.setText("A")
                    self.pri_report3.ui.comp_remark_label.setText("Excellent")

                self.pri_report3.ui.bas_sc_c1_label.setText(str(row[38]))
                self.pri_report3.ui.bas_sc_c2_label.setText(str(row[39]))
                self.pri_report3.ui.bas_sc_ass_label.setText(str(row[40]))
                self.pri_report3.ui.bas_sc_exam_label.setText(str(row[41]))
                self.pri_report3.ui.bas_sc_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.pri_report3.ui.bas_sc_grade_label.setText("F")
                    self.pri_report3.ui.bas_sc_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.pri_report3.ui.bas_sc_grade_label.setText("D")
                    self.pri_report3.ui.bas_sc_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.pri_report3.ui.bas_sc_grade_label.setText("C")
                    self.pri_report3.ui.bas_sc_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.pri_report3.ui.bas_sc_grade_label.setText("B")
                    self.pri_report3.ui.bas_sc_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.bas_sc_grade_label.setText("A")
                    self.pri_report3.ui.bas_sc_remark_label.setText("Excellent")

                self.pri_report3.ui.religion_c1_label.setText(str(row[43]))
                self.pri_report3.ui.religion_c2_label.setText(str(row[44]))
                self.pri_report3.ui.religion_ass_label.setText(str(row[45]))
                self.pri_report3.ui.religion_exam_label.setText(str(row[46]))
                self.pri_report3.ui.religion_total_label.setText(str(row[47]))

                if row[47] < 40:
                    self.pri_report3.ui.religion_grade_label.setText("F")
                    self.pri_report3.ui.religion_remark_label.setText("Fail")
                elif row[47] >= 40 and row[47] < 50:
                    self.pri_report3.ui.religion_grade_label.setText("D")
                    self.pri_report3.ui.religion_remark_label.setText("Pass")
                elif row[47] >= 50 and row[47] < 60:
                    self.pri_report3.ui.religion_grade_label.setText("C")
                    self.pri_report3.ui.religion_remark_label.setText("Good")
                elif row[47] >= 60 and row[47] < 70:
                    self.pri_report3.ui.religion_grade_label.setText("B")
                    self.pri_report3.ui.religion_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.religion_grade_label.setText("A")
                    self.pri_report3.ui.religion_remark_label.setText("Excellent")

                self.pri_report3.ui.civic_c1_label.setText(str(row[48]))
                self.pri_report3.ui.civic_c2_label.setText(str(row[49]))
                self.pri_report3.ui.civic_ass_label.setText(str(row[50]))
                self.pri_report3.ui.civic_exam_label.setText(str(row[51]))
                self.pri_report3.ui.civic_total_label.setText(str(row[52]))

                if row[52] < 40:
                    self.pri_report3.ui.civic_grade_label.setText("F")
                    self.pri_report3.ui.civic_remark_label.setText("Fail")
                elif row[52] >= 40 and row[52] < 50:
                    self.pri_report3.ui.civic_grade_label.setText("D")
                    self.pri_report3.ui.civic_remark_label.setText("Pass")
                elif row[52] >= 50 and row[52] < 60:
                    self.pri_report3.ui.civic_grade_label.setText("C")
                    self.pri_report3.ui.civic_remark_label.setText("Good")
                elif row[52] >= 60 and row[52] < 70:
                    self.pri_report3.ui.civic_grade_label.setText("B")
                    self.pri_report3.ui.civic_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.civic_grade_label.setText("A")
                    self.pri_report3.ui.civic_remark_label.setText("Excellent")

                self.pri_report3.ui.verbal_c1_label.setText(str(row[53]))
                self.pri_report3.ui.verbal_c2_label.setText(str(row[54]))
                self.pri_report3.ui.verbal_ass_label.setText(str(row[55]))
                self.pri_report3.ui.verbal_exam_label.setText(str(row[56]))
                self.pri_report3.ui.verbal_total_label.setText(str(row[57]))

                if row[57] < 40:
                    self.pri_report3.ui.verbal_grade_label.setText("F")
                    self.pri_report3.ui.verbal_remark_label.setText("Fail")
                elif row[57] >= 40 and row[57] < 50:
                    self.pri_report3.ui.verbal_grade_label.setText("D")
                    self.pri_report3.ui.verbal_remark_label.setText("Pass")
                elif row[57] >= 50 and row[57] < 60:
                    self.pri_report3.ui.verbal_grade_label.setText("C")
                    self.pri_report3.ui.verbal_remark_label.setText("Good")
                elif row[57] >= 60 and row[57] < 70:
                    self.pri_report3.ui.verbal_grade_label.setText("B")
                    self.pri_report3.ui.verbal_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.verbal_grade_label.setText("A")
                    self.pri_report3.ui.verbal_remark_label.setText("Excellent")

                self.pri_report3.ui.quant_c1_label.setText(str(row[58]))
                self.pri_report3.ui.quant_c2_label.setText(str(row[59]))
                self.pri_report3.ui.quant_ass_label.setText(str(row[60]))
                self.pri_report3.ui.quant_exam_label.setText(str(row[61]))
                self.pri_report3.ui.quant_total_label.setText(str(row[62]))

                if row[62] < 40:
                    self.pri_report3.ui.quant_grade_label.setText("F")
                    self.pri_report3.ui.quant_remark_label.setText("Fail")
                elif row[62] >= 40 and row[62] < 50:
                    self.pri_report3.ui.quant_grade_label.setText("D")
                    self.pri_report3.ui.quant_remark_label.setText("Pass")
                elif row[62] >= 50 and row[62] < 60:
                    self.pri_report3.ui.quant_grade_label.setText("C")
                    self.pri_report3.ui.quant_remark_label.setText("Good")
                elif row[62] >= 60 and row[62] < 70:
                    self.pri_report3.ui.quant_grade_label.setText("B")
                    self.pri_report3.ui.quant_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.quant_grade_label.setText("A")
                    self.pri_report3.ui.quant_remark_label.setText("Excellent")

                self.pri_report3.ui.handwriting_c1_label.setText(str(row[63]))
                self.pri_report3.ui.handwriting_c2_label.setText(str(row[64]))
                self.pri_report3.ui.handwriting_ass_label.setText(str(row[65]))
                self.pri_report3.ui.handwriting_exam_label.setText(str(row[66]))
                self.pri_report3.ui.handwriting_total_label.setText(str(row[67]))

                if row[67] < 40:
                    self.pri_report3.ui.handwriting_grade_label.setText("F")
                    self.pri_report3.ui.handwriting_remark_label.setText("Fail")
                elif row[67] >= 40 and row[67] < 50:
                    self.pri_report3.ui.handwriting_grade_label.setText("D")
                    self.pri_report3.ui.handwriting_remark_label.setText("Pass")
                elif row[67] >= 50 and row[67] < 60:
                    self.pri_report3.ui.handwriting_grade_label.setText("C")
                    self.pri_report3.ui.handwriting_remark_label.setText("Good")
                elif row[67] >= 60 and row[67] < 70:
                    self.pri_report3.ui.handwriting_grade_label.setText("B")
                    self.pri_report3.ui.handwriting_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.handwriting_grade_label.setText("A")
                    self.pri_report3.ui.handwriting_remark_label.setText("Excellent")

                self.pri_report3.ui.french_c1_label.setText(str(row[68]))
                self.pri_report3.ui.french_c2_label.setText(str(row[69]))
                self.pri_report3.ui.french_ass_label.setText(str(row[70]))
                self.pri_report3.ui.french_exam_label.setText(str(row[71]))
                self.pri_report3.ui.french_total_label.setText(str(row[72]))

                if row[72] < 40:
                    self.pri_report3.ui.french_grade_label.setText("F")
                    self.pri_report3.ui.french_remark_label.setText("Fail")
                elif row[72] >= 40 and row[72] < 50:
                    self.pri_report3.ui.french_grade_label.setText("D")
                    self.pri_report3.ui.french_remark_label.setText("Pass")
                elif row[72] >= 50 and row[72] < 60:
                    self.pri_report3.ui.french_grade_label.setText("C")
                    self.pri_report3.ui.french_remark_label.setText("Good")
                elif row[72] >= 60 and row[72] < 70:
                    self.pri_report3.ui.french_grade_label.setText("B")
                    self.pri_report3.ui.french_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.french_grade_label.setText("A")
                    self.pri_report3.ui.french_remark_label.setText("Excellent")

                self.pri_report3.ui.jolly_c1_label.setText(str(row[73]))
                self.pri_report3.ui.jolly_c2_label.setText(str(row[74]))
                self.pri_report3.ui.jolly_ass_label.setText(str(row[75]))
                self.pri_report3.ui.jolly_exam_label.setText(str(row[76]))
                self.pri_report3.ui.jolly_total_label.setText(str(row[77]))

                if row[77] < 40:
                    self.pri_report3.ui.jolly_grade_label.setText("F")
                    self.pri_report3.ui.jolly_remark_label.setText("Fail")
                elif row[77] >= 40 and row[77] < 50:
                    self.pri_report3.ui.jolly_grade_label.setText("D")
                    self.pri_report3.ui.jolly_remark_label.setText("Pass")
                elif row[77] >= 50 and row[77] < 60:
                    self.pri_report3.ui.jolly_grade_label.setText("C")
                    self.pri_report3.ui.jolly_remark_label.setText("Good")
                elif row[77] >= 60 and row[77] < 70:
                    self.pri_report3.ui.jolly_grade_label.setText("B")
                    self.pri_report3.ui.jolly_remark_label.setText("Very Good")
                else:
                    self.pri_report3.ui.jolly_grade_label.setText("A")
                    self.pri_report3.ui.jolly_remark_label.setText("Excellent")

                self.pri_report3.ui.total_scores3_label.setText(str(row[78]))
                self.pri_report3.ui.avg3_label.setText(str(row[79]))
                self.pri_report3.ui.total_cum_label.setText(str(row[80]))
                self.pri_report3.ui.avg_cum_label.setText(str(row[81]))

                if row[79] < 40:
                    self.pri_report3.ui.master_com_label.setText("Bad result. Be careful.")
                    self.pri_report3.ui.head_com_label.setText("Bad result.")
                elif row[79] >= 40 and row[79] < 50:
                    self.pri_report3.ui.master_com_label.setText("Weak result. Work hard.")
                    self.pri_report3.ui.head_com_label.setText("Weak result.")
                elif row[79] >= 50 and row[79] < 60:
                    self.pri_report3.ui.master_com_label.setText("Fair result. Work hard.")
                    self.pri_report3.ui.head_com_label.setText("Fair result.")
                elif row[79] >= 60 and row[79] < 70:
                    self.pri_report3.ui.master_com_label.setText("Good result. Put more effort.")
                    self.pri_report3.ui.head_com_label.setText("Good result.")
                else:
                    self.pri_report3.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.pri_report3.ui.head_com_label.setText("Excellent result.")

                cmd9 = "SELECT * FROM t_pri_scores_first WHERE stud_no = ?"
                cur.execute(cmd9, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.pri_report3.ui.total_scores_label.setText("None")
                    self.pri_report3.ui.avg_label.setText("None")
                elif row[78] == None and row[79] == None:
                    self.pri_report3.ui.total_scores_label.setText("None")
                    self.pri_report3.ui.avg_label.setText("None")
                else:
                    self.pri_report3.ui.total_scores_label.setText(str(row[78]))
                    self.pri_report3.ui.avg_label.setText(str(row[79]))

                cmd10 = "SELECT * FROM t_pri_scores_second WHERE stud_no = ?"
                cur.execute(cmd10, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.pri_report3.ui.total_scores2_label.setText("None")
                    self.pri_report3.ui.avg2_label.setText("None")
                elif row[78] == None and row[79] == None:
                    self.pri_report3.ui.total_scores2_label.setText("None")
                    self.pri_report3.ui.avg2_label.setText("None")
                else:
                    self.pri_report3.ui.total_scores2_label.setText(str(row[78]))
                    self.pri_report3.ui.avg2_label.setText(str(row[79]))

                positions = []
                cmd11 = "SELECT * FROM t_pri_scores_third WHERE score_class = ? ORDER BY avg DESC"
                cur.execute(cmd11, (classes_combo,))
                rows = cur.fetchall()
                for row in rows:
                    positions.append(row[1])
                self.pri_report3.ui.out_of_label.setText(str(len(positions)))
                for i in range(len(positions)):
                    if admission_no == positions[i]:
                        if i in range (10, len(positions), 100):
                            self.pri_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (11, len(positions), 100):
                            self.pri_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (12, len(positions), 100):
                            self.pri_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (0, len(positions), 10):
                            self.pri_report3.ui.position_label.setText(str(i+1)+"st")
                        elif i in range (1, len(positions), 10):
                            self.pri_report3.ui.position_label.setText(str(i+1)+"nd")
                        elif i in range (2, len(positions), 10):
                            self.pri_report3.ui.position_label.setText(str(i+1)+"rd")
                        else:
                            self.pri_report3.ui.position_label.setText(str(i+1)+"th")

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.pri_report3.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.pri_report3.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.pri_report3.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.pri_report3.ui.fees_label.setText(row[4])

                cmd8 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd8)
                row = cur.fetchone()
                self.pri_report3.ui.session_label.setText(row[2])

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
            self.pri_report3.ui.att_a_label.setText("v")
            self.pri_report3.ui.att_b_label.setText("")
            self.pri_report3.ui.att_c_label.setText("")
            self.pri_report3.ui.att_d_label.setText("")
            self.pri_report3.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.pri_report3.ui.att_a_label.setText("")
            self.pri_report3.ui.att_b_label.setText("v")
            self.pri_report3.ui.att_c_label.setText("")
            self.pri_report3.ui.att_d_label.setText("")
            self.pri_report3.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.pri_report3.ui.att_a_label.setText("")
            self.pri_report3.ui.att_b_label.setText("")
            self.pri_report3.ui.att_c_label.setText("v")
            self.pri_report3.ui.att_d_label.setText("")
            self.pri_report3.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.pri_report3.ui.att_a_label.setText("")
            self.pri_report3.ui.att_b_label.setText("")
            self.pri_report3.ui.att_c_label.setText("")
            self.pri_report3.ui.att_d_label.setText("v")
            self.pri_report3.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.pri_report3.ui.att_a_label.setText("")
            self.pri_report3.ui.att_b_label.setText("")
            self.pri_report3.ui.att_c_label.setText("")
            self.pri_report3.ui.att_d_label.setText("")
            self.pri_report3.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.pri_report3.ui.con_a_label.setText("v")
            self.pri_report3.ui.con_b_label.setText("")
            self.pri_report3.ui.con_c_label.setText("")
            self.pri_report3.ui.con_d_label.setText("")
            self.pri_report3.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.pri_report3.ui.con_a_label.setText("")
            self.pri_report3.ui.con_b_label.setText("v")
            self.pri_report3.ui.con_c_label.setText("")
            self.pri_report3.ui.con_d_label.setText("")
            self.pri_report3.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.pri_report3.ui.con_a_label.setText("")
            self.pri_report3.ui.con_b_label.setText("")
            self.pri_report3.ui.con_c_label.setText("v")
            self.pri_report3.ui.con_d_label.setText("")
            self.pri_report3.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.pri_report3.ui.con_a_label.setText("")
            self.pri_report3.ui.con_b_label.setText("")
            self.pri_report3.ui.con_c_label.setText("")
            self.pri_report3.ui.con_d_label.setText("v")
            self.pri_report3.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.pri_report3.ui.con_a_label.setText("")
            self.pri_report3.ui.con_b_label.setText("")
            self.pri_report3.ui.con_c_label.setText("")
            self.pri_report3.ui.con_d_label.setText("")
            self.pri_report3.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.pri_report3.ui.neat_a_label.setText("v")
            self.pri_report3.ui.neat_b_label.setText("")
            self.pri_report3.ui.neat_c_label.setText("")
            self.pri_report3.ui.neat_d_label.setText("")
            self.pri_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.pri_report3.ui.neat_a_label.setText("")
            self.pri_report3.ui.neat_b_label.setText("v")
            self.pri_report3.ui.neat_c_label.setText("")
            self.pri_report3.ui.neat_d_label.setText("")
            self.pri_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.pri_report3.ui.neat_a_label.setText("")
            self.pri_report3.ui.neat_b_label.setText("v")
            self.pri_report3.ui.neat_c_label.setText("")
            self.pri_report3.ui.neat_d_label.setText("")
            self.pri_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.pri_report3.ui.neat_a_label.setText("")
            self.pri_report3.ui.neat_b_label.setText("")
            self.pri_report3.ui.neat_c_label.setText("v")
            self.pri_report3.ui.neat_d_label.setText("")
            self.pri_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.pri_report3.ui.neat_a_label.setText("")
            self.pri_report3.ui.neat_b_label.setText("")
            self.pri_report3.ui.neat_c_label.setText("")
            self.pri_report3.ui.neat_d_label.setText("v")
            self.pri_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.pri_report3.ui.neat_a_label.setText("")
            self.pri_report3.ui.neat_b_label.setText("")
            self.pri_report3.ui.neat_c_label.setText("")
            self.pri_report3.ui.neat_d_label.setText("")
            self.pri_report3.ui.neat_e_label.setText("v")


    def printReport3(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.pri_report3.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

class PriReport3(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PriReport3rdForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pri_scores_record = PriScoresRecord()
    pri_scores_record.show()
    sys.exit(app.exec_())
