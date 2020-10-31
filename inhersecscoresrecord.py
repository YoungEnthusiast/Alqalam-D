import sys
from PyQt5 import QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QDateTime, QByteArray
from secreport import Ui_SecReportForm
from secreport2nd import Ui_SecReport2ndForm
from secreport3rd import Ui_SecReport3rdForm

from secscoresrecord import Ui_SecScoreRecForm
from secscoresrecord2nd import Ui_SecScoreRec2ndForm
from secscoresrecord3rd import Ui_SecScoreRec3rdForm
from secscoreslist import Ui_SecScoreForm
from secscoreslist2nd import Ui_SecScore2ndForm
from secscoreslist3rd import Ui_SecScore3rdForm

import sqlite3
from sqlite3 import Error


class SecScoresRecord(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_SecScoreRecForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic1_score_btn.clicked.connect(self.saveArabic1Scores)
        self.ui.nahwu_score_btn.clicked.connect(self.saveNahwuScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.bas_sc_score_btn.clicked.connect(self.saveBasScScores)
        self.ui.religion_score_btn.clicked.connect(self.saveReligionScores)
        self.ui.civic_score_btn.clicked.connect(self.saveCivicScores)
        self.ui.cca_score_btn.clicked.connect(self.saveCcaScores)
        self.ui.prevoc_score_btn.clicked.connect(self.savePrevocScores)
        self.ui.french_score_btn.clicked.connect(self.saveFrenchScores)
        self.ui.hausa_score_btn.clicked.connect(self.saveHausaScores)

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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic1_c1 == 0 and arabic1_c2 == 0 and arabic1_ass == 0 and arabic1_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, arabic1_c1 = ?, arabic1_c2 = ?, arabic1_ass = ?, arabic1_exam = ?, arabic1_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveNahwuScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        nahwu_c1 = self.ui.nahwu_c1_spin.value()
        nahwu_c2 = self.ui.nahwu_c2_spin.value()
        nahwu_ass = self.ui.nahwu_ass_spin.value()
        nahwu_exam = self.ui.nahwu_exam_spin.value()
        nahwu_total = nahwu_c1 + nahwu_c2 + nahwu_ass + nahwu_exam

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if nahwu_c1 == 0 and nahwu_c2 == 0 and nahwu_ass == 0 and nahwu_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, nahwu_c1 = ?, nahwu_c2 = ?, nahwu_ass = ?, nahwu_exam = ?, nahwu_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if bas_sc_c1 == 0 and bas_sc_c2 == 0 and bas_sc_ass == 0 and bas_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, bas_sc_c1 = ?, bas_sc_c2 = ?, bas_sc_ass = ?, bas_sc_exam = ?, bas_sc_total = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if religion_c1 == 0 and religion_c2 == 0 and religion_ass == 0 and religion_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, religion_c1 = ?, religion_c2 = ?, religion_ass = ?, religion_exam = ?, religion_total = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if civic_c1 == 0 and civic_c2 == 0 and civic_ass == 0 and civic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, civic_c1 = ?, civic_c2 = ?, civic_ass = ?, civic_exam = ?, civic_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()


    def saveCcaScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        cca_c1 = self.ui.cca_c1_spin.value()
        cca_c2 = self.ui.cca_c2_spin.value()
        cca_ass = self.ui.cca_ass_spin.value()
        cca_exam = self.ui.cca_exam_spin.value()
        cca_total = cca_c1 + cca_c2 + cca_ass + cca_exam

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if cca_c1 == 0 and cca_c2 == 0 and cca_ass == 0 and cca_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, cca_c1 = ?, cca_c2 = ?, cca_ass = ?, cca_exam = ?, cca_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def savePrevocScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        prevoc_c1 = self.ui.prevoc_c1_spin.value()
        prevoc_c2 = self.ui.prevoc_c2_spin.value()
        prevoc_ass = self.ui.prevoc_ass_spin.value()
        prevoc_exam = self.ui.prevoc_exam_spin.value()
        prevoc_total = prevoc_c1 + prevoc_c2 + prevoc_ass + prevoc_exam

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if prevoc_c1 == 0 and prevoc_c2 == 0 and prevoc_ass == 0 and prevoc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, prevoc_c1 = ?, prevoc_c2 = ?, prevoc_ass = ?, prevoc_exam = ?, prevoc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if french_c1 == 0 and french_c2 == 0 and french_ass == 0 and french_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, french_c1, french_c2, french_ass, french_exam, french_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, french_c1 = ?, french_c2 = ?, french_ass = ?, french_exam = ?, french_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveHausaScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        hausa_c1 = self.ui.hausa_c1_spin.value()
        hausa_c2 = self.ui.hausa_c2_spin.value()
        hausa_ass = self.ui.hausa_ass_spin.value()
        hausa_exam = self.ui.hausa_exam_spin.value()
        hausa_total = hausa_c1 + hausa_c2 + hausa_ass + hausa_exam

        cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if hausa_c1 == 0 and hausa_c2 == 0 and hausa_ass == 0 and hausa_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_first(stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_first SET stud_no = ?, hausa_c1 = ?, hausa_c2 = ?, hausa_ass = ?, hausa_exam = ?, hausa_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total, stud_no,))
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
            cmd1 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42] + row[47] + row[52] + row[57] + row[62] + row[67]
            avg = round((all_total/1300)*100, 4)
            cmd2 = "UPDATE t_sec_scores_first SET stud_no = ?, all_total = ?, avg = ?  WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no, all_total, avg, stud_no,))
            con.commit()
            QMessageBox.information(self, "ccauting Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "ccauting Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "ccauting Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()

class SecScoresView(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SecScoreForm()
        self.ui.setupUi(self)

        self.sec_report = SecReport()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()


        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generateSecReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_sec_scores_first ORDER BY score_class')
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
        cmd = "SELECT * FROM t_sec_scores_first ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_sec_scores_first WHERE score_class = ? ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_sec_scores_first WHERE score_class = ? ORDER BY stud_no"
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
            QMessageBox.critical(self, "Deleting Student", "ERROR: Please select student's admission number before pressing delete", QMessageBox.Ok)
        elif stud_no == "":
            QMessageBox.critical(self, "Deleting Student", "ERROR: Please select a class and student's admission number before pressing delete", QMessageBox.Ok)
        else:
            cmd = "DELETE FROM t_sec_scores_first WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting Student', "WARNING: Deleting will remove all the student's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generateSecReport(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        admission_no = self.ui.stud_adm_no_comboBox.currentText()
        cmd1 = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd1, (admission_no,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Printing Report", "ERROR: Please select a class and student's admission number before generating report", QMessageBox.Ok)
        else:

            self.sec_report.ui.name_label.setText(row[1])
            self.sec_report.ui.class_label.setText(row[3])
            self.sec_report.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.sec_report.ui.photo_label.setPixmap(QPixmap(pixmap))

            try:

                cmd3 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.sec_report.ui.qur_c1_label.setText(str(row[3]))
                self.sec_report.ui.qur_c2_label.setText(str(row[4]))
                self.sec_report.ui.qur_ass_label.setText(str(row[5]))
                self.sec_report.ui.qur_exam_label.setText(str(row[6]))
                self.sec_report.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.sec_report.ui.qur_grade_label.setText("F")
                    self.sec_report.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.sec_report.ui.qur_grade_label.setText("D")
                    self.sec_report.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.sec_report.ui.qur_grade_label.setText("C")
                    self.sec_report.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.sec_report.ui.qur_grade_label.setText("B")
                    self.sec_report.ui.qur_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.qur_grade_label.setText("A")
                    self.sec_report.ui.qur_remark_label.setText("Excellent")

                self.sec_report.ui.ibadat_c1_label.setText(str(row[8]))
                self.sec_report.ui.ibadat_c2_label.setText(str(row[9]))
                self.sec_report.ui.ibadat_ass_label.setText(str(row[10]))
                self.sec_report.ui.ibadat_exam_label.setText(str(row[11]))
                self.sec_report.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.sec_report.ui.ibadat_grade_label.setText("F")
                    self.sec_report.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.sec_report.ui.ibadat_grade_label.setText("D")
                    self.sec_report.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.sec_report.ui.ibadat_grade_label.setText("C")
                    self.sec_report.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.sec_report.ui.ibadat_grade_label.setText("B")
                    self.sec_report.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.ibadat_grade_label.setText("A")
                    self.sec_report.ui.ibadat_remark_label.setText("Excellent")

                self.sec_report.ui.arabic1_c1_label.setText(str(row[13]))
                self.sec_report.ui.arabic1_c2_label.setText(str(row[14]))
                self.sec_report.ui.arabic1_ass_label.setText(str(row[15]))
                self.sec_report.ui.arabic1_exam_label.setText(str(row[16]))
                self.sec_report.ui.arabic1_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.sec_report.ui.arabic1_grade_label.setText("F")
                    self.sec_report.ui.arabic1_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.sec_report.ui.arabic1_grade_label.setText("D")
                    self.sec_report.ui.arabic1_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.sec_report.ui.arabic1_grade_label.setText("C")
                    self.sec_report.ui.arabic1_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.sec_report.ui.arabic1_grade_label.setText("B")
                    self.sec_report.ui.arabic1_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.arabic1_grade_label.setText("A")
                    self.sec_report.ui.arabic1_remark_label.setText("Excellent")

                self.sec_report.ui.nahwu_c1_label.setText(str(row[18]))
                self.sec_report.ui.nahwu_c2_label.setText(str(row[19]))
                self.sec_report.ui.nahwu_ass_label.setText(str(row[20]))
                self.sec_report.ui.nahwu_exam_label.setText(str(row[21]))
                self.sec_report.ui.nahwu_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.sec_report.ui.nahwu_grade_label.setText("F")
                    self.sec_report.ui.nahwu_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.sec_report.ui.nahwu_grade_label.setText("D")
                    self.sec_report.ui.nahwu_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.sec_report.ui.nahwu_grade_label.setText("C")
                    self.sec_report.ui.nahwu_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.sec_report.ui.nahwu_grade_label.setText("B")
                    self.sec_report.ui.nahwu_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.nahwu_grade_label.setText("A")
                    self.sec_report.ui.nahwu_remark_label.setText("Excellent")

                self.sec_report.ui.eng_c1_label.setText(str(row[23]))
                self.sec_report.ui.eng_c2_label.setText(str(row[24]))
                self.sec_report.ui.eng_ass_label.setText(str(row[25]))
                self.sec_report.ui.eng_exam_label.setText(str(row[26]))
                self.sec_report.ui.eng_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.sec_report.ui.eng_grade_label.setText("F")
                    self.sec_report.ui.eng_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.sec_report.ui.eng_grade_label.setText("D")
                    self.sec_report.ui.eng_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.sec_report.ui.eng_grade_label.setText("C")
                    self.sec_report.ui.eng_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.sec_report.ui.eng_grade_label.setText("B")
                    self.sec_report.ui.eng_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.eng_grade_label.setText("A")
                    self.sec_report.ui.eng_remark_label.setText("Excellent")

                self.sec_report.ui.math_c1_label.setText(str(row[28]))
                self.sec_report.ui.math_c2_label.setText(str(row[29]))
                self.sec_report.ui.math_ass_label.setText(str(row[30]))
                self.sec_report.ui.math_exam_label.setText(str(row[31]))
                self.sec_report.ui.math_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.sec_report.ui.math_grade_label.setText("F")
                    self.sec_report.ui.math_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.sec_report.ui.math_grade_label.setText("D")
                    self.sec_report.ui.math_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.sec_report.ui.math_grade_label.setText("C")
                    self.sec_report.ui.math_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.sec_report.ui.math_grade_label.setText("B")
                    self.sec_report.ui.math_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.math_grade_label.setText("A")
                    self.sec_report.ui.math_remark_label.setText("Excellent")

                self.sec_report.ui.bas_sc_c1_label.setText(str(row[33]))
                self.sec_report.ui.bas_sc_c2_label.setText(str(row[34]))
                self.sec_report.ui.bas_sc_ass_label.setText(str(row[35]))
                self.sec_report.ui.bas_sc_exam_label.setText(str(row[36]))
                self.sec_report.ui.bas_sc_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.sec_report.ui.bas_sc_grade_label.setText("F")
                    self.sec_report.ui.bas_sc_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.sec_report.ui.bas_sc_grade_label.setText("D")
                    self.sec_report.ui.bas_sc_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.sec_report.ui.bas_sc_grade_label.setText("C")
                    self.sec_report.ui.bas_sc_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.sec_report.ui.bas_sc_grade_label.setText("B")
                    self.sec_report.ui.bas_sc_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.bas_sc_grade_label.setText("A")
                    self.sec_report.ui.bas_sc_remark_label.setText("Excellent")

                self.sec_report.ui.religion_c1_label.setText(str(row[38]))
                self.sec_report.ui.religion_c2_label.setText(str(row[39]))
                self.sec_report.ui.religion_ass_label.setText(str(row[40]))
                self.sec_report.ui.religion_exam_label.setText(str(row[41]))
                self.sec_report.ui.religion_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.sec_report.ui.religion_grade_label.setText("F")
                    self.sec_report.ui.religion_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.sec_report.ui.religion_grade_label.setText("D")
                    self.sec_report.ui.religion_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.sec_report.ui.religion_grade_label.setText("C")
                    self.sec_report.ui.religion_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.sec_report.ui.religion_grade_label.setText("B")
                    self.sec_report.ui.religion_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.religion_grade_label.setText("A")
                    self.sec_report.ui.religion_remark_label.setText("Excellent")

                self.sec_report.ui.civic_c1_label.setText(str(row[43]))
                self.sec_report.ui.civic_c2_label.setText(str(row[44]))
                self.sec_report.ui.civic_ass_label.setText(str(row[45]))
                self.sec_report.ui.civic_exam_label.setText(str(row[46]))
                self.sec_report.ui.civic_total_label.setText(str(row[47]))

                if row[47] < 40:
                    self.sec_report.ui.civic_grade_label.setText("F")
                    self.sec_report.ui.civic_remark_label.setText("Fail")
                elif row[47] >= 40 and row[47] < 50:
                    self.sec_report.ui.civic_grade_label.setText("D")
                    self.sec_report.ui.civic_remark_label.setText("Pass")
                elif row[47] >= 50 and row[47] < 60:
                    self.sec_report.ui.civic_grade_label.setText("C")
                    self.sec_report.ui.civic_remark_label.setText("Good")
                elif row[47] >= 60 and row[47] < 70:
                    self.sec_report.ui.civic_grade_label.setText("B")
                    self.sec_report.ui.civic_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.civic_grade_label.setText("A")
                    self.sec_report.ui.civic_remark_label.setText("Excellent")

                self.sec_report.ui.cca_c1_label.setText(str(row[48]))
                self.sec_report.ui.cca_c2_label.setText(str(row[49]))
                self.sec_report.ui.cca_ass_label.setText(str(row[50]))
                self.sec_report.ui.cca_exam_label.setText(str(row[51]))
                self.sec_report.ui.cca_total_label.setText(str(row[52]))

                if row[52] < 40:
                    self.sec_report.ui.cca_grade_label.setText("F")
                    self.sec_report.ui.cca_remark_label.setText("Fail")
                elif row[52] >= 40 and row[52] < 50:
                    self.sec_report.ui.cca_grade_label.setText("D")
                    self.sec_report.ui.cca_remark_label.setText("Pass")
                elif row[52] >= 50 and row[52] < 60:
                    self.sec_report.ui.cca_grade_label.setText("C")
                    self.sec_report.ui.cca_remark_label.setText("Good")
                elif row[52] >= 60 and row[52] < 70:
                    self.sec_report.ui.cca_grade_label.setText("B")
                    self.sec_report.ui.cca_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.cca_grade_label.setText("A")
                    self.sec_report.ui.cca_remark_label.setText("Excellent")

                self.sec_report.ui.prevoc_c1_label.setText(str(row[53]))
                self.sec_report.ui.prevoc_c2_label.setText(str(row[54]))
                self.sec_report.ui.prevoc_ass_label.setText(str(row[55]))
                self.sec_report.ui.prevoc_exam_label.setText(str(row[56]))
                self.sec_report.ui.prevoc_total_label.setText(str(row[57]))

                if row[57] < 40:
                    self.sec_report.ui.prevoc_grade_label.setText("F")
                    self.sec_report.ui.prevoc_remark_label.setText("Fail")
                elif row[57] >= 40 and row[57] < 50:
                    self.sec_report.ui.prevoc_grade_label.setText("D")
                    self.sec_report.ui.prevoc_remark_label.setText("Pass")
                elif row[57] >= 50 and row[57] < 60:
                    self.sec_report.ui.prevoc_grade_label.setText("C")
                    self.sec_report.ui.prevoc_remark_label.setText("Good")
                elif row[57] >= 60 and row[57] < 70:
                    self.sec_report.ui.prevoc_grade_label.setText("B")
                    self.sec_report.ui.prevoc_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.prevoc_grade_label.setText("A")
                    self.sec_report.ui.prevoc_remark_label.setText("Excellent")

                self.sec_report.ui.french_c1_label.setText(str(row[58]))
                self.sec_report.ui.french_c2_label.setText(str(row[59]))
                self.sec_report.ui.french_ass_label.setText(str(row[60]))
                self.sec_report.ui.french_exam_label.setText(str(row[61]))
                self.sec_report.ui.french_total_label.setText(str(row[62]))

                if row[62] < 40:
                    self.sec_report.ui.french_grade_label.setText("F")
                    self.sec_report.ui.french_remark_label.setText("Fail")
                elif row[62] >= 40 and row[62] < 50:
                    self.sec_report.ui.french_grade_label.setText("D")
                    self.sec_report.ui.french_remark_label.setText("Pass")
                elif row[62] >= 50 and row[62] < 60:
                    self.sec_report.ui.french_grade_label.setText("C")
                    self.sec_report.ui.french_remark_label.setText("Good")
                elif row[62] >= 60 and row[62] < 70:
                    self.sec_report.ui.french_grade_label.setText("B")
                    self.sec_report.ui.french_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.french_grade_label.setText("A")
                    self.sec_report.ui.french_remark_label.setText("Excellent")

                self.sec_report.ui.hausa_c1_label.setText(str(row[63]))
                self.sec_report.ui.hausa_c2_label.setText(str(row[64]))
                self.sec_report.ui.hausa_ass_label.setText(str(row[65]))
                self.sec_report.ui.hausa_exam_label.setText(str(row[66]))
                self.sec_report.ui.hausa_total_label.setText(str(row[67]))

                if row[67] < 40:
                    self.sec_report.ui.hausa_grade_label.setText("F")
                    self.sec_report.ui.hausa_remark_label.setText("Fail")
                elif row[67] >= 40 and row[67] < 50:
                    self.sec_report.ui.hausa_grade_label.setText("D")
                    self.sec_report.ui.hausa_remark_label.setText("Pass")
                elif row[67] >= 50 and row[67] < 60:
                    self.sec_report.ui.hausa_grade_label.setText("C")
                    self.sec_report.ui.hausa_remark_label.setText("Good")
                elif row[67] >= 60 and row[67] < 70:
                    self.sec_report.ui.hausa_grade_label.setText("B")
                    self.sec_report.ui.hausa_remark_label.setText("Very Good")
                else:
                    self.sec_report.ui.hausa_grade_label.setText("A")
                    self.sec_report.ui.hausa_remark_label.setText("Excellent")

                self.sec_report.ui.total_scores_label.setText(str(row[68]))
                self.sec_report.ui.avg_label.setText(str(row[69]))

                if row[69] < 40:
                    self.sec_report.ui.master_com_label.setText("Bad result. Be careful.")
                    self.sec_report.ui.head_com_label.setText("Bad result.")
                elif row[69] >= 40 and row[69] < 50:
                    self.sec_report.ui.master_com_label.setText("Weak result. Work hard.")
                    self.sec_report.ui.head_com_label.setText("Weak result.")
                elif row[69] >= 50 and row[69] < 60:
                    self.sec_report.ui.master_com_label.setText("Fair result. Work hard.")
                    self.sec_report.ui.head_com_label.setText("Fair result.")
                elif row[69] >= 60 and row[69] < 70:
                    self.sec_report.ui.master_com_label.setText("Good result. Put more effort.")
                    self.sec_report.ui.head_com_label.setText("Good result.")
                else:
                    self.sec_report.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.sec_report.ui.head_com_label.setText("Excellent result.")

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.sec_report.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.sec_report.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.sec_report.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.sec_report.ui.fees_label.setText(row[4])

                cmd8 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd8)
                row = cur.fetchone()
                self.sec_report.ui.session_label.setText(row[2])

                if self.ui.att_a_radio.isChecked() == False and self.ui.att_b_radio.isChecked() == False and self.ui.att_c_radio.isChecked() == False and self.ui.att_d_radio.isChecked() == False and self.ui.att_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grade in attendance", QMessageBox.Ok)

                elif self.ui.con_a_radio.isChecked() == False and self.ui.con_b_radio.isChecked() == False and self.ui.con_c_radio.isChecked() == False and self.ui.con_d_radio.isChecked() == False and self.ui.con_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grades in conduct", QMessageBox.Ok)

                elif self.ui.neat_a_radio.isChecked() == False and self.ui.neat_b_radio.isChecked() == False and self.ui.neat_c_radio.isChecked() == False and self.ui.neat_d_radio.isChecked() == False and self.ui.neat_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grades in neatness", QMessageBox.Ok)
                else:
                    self.printReport()
            except Error:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all student's scores have been recorded in all subjects", QMessageBox.Ok)
            except TypeError:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all student's scores have been recorded in all subjects", QMessageBox.Ok)


    def displayRadios(self):
        if self.ui.att_a_radio.isChecked():
            self.sec_report.ui.att_a_label.setText("v")
            self.sec_report.ui.att_b_label.setText("")
            self.sec_report.ui.att_c_label.setText("")
            self.sec_report.ui.att_d_label.setText("")
            self.sec_report.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.sec_report.ui.att_a_label.setText("")
            self.sec_report.ui.att_b_label.setText("v")
            self.sec_report.ui.att_c_label.setText("")
            self.sec_report.ui.att_d_label.setText("")
            self.sec_report.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.sec_report.ui.att_a_label.setText("")
            self.sec_report.ui.att_b_label.setText("")
            self.sec_report.ui.att_c_label.setText("v")
            self.sec_report.ui.att_d_label.setText("")
            self.sec_report.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.sec_report.ui.att_a_label.setText("")
            self.sec_report.ui.att_b_label.setText("")
            self.sec_report.ui.att_c_label.setText("")
            self.sec_report.ui.att_d_label.setText("v")
            self.sec_report.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.sec_report.ui.att_a_label.setText("")
            self.sec_report.ui.att_b_label.setText("")
            self.sec_report.ui.att_c_label.setText("")
            self.sec_report.ui.att_d_label.setText("")
            self.sec_report.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.sec_report.ui.con_a_label.setText("v")
            self.sec_report.ui.con_b_label.setText("")
            self.sec_report.ui.con_c_label.setText("")
            self.sec_report.ui.con_d_label.setText("")
            self.sec_report.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.sec_report.ui.con_a_label.setText("")
            self.sec_report.ui.con_b_label.setText("v")
            self.sec_report.ui.con_c_label.setText("")
            self.sec_report.ui.con_d_label.setText("")
            self.sec_report.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.sec_report.ui.con_a_label.setText("")
            self.sec_report.ui.con_b_label.setText("")
            self.sec_report.ui.con_c_label.setText("v")
            self.sec_report.ui.con_d_label.setText("")
            self.sec_report.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.sec_report.ui.con_a_label.setText("")
            self.sec_report.ui.con_b_label.setText("")
            self.sec_report.ui.con_c_label.setText("")
            self.sec_report.ui.con_d_label.setText("v")
            self.sec_report.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.sec_report.ui.con_a_label.setText("")
            self.sec_report.ui.con_b_label.setText("")
            self.sec_report.ui.con_c_label.setText("")
            self.sec_report.ui.con_d_label.setText("")
            self.sec_report.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.sec_report.ui.neat_a_label.setText("v")
            self.sec_report.ui.neat_b_label.setText("")
            self.sec_report.ui.neat_c_label.setText("")
            self.sec_report.ui.neat_d_label.setText("")
            self.sec_report.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.sec_report.ui.neat_a_label.setText("")
            self.sec_report.ui.neat_b_label.setText("v")
            self.sec_report.ui.neat_c_label.setText("")
            self.sec_report.ui.neat_d_label.setText("")
            self.sec_report.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.sec_report.ui.neat_a_label.setText("")
            self.sec_report.ui.neat_b_label.setText("v")
            self.sec_report.ui.neat_c_label.setText("")
            self.sec_report.ui.neat_d_label.setText("")
            self.sec_report.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.sec_report.ui.neat_a_label.setText("")
            self.sec_report.ui.neat_b_label.setText("")
            self.sec_report.ui.neat_c_label.setText("v")
            self.sec_report.ui.neat_d_label.setText("")
            self.sec_report.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.sec_report.ui.neat_a_label.setText("")
            self.sec_report.ui.neat_b_label.setText("")
            self.sec_report.ui.neat_c_label.setText("")
            self.sec_report.ui.neat_d_label.setText("v")
            self.sec_report.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.sec_report.ui.neat_a_label.setText("")
            self.sec_report.ui.neat_b_label.setText("")
            self.sec_report.ui.neat_c_label.setText("")
            self.sec_report.ui.neat_d_label.setText("")
            self.sec_report.ui.neat_e_label.setText("v")


    def printReport(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.sec_report.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

class SecReport(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SecReportForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())

        self.ui.dateTimeEdit.hide()

class SecScoresRecord2(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_SecScoreRec2ndForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic1_score_btn.clicked.connect(self.saveArabic1Scores)
        self.ui.nahwu_score_btn.clicked.connect(self.saveNahwuScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.bas_sc_score_btn.clicked.connect(self.saveBasScScores)
        self.ui.religion_score_btn.clicked.connect(self.saveReligionScores)
        self.ui.civic_score_btn.clicked.connect(self.saveCivicScores)
        self.ui.cca_score_btn.clicked.connect(self.saveCcaScores)
        self.ui.prevoc_score_btn.clicked.connect(self.savePrevocScores)
        self.ui.french_score_btn.clicked.connect(self.saveFrenchScores)
        self.ui.hausa_score_btn.clicked.connect(self.saveHausaScores)

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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic1_c1 == 0 and arabic1_c2 == 0 and arabic1_ass == 0 and arabic1_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, arabic1_c1 = ?, arabic1_c2 = ?, arabic1_ass = ?, arabic1_exam = ?, arabic1_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveNahwuScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        nahwu_c1 = self.ui.nahwu_c1_spin.value()
        nahwu_c2 = self.ui.nahwu_c2_spin.value()
        nahwu_ass = self.ui.nahwu_ass_spin.value()
        nahwu_exam = self.ui.nahwu_exam_spin.value()
        nahwu_total = nahwu_c1 + nahwu_c2 + nahwu_ass + nahwu_exam

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if nahwu_c1 == 0 and nahwu_c2 == 0 and nahwu_ass == 0 and nahwu_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, nahwu_c1 = ?, nahwu_c2 = ?, nahwu_ass = ?, nahwu_exam = ?, nahwu_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if bas_sc_c1 == 0 and bas_sc_c2 == 0 and bas_sc_ass == 0 and bas_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, bas_sc_c1 = ?, bas_sc_c2 = ?, bas_sc_ass = ?, bas_sc_exam = ?, bas_sc_total = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if religion_c1 == 0 and religion_c2 == 0 and religion_ass == 0 and religion_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, religion_c1 = ?, religion_c2 = ?, religion_ass = ?, religion_exam = ?, religion_total = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if civic_c1 == 0 and civic_c2 == 0 and civic_ass == 0 and civic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, civic_c1 = ?, civic_c2 = ?, civic_ass = ?, civic_exam = ?, civic_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()


    def saveCcaScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        cca_c1 = self.ui.cca_c1_spin.value()
        cca_c2 = self.ui.cca_c2_spin.value()
        cca_ass = self.ui.cca_ass_spin.value()
        cca_exam = self.ui.cca_exam_spin.value()
        cca_total = cca_c1 + cca_c2 + cca_ass + cca_exam

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if cca_c1 == 0 and cca_c2 == 0 and cca_ass == 0 and cca_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, cca_c1 = ?, cca_c2 = ?, cca_ass = ?, cca_exam = ?, cca_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def savePrevocScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        prevoc_c1 = self.ui.prevoc_c1_spin.value()
        prevoc_c2 = self.ui.prevoc_c2_spin.value()
        prevoc_ass = self.ui.prevoc_ass_spin.value()
        prevoc_exam = self.ui.prevoc_exam_spin.value()
        prevoc_total = prevoc_c1 + prevoc_c2 + prevoc_ass + prevoc_exam

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if prevoc_c1 == 0 and prevoc_c2 == 0 and prevoc_ass == 0 and prevoc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, prevoc_c1 = ?, prevoc_c2 = ?, prevoc_ass = ?, prevoc_exam = ?, prevoc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if french_c1 == 0 and french_c2 == 0 and french_ass == 0 and french_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, french_c1, french_c2, french_ass, french_exam, french_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, french_c1 = ?, french_c2 = ?, french_ass = ?, french_exam = ?, french_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveHausaScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        hausa_c1 = self.ui.hausa_c1_spin.value()
        hausa_c2 = self.ui.hausa_c2_spin.value()
        hausa_ass = self.ui.hausa_ass_spin.value()
        hausa_exam = self.ui.hausa_exam_spin.value()
        hausa_total = hausa_c1 + hausa_c2 + hausa_ass + hausa_exam

        cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if hausa_c1 == 0 and hausa_c2 == 0 and hausa_ass == 0 and hausa_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_second(stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, hausa_c1 = ?, hausa_c2 = ?, hausa_ass = ?, hausa_exam = ?, hausa_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total, stud_no,))
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
            cmd1 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42] + row[47] + row[52] + row[57] + row[62] + row[67]
            avg = round((all_total/1300)*100, 4)

            cmd2 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum = all_total
                avg_cum = round((total_cum/1300)*100, 4)
            elif row[68] == None:
                total_cum = all_total
                avg_cum = round((total_cum/1300)*100, 4)
            else:
                total_cum = row[68] + all_total
                avg_cum = round((total_cum/3000)*100, 4)
            cmd3 = "UPDATE t_sec_scores_second SET stud_no = ?, all_total = ?, avg = ?, total_cum = ?, avg_cum = ?  WHERE stud_no = ?"
            cur.execute(cmd3, (stud_no, all_total, avg, total_cum, avg_cum, stud_no,))
            con.commit()
            QMessageBox.information(self, "ccauting Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "ccauting Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "ccauting Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()

class SecScoresView2(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SecScore2ndForm()
        self.ui.setupUi(self)

        self.sec_report2 = SecReport2()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()


        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generateSecReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_sec_scores_second ORDER BY score_class')
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
        cmd = "SELECT * FROM t_sec_scores_second ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_sec_scores_second WHERE score_class = ? ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_sec_scores_second WHERE score_class = ? ORDER BY stud_no"
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
            QMessageBox.critical(self, "Deleting student", "ERROR: Please select student's admission number before pressing delete", QMessageBox.Ok)
        elif stud_no == "":
            QMessageBox.critical(self, "Deleting student", "ERROR: Please select a class and student's admission number before pressing delete", QMessageBox.Ok)
        else:
            cmd = "DELETE FROM t_sec_scores_second WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting student', "WARNING: Deleting will remove all the student's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generateSecReport(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        admission_no = self.ui.stud_adm_no_comboBox.currentText()
        cmd1 = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd1, (admission_no,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Printing Report", "ERROR: Please select a class and student's admission number before generating report", QMessageBox.Ok)
        else:

            self.sec_report2.ui.name_label.setText(row[1])
            self.sec_report2.ui.class_label.setText(row[3])
            self.sec_report2.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.sec_report2.ui.photo_label.setPixmap(QPixmap(pixmap))

            try:

                cmd3 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.sec_report2.ui.qur_c1_label.setText(str(row[3]))
                self.sec_report2.ui.qur_c2_label.setText(str(row[4]))
                self.sec_report2.ui.qur_ass_label.setText(str(row[5]))
                self.sec_report2.ui.qur_exam_label.setText(str(row[6]))
                self.sec_report2.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.sec_report2.ui.qur_grade_label.setText("F")
                    self.sec_report2.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.sec_report2.ui.qur_grade_label.setText("D")
                    self.sec_report2.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.sec_report2.ui.qur_grade_label.setText("C")
                    self.sec_report2.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.sec_report2.ui.qur_grade_label.setText("B")
                    self.sec_report2.ui.qur_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.qur_grade_label.setText("A")
                    self.sec_report2.ui.qur_remark_label.setText("Excellent")

                self.sec_report2.ui.ibadat_c1_label.setText(str(row[8]))
                self.sec_report2.ui.ibadat_c2_label.setText(str(row[9]))
                self.sec_report2.ui.ibadat_ass_label.setText(str(row[10]))
                self.sec_report2.ui.ibadat_exam_label.setText(str(row[11]))
                self.sec_report2.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.sec_report2.ui.ibadat_grade_label.setText("F")
                    self.sec_report2.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.sec_report2.ui.ibadat_grade_label.setText("D")
                    self.sec_report2.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.sec_report2.ui.ibadat_grade_label.setText("C")
                    self.sec_report2.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.sec_report2.ui.ibadat_grade_label.setText("B")
                    self.sec_report2.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.ibadat_grade_label.setText("A")
                    self.sec_report2.ui.ibadat_remark_label.setText("Excellent")

                self.sec_report2.ui.arabic1_c1_label.setText(str(row[13]))
                self.sec_report2.ui.arabic1_c2_label.setText(str(row[14]))
                self.sec_report2.ui.arabic1_ass_label.setText(str(row[15]))
                self.sec_report2.ui.arabic1_exam_label.setText(str(row[16]))
                self.sec_report2.ui.arabic1_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.sec_report2.ui.arabic1_grade_label.setText("F")
                    self.sec_report2.ui.arabic1_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.sec_report2.ui.arabic1_grade_label.setText("D")
                    self.sec_report2.ui.arabic1_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.sec_report2.ui.arabic1_grade_label.setText("C")
                    self.sec_report2.ui.arabic1_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.sec_report2.ui.arabic1_grade_label.setText("B")
                    self.sec_report2.ui.arabic1_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.arabic1_grade_label.setText("A")
                    self.sec_report2.ui.arabic1_remark_label.setText("Excellent")

                self.sec_report2.ui.nahwu_c1_label.setText(str(row[18]))
                self.sec_report2.ui.nahwu_c2_label.setText(str(row[19]))
                self.sec_report2.ui.nahwu_ass_label.setText(str(row[20]))
                self.sec_report2.ui.nahwu_exam_label.setText(str(row[21]))
                self.sec_report2.ui.nahwu_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.sec_report2.ui.nahwu_grade_label.setText("F")
                    self.sec_report2.ui.nahwu_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.sec_report2.ui.nahwu_grade_label.setText("D")
                    self.sec_report2.ui.nahwu_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.sec_report2.ui.nahwu_grade_label.setText("C")
                    self.sec_report2.ui.nahwu_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.sec_report2.ui.nahwu_grade_label.setText("B")
                    self.sec_report2.ui.nahwu_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.nahwu_grade_label.setText("A")
                    self.sec_report2.ui.nahwu_remark_label.setText("Excellent")

                self.sec_report2.ui.eng_c1_label.setText(str(row[23]))
                self.sec_report2.ui.eng_c2_label.setText(str(row[24]))
                self.sec_report2.ui.eng_ass_label.setText(str(row[25]))
                self.sec_report2.ui.eng_exam_label.setText(str(row[26]))
                self.sec_report2.ui.eng_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.sec_report2.ui.eng_grade_label.setText("F")
                    self.sec_report2.ui.eng_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.sec_report2.ui.eng_grade_label.setText("D")
                    self.sec_report2.ui.eng_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.sec_report2.ui.eng_grade_label.setText("C")
                    self.sec_report2.ui.eng_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.sec_report2.ui.eng_grade_label.setText("B")
                    self.sec_report2.ui.eng_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.eng_grade_label.setText("A")
                    self.sec_report2.ui.eng_remark_label.setText("Excellent")

                self.sec_report2.ui.math_c1_label.setText(str(row[28]))
                self.sec_report2.ui.math_c2_label.setText(str(row[29]))
                self.sec_report2.ui.math_ass_label.setText(str(row[30]))
                self.sec_report2.ui.math_exam_label.setText(str(row[31]))
                self.sec_report2.ui.math_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.sec_report2.ui.math_grade_label.setText("F")
                    self.sec_report2.ui.math_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.sec_report2.ui.math_grade_label.setText("D")
                    self.sec_report2.ui.math_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.sec_report2.ui.math_grade_label.setText("C")
                    self.sec_report2.ui.math_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.sec_report2.ui.math_grade_label.setText("B")
                    self.sec_report2.ui.math_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.math_grade_label.setText("A")
                    self.sec_report2.ui.math_remark_label.setText("Excellent")

                self.sec_report2.ui.bas_sc_c1_label.setText(str(row[33]))
                self.sec_report2.ui.bas_sc_c2_label.setText(str(row[34]))
                self.sec_report2.ui.bas_sc_ass_label.setText(str(row[35]))
                self.sec_report2.ui.bas_sc_exam_label.setText(str(row[36]))
                self.sec_report2.ui.bas_sc_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.sec_report2.ui.bas_sc_grade_label.setText("F")
                    self.sec_report2.ui.bas_sc_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.sec_report2.ui.bas_sc_grade_label.setText("D")
                    self.sec_report2.ui.bas_sc_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.sec_report2.ui.bas_sc_grade_label.setText("C")
                    self.sec_report2.ui.bas_sc_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.sec_report2.ui.bas_sc_grade_label.setText("B")
                    self.sec_report2.ui.bas_sc_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.bas_sc_grade_label.setText("A")
                    self.sec_report2.ui.bas_sc_remark_label.setText("Excellent")

                self.sec_report2.ui.religion_c1_label.setText(str(row[38]))
                self.sec_report2.ui.religion_c2_label.setText(str(row[39]))
                self.sec_report2.ui.religion_ass_label.setText(str(row[40]))
                self.sec_report2.ui.religion_exam_label.setText(str(row[41]))
                self.sec_report2.ui.religion_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.sec_report2.ui.religion_grade_label.setText("F")
                    self.sec_report2.ui.religion_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.sec_report2.ui.religion_grade_label.setText("D")
                    self.sec_report2.ui.religion_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.sec_report2.ui.religion_grade_label.setText("C")
                    self.sec_report2.ui.religion_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.sec_report2.ui.religion_grade_label.setText("B")
                    self.sec_report2.ui.religion_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.religion_grade_label.setText("A")
                    self.sec_report2.ui.religion_remark_label.setText("Excellent")

                self.sec_report2.ui.civic_c1_label.setText(str(row[43]))
                self.sec_report2.ui.civic_c2_label.setText(str(row[44]))
                self.sec_report2.ui.civic_ass_label.setText(str(row[45]))
                self.sec_report2.ui.civic_exam_label.setText(str(row[46]))
                self.sec_report2.ui.civic_total_label.setText(str(row[47]))

                if row[47] < 40:
                    self.sec_report2.ui.civic_grade_label.setText("F")
                    self.sec_report2.ui.civic_remark_label.setText("Fail")
                elif row[47] >= 40 and row[47] < 50:
                    self.sec_report2.ui.civic_grade_label.setText("D")
                    self.sec_report2.ui.civic_remark_label.setText("Pass")
                elif row[47] >= 50 and row[47] < 60:
                    self.sec_report2.ui.civic_grade_label.setText("C")
                    self.sec_report2.ui.civic_remark_label.setText("Good")
                elif row[47] >= 60 and row[47] < 70:
                    self.sec_report2.ui.civic_grade_label.setText("B")
                    self.sec_report2.ui.civic_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.civic_grade_label.setText("A")
                    self.sec_report2.ui.civic_remark_label.setText("Excellent")

                self.sec_report2.ui.cca_c1_label.setText(str(row[48]))
                self.sec_report2.ui.cca_c2_label.setText(str(row[49]))
                self.sec_report2.ui.cca_ass_label.setText(str(row[50]))
                self.sec_report2.ui.cca_exam_label.setText(str(row[51]))
                self.sec_report2.ui.cca_total_label.setText(str(row[52]))

                if row[52] < 40:
                    self.sec_report2.ui.cca_grade_label.setText("F")
                    self.sec_report2.ui.cca_remark_label.setText("Fail")
                elif row[52] >= 40 and row[52] < 50:
                    self.sec_report2.ui.cca_grade_label.setText("D")
                    self.sec_report2.ui.cca_remark_label.setText("Pass")
                elif row[52] >= 50 and row[52] < 60:
                    self.sec_report2.ui.cca_grade_label.setText("C")
                    self.sec_report2.ui.cca_remark_label.setText("Good")
                elif row[52] >= 60 and row[52] < 70:
                    self.sec_report2.ui.cca_grade_label.setText("B")
                    self.sec_report2.ui.cca_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.cca_grade_label.setText("A")
                    self.sec_report2.ui.cca_remark_label.setText("Excellent")

                self.sec_report2.ui.prevoc_c1_label.setText(str(row[53]))
                self.sec_report2.ui.prevoc_c2_label.setText(str(row[54]))
                self.sec_report2.ui.prevoc_ass_label.setText(str(row[55]))
                self.sec_report2.ui.prevoc_exam_label.setText(str(row[56]))
                self.sec_report2.ui.prevoc_total_label.setText(str(row[57]))

                if row[57] < 40:
                    self.sec_report2.ui.prevoc_grade_label.setText("F")
                    self.sec_report2.ui.prevoc_remark_label.setText("Fail")
                elif row[57] >= 40 and row[57] < 50:
                    self.sec_report2.ui.prevoc_grade_label.setText("D")
                    self.sec_report2.ui.prevoc_remark_label.setText("Pass")
                elif row[57] >= 50 and row[57] < 60:
                    self.sec_report2.ui.prevoc_grade_label.setText("C")
                    self.sec_report2.ui.prevoc_remark_label.setText("Good")
                elif row[57] >= 60 and row[57] < 70:
                    self.sec_report2.ui.prevoc_grade_label.setText("B")
                    self.sec_report2.ui.prevoc_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.prevoc_grade_label.setText("A")
                    self.sec_report2.ui.prevoc_remark_label.setText("Excellent")

                self.sec_report2.ui.french_c1_label.setText(str(row[58]))
                self.sec_report2.ui.french_c2_label.setText(str(row[59]))
                self.sec_report2.ui.french_ass_label.setText(str(row[60]))
                self.sec_report2.ui.french_exam_label.setText(str(row[61]))
                self.sec_report2.ui.french_total_label.setText(str(row[62]))

                if row[62] < 40:
                    self.sec_report2.ui.french_grade_label.setText("F")
                    self.sec_report2.ui.french_remark_label.setText("Fail")
                elif row[62] >= 40 and row[62] < 50:
                    self.sec_report2.ui.french_grade_label.setText("D")
                    self.sec_report2.ui.french_remark_label.setText("Pass")
                elif row[62] >= 50 and row[62] < 60:
                    self.sec_report2.ui.french_grade_label.setText("C")
                    self.sec_report2.ui.french_remark_label.setText("Good")
                elif row[62] >= 60 and row[62] < 70:
                    self.sec_report2.ui.french_grade_label.setText("B")
                    self.sec_report2.ui.french_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.french_grade_label.setText("A")
                    self.sec_report2.ui.french_remark_label.setText("Excellent")

                self.sec_report2.ui.hausa_c1_label.setText(str(row[63]))
                self.sec_report2.ui.hausa_c2_label.setText(str(row[64]))
                self.sec_report2.ui.hausa_ass_label.setText(str(row[65]))
                self.sec_report2.ui.hausa_exam_label.setText(str(row[66]))
                self.sec_report2.ui.hausa_total_label.setText(str(row[67]))

                if row[67] < 40:
                    self.sec_report2.ui.hausa_grade_label.setText("F")
                    self.sec_report2.ui.hausa_remark_label.setText("Fail")
                elif row[67] >= 40 and row[67] < 50:
                    self.sec_report2.ui.hausa_grade_label.setText("D")
                    self.sec_report2.ui.hausa_remark_label.setText("Pass")
                elif row[67] >= 50 and row[67] < 60:
                    self.sec_report2.ui.hausa_grade_label.setText("C")
                    self.sec_report2.ui.hausa_remark_label.setText("Good")
                elif row[67] >= 60 and row[67] < 70:
                    self.sec_report2.ui.hausa_grade_label.setText("B")
                    self.sec_report2.ui.hausa_remark_label.setText("Very Good")
                else:
                    self.sec_report2.ui.hausa_grade_label.setText("A")
                    self.sec_report2.ui.hausa_remark_label.setText("Excellent")

                self.sec_report2.ui.total_scores2_label.setText(str(row[68]))
                self.sec_report2.ui.avg2_label.setText(str(row[69]))
                self.sec_report2.ui.total_cum_label.setText(str(row[70]))
                self.sec_report2.ui.avg_cum_label.setText(str(row[71]))

                if row[69] < 40:
                    self.sec_report2.ui.master_com_label.setText("Bad result. Be careful.")
                    self.sec_report2.ui.head_com_label.setText("Bad result.")
                elif row[69] >= 40 and row[69] < 50:
                    self.sec_report2.ui.master_com_label.setText("Weak result. Work hard.")
                    self.sec_report2.ui.head_com_label.setText("Weak result.")
                elif row[69] >= 50 and row[69] < 60:
                    self.sec_report2.ui.master_com_label.setText("Fair result. Work hard.")
                    self.sec_report2.ui.head_com_label.setText("Fair result.")
                elif row[69] >= 60 and row[69] < 70:
                    self.sec_report2.ui.master_com_label.setText("Good result. Put more effort.")
                    self.sec_report2.ui.head_com_label.setText("Good result.")
                else:
                    self.sec_report2.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.sec_report2.ui.head_com_label.setText("Excellent result.")

                cmd9 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
                cur.execute(cmd9, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.sec_report2.ui.total_scores_label.setText("None")
                    self.sec_report2.ui.avg_label.setText("None")
                elif row[68] == None and row[69] == None:
                    self.sec_report2.ui.total_scores_label.setText("None")
                    self.sec_report2.ui.avg_label.setText("None")
                else:
                    self.sec_report2.ui.total_scores_label.setText(str(row[68]))
                    self.sec_report2.ui.avg_label.setText(str(row[69]))

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.sec_report2.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.sec_report2.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.sec_report2.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.sec_report2.ui.fees_label.setText(row[4])

                cmd8 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd8)
                row = cur.fetchone()
                self.sec_report2.ui.session_label.setText(row[2])

                if self.ui.att_a_radio.isChecked() == False and self.ui.att_b_radio.isChecked() == False and self.ui.att_c_radio.isChecked() == False and self.ui.att_d_radio.isChecked() == False and self.ui.att_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grade in attendance", QMessageBox.Ok)

                elif self.ui.con_a_radio.isChecked() == False and self.ui.con_b_radio.isChecked() == False and self.ui.con_c_radio.isChecked() == False and self.ui.con_d_radio.isChecked() == False and self.ui.con_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grades in conduct", QMessageBox.Ok)

                elif self.ui.neat_a_radio.isChecked() == False and self.ui.neat_b_radio.isChecked() == False and self.ui.neat_c_radio.isChecked() == False and self.ui.neat_d_radio.isChecked() == False and self.ui.neat_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grades in neatness", QMessageBox.Ok)
                else:
                    self.printReport2()
            except Error:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all student's scores have been recorded in all subjects", QMessageBox.Ok)
            except TypeError:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all student's scores have been recorded in all subjects", QMessageBox.Ok)

    def displayRadios(self):
        if self.ui.att_a_radio.isChecked():
            self.sec_report2.ui.att_a_label.setText("v")
            self.sec_report2.ui.att_b_label.setText("")
            self.sec_report2.ui.att_c_label.setText("")
            self.sec_report2.ui.att_d_label.setText("")
            self.sec_report2.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.sec_report2.ui.att_a_label.setText("")
            self.sec_report2.ui.att_b_label.setText("v")
            self.sec_report2.ui.att_c_label.setText("")
            self.sec_report2.ui.att_d_label.setText("")
            self.sec_report2.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.sec_report2.ui.att_a_label.setText("")
            self.sec_report2.ui.att_b_label.setText("")
            self.sec_report2.ui.att_c_label.setText("v")
            self.sec_report2.ui.att_d_label.setText("")
            self.sec_report2.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.sec_report2.ui.att_a_label.setText("")
            self.sec_report2.ui.att_b_label.setText("")
            self.sec_report2.ui.att_c_label.setText("")
            self.sec_report2.ui.att_d_label.setText("v")
            self.sec_report2.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.sec_report2.ui.att_a_label.setText("")
            self.sec_report2.ui.att_b_label.setText("")
            self.sec_report2.ui.att_c_label.setText("")
            self.sec_report2.ui.att_d_label.setText("")
            self.sec_report2.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.sec_report2.ui.con_a_label.setText("v")
            self.sec_report2.ui.con_b_label.setText("")
            self.sec_report2.ui.con_c_label.setText("")
            self.sec_report2.ui.con_d_label.setText("")
            self.sec_report2.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.sec_report2.ui.con_a_label.setText("")
            self.sec_report2.ui.con_b_label.setText("v")
            self.sec_report2.ui.con_c_label.setText("")
            self.sec_report2.ui.con_d_label.setText("")
            self.sec_report2.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.sec_report2.ui.con_a_label.setText("")
            self.sec_report2.ui.con_b_label.setText("")
            self.sec_report2.ui.con_c_label.setText("v")
            self.sec_report2.ui.con_d_label.setText("")
            self.sec_report2.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.sec_report2.ui.con_a_label.setText("")
            self.sec_report2.ui.con_b_label.setText("")
            self.sec_report2.ui.con_c_label.setText("")
            self.sec_report2.ui.con_d_label.setText("v")
            self.sec_report2.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.sec_report2.ui.con_a_label.setText("")
            self.sec_report2.ui.con_b_label.setText("")
            self.sec_report2.ui.con_c_label.setText("")
            self.sec_report2.ui.con_d_label.setText("")
            self.sec_report2.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.sec_report2.ui.neat_a_label.setText("v")
            self.sec_report2.ui.neat_b_label.setText("")
            self.sec_report2.ui.neat_c_label.setText("")
            self.sec_report2.ui.neat_d_label.setText("")
            self.sec_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.sec_report2.ui.neat_a_label.setText("")
            self.sec_report2.ui.neat_b_label.setText("v")
            self.sec_report2.ui.neat_c_label.setText("")
            self.sec_report2.ui.neat_d_label.setText("")
            self.sec_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.sec_report2.ui.neat_a_label.setText("")
            self.sec_report2.ui.neat_b_label.setText("v")
            self.sec_report2.ui.neat_c_label.setText("")
            self.sec_report2.ui.neat_d_label.setText("")
            self.sec_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.sec_report2.ui.neat_a_label.setText("")
            self.sec_report2.ui.neat_b_label.setText("")
            self.sec_report2.ui.neat_c_label.setText("v")
            self.sec_report2.ui.neat_d_label.setText("")
            self.sec_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.sec_report2.ui.neat_a_label.setText("")
            self.sec_report2.ui.neat_b_label.setText("")
            self.sec_report2.ui.neat_c_label.setText("")
            self.sec_report2.ui.neat_d_label.setText("v")
            self.sec_report2.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.sec_report2.ui.neat_a_label.setText("")
            self.sec_report2.ui.neat_b_label.setText("")
            self.sec_report2.ui.neat_c_label.setText("")
            self.sec_report2.ui.neat_d_label.setText("")
            self.sec_report2.ui.neat_e_label.setText("v")


    def printReport2(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.sec_report2.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

class SecReport2(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SecReport2ndForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())

        self.ui.dateTimeEdit.hide()


class SecScoresRecord3(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_SecScoreRec3rdForm()
        self.ui.setupUi(self)

        self.displayClasses()

        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

        self.ui.qur_score_btn.clicked.connect(self.saveQurScores)
        self.ui.ibadat_score_btn.clicked.connect(self.saveIbadatScores)
        self.ui.arabic1_score_btn.clicked.connect(self.saveArabic1Scores)
        self.ui.nahwu_score_btn.clicked.connect(self.saveNahwuScores)
        self.ui.eng_score_btn.clicked.connect(self.saveEnglishScores)
        self.ui.math_score_btn.clicked.connect(self.saveMathScores)
        self.ui.bas_sc_score_btn.clicked.connect(self.saveBasScScores)
        self.ui.religion_score_btn.clicked.connect(self.saveReligionScores)
        self.ui.civic_score_btn.clicked.connect(self.saveCivicScores)
        self.ui.cca_score_btn.clicked.connect(self.saveCcaScores)
        self.ui.prevoc_score_btn.clicked.connect(self.savePrevocScores)
        self.ui.french_score_btn.clicked.connect(self.saveFrenchScores)
        self.ui.hausa_score_btn.clicked.connect(self.saveHausaScores)

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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if qur_c1 == 0 and qur_c2 == 0 and qur_ass == 0 and qur_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, score_class, qur_c1, qur_c2, qur_ass, qur_exam, qur_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, score_class = ?, qur_c1 = ?, qur_c2 = ?, qur_ass = ?, qur_exam = ?, qur_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if ibadat_c1 == 0 and ibadat_c2 == 0 and ibadat_ass == 0 and ibadat_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, ibadat_c1, ibadat_c2, ibadat_ass, ibadat_exam, ibadat_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, ibadat_c1 = ?, ibadat_c2 = ?, ibadat_ass = ?, ibadat_exam = ?, ibadat_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if arabic1_c1 == 0 and arabic1_c2 == 0 and arabic1_ass == 0 and arabic1_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, arabic1_c1 = ?, arabic1_c2 = ?, arabic1_ass = ?, arabic1_exam = ?, arabic1_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, arabic1_c1, arabic1_c2, arabic1_ass, arabic1_exam, arabic1_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveNahwuScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        nahwu_c1 = self.ui.nahwu_c1_spin.value()
        nahwu_c2 = self.ui.nahwu_c2_spin.value()
        nahwu_ass = self.ui.nahwu_ass_spin.value()
        nahwu_exam = self.ui.nahwu_exam_spin.value()
        nahwu_total = nahwu_c1 + nahwu_c2 + nahwu_ass + nahwu_exam

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if nahwu_c1 == 0 and nahwu_c2 == 0 and nahwu_ass == 0 and nahwu_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, nahwu_c1 = ?, nahwu_c2 = ?, nahwu_ass = ?, nahwu_exam = ?, nahwu_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, nahwu_c1, nahwu_c2, nahwu_ass, nahwu_exam, nahwu_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if eng_c1 == 0 and eng_c2 == 0 and eng_ass == 0 and eng_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, eng_c1, eng_c2, eng_ass, eng_exam, eng_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, eng_c1 = ?, eng_c2 = ?, eng_ass = ?, eng_exam = ?, eng_total  = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if math_c1 == 0 and math_c2 == 0 and math_ass == 0 and math_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, math_c1, math_c2, math_ass, math_exam, math_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, math_c1 = ?, math_c2 = ?, math_ass = ?, math_exam = ?, math_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, math_c1, math_c2, math_ass, math_exam, math_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if bas_sc_c1 == 0 and bas_sc_c2 == 0 and bas_sc_ass == 0 and bas_sc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, bas_sc_c1, bas_sc_c2, bas_sc_ass, bas_sc_exam, bas_sc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, bas_sc_c1 = ?, bas_sc_c2 = ?, bas_sc_ass = ?, bas_sc_exam = ?, bas_sc_total = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if religion_c1 == 0 and religion_c2 == 0 and religion_ass == 0 and religion_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, religion_c1, religion_c2, religion_ass, religion_exam, religion_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, religion_c1 = ?, religion_c2 = ?, religion_ass = ?, religion_exam = ?, religion_total = ? WHERE stud_no = ?"
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if civic_c1 == 0 and civic_c2 == 0 and civic_ass == 0 and civic_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, civic_c1 = ?, civic_c2 = ?, civic_ass = ?, civic_exam = ?, civic_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, civic_c1, civic_c2, civic_ass, civic_exam, civic_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()


    def saveCcaScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        cca_c1 = self.ui.cca_c1_spin.value()
        cca_c2 = self.ui.cca_c2_spin.value()
        cca_ass = self.ui.cca_ass_spin.value()
        cca_exam = self.ui.cca_exam_spin.value()
        cca_total = cca_c1 + cca_c2 + cca_ass + cca_exam

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if cca_c1 == 0 and cca_c2 == 0 and cca_ass == 0 and cca_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, cca_c1 = ?, cca_c2 = ?, cca_ass = ?, cca_exam = ?, cca_total  = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, cca_c1, cca_c2, cca_ass, cca_exam, cca_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def savePrevocScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        prevoc_c1 = self.ui.prevoc_c1_spin.value()
        prevoc_c2 = self.ui.prevoc_c2_spin.value()
        prevoc_ass = self.ui.prevoc_ass_spin.value()
        prevoc_exam = self.ui.prevoc_exam_spin.value()
        prevoc_total = prevoc_c1 + prevoc_c2 + prevoc_ass + prevoc_exam

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if prevoc_c1 == 0 and prevoc_c2 == 0 and prevoc_ass == 0 and prevoc_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, prevoc_c1 = ?, prevoc_c2 = ?, prevoc_ass = ?, prevoc_exam = ?, prevoc_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, prevoc_c1, prevoc_c2, prevoc_ass, prevoc_exam, prevoc_total, stud_no,))
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

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if french_c1 == 0 and french_c2 == 0 and french_ass == 0 and french_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, french_c1, french_c2, french_ass, french_exam, french_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, french_c1 = ?, french_c2 = ?, french_ass = ?, french_exam = ?, french_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, french_c1, french_c2, french_ass, french_exam, french_total, stud_no,))
                con.commit()
                QMessageBox.information(self, "Modifing Score", "Student's scores modified successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "Saving Score", "ERROR: Please select student's class and admission number", QMessageBox.Ok)
        finally:
            con.close()

    def saveHausaScores(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_adm_no_comboBox.currentText()

        hausa_c1 = self.ui.hausa_c1_spin.value()
        hausa_c2 = self.ui.hausa_c2_spin.value()
        hausa_ass = self.ui.hausa_ass_spin.value()
        hausa_exam = self.ui.hausa_exam_spin.value()
        hausa_total = hausa_c1 + hausa_c2 + hausa_ass + hausa_exam

        cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
        try:
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            if hausa_c1 == 0 and hausa_c2 == 0 and hausa_ass == 0 and hausa_exam == 0:
                QMessageBox.critical(self, 'Saving Score', "ERROR: Please fill in scores before saving", QMessageBox.Ok)
            elif row == None:
                cmd2 = "INSERT INTO t_sec_scores_third(stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(cmd2, (stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total,))
                QMessageBox.information(self, 'Saving Score', "Student's scores saved successfully", QMessageBox.Ok)
                con.commit()
            else:
                cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, hausa_c1 = ?, hausa_c2 = ?, hausa_ass = ?, hausa_exam = ?, hausa_total = ? WHERE stud_no = ?"
                cur.execute(cmd3, (stud_no, hausa_c1, hausa_c2, hausa_ass, hausa_exam, hausa_total, stud_no,))
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
            cmd1 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
            cur.execute(cmd1, (stud_no,))
            row = cur.fetchone()
            all_total = row[7] + row[12] + row[17] + row[22] + row[27] + row[32] + row[37] + row[42] + row[47] + row[52] + row[57] + row[62] + row[67]
            avg = round((all_total/1300)*100, 4)

            cmd0 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
            cur.execute(cmd0, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum0 = all_total
            elif row[68] == None:
                total_cum0 = all_total
            else:
                total_cum0 = row[68] + all_total

            cmd2 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
            cur.execute(cmd2, (stud_no,))
            row = cur.fetchone()
            if row == None:
                total_cum = total_cum0
                avg_cum = round((total_cum/2600)*100, 4)
            elif row[68] == row[70]:
                total_cum = row[68] + total_cum0
                avg_cum = round((total_cum/2600)*100, 4)
            else:
                total_cum = row[68] + total_cum0
                avg_cum = round((total_cum/3900)*100, 4)

            cmd3 = "UPDATE t_sec_scores_third SET stud_no = ?, all_total = ?, avg = ?, total_cum = ?, avg_cum = ?  WHERE stud_no = ?"
            cur.execute(cmd3, (stud_no, all_total, avg, total_cum, avg_cum, stud_no,))
            con.commit()
            QMessageBox.information(self, "ccauting Total and Average", "Student's Total and Average Saved Successfully", QMessageBox.Ok)
        except Error:
            QMessageBox.critical(self, "ccauting Total Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        except TypeError:
            QMessageBox.critical(self, "ccauting Total and Average", "ERROR:\n-Please select student's class and admission number\n-Also, ensure you have saved all students' scores in all subjects", QMessageBox.Ok)
        finally:
            con.close()

class SecScoresView3(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SecScore3rdForm()
        self.ui.setupUi(self)

        self.sec_report3 = SecReport3()

        self.displayClasses()
        self.listStudsScores()

        self.ui.switch_back_btn.hide()


        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)
        self.ui.class_comboBox.currentTextChanged.connect(self.displayStuds)
        self.ui.switch_back_btn.clicked.connect(self.listStudsScores)
        self.ui.report_gen_btn.clicked.connect(self.displayRadios)
        self.ui.report_gen_btn.clicked.connect(self.generateSecReport)
        self.ui.del_btn.clicked.connect(self.deleteStud)
        self.ui.stud_adm_no_comboBox.currentTextChanged.connect(self.displayName)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_sec_scores_third ORDER BY score_class')
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
        cmd = "SELECT * FROM t_sec_scores_third ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_sec_scores_third WHERE score_class = ? ORDER BY stud_no"
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
        cmd = "SELECT * FROM t_sec_scores_third WHERE score_class = ? ORDER BY stud_no"
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
            QMessageBox.critical(self, "Deleting student", "ERROR: Please select student's admission number before pressing delete", QMessageBox.Ok)
        elif stud_no == "":
            QMessageBox.critical(self, "Deleting student", "ERROR: Please select a class and student's admission number before pressing delete", QMessageBox.Ok)
        else:
            cmd = "DELETE FROM t_sec_scores_third WHERE stud_no = ?"
            buttonReply = QMessageBox.warning(self, 'Deleting student', "WARNING: Deleting will remove all the student's score records in the class. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.listClass()
                con.close()

    def generateSecReport(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        admission_no = self.ui.stud_adm_no_comboBox.currentText()
        cmd1 = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd1, (admission_no,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Printing Report", "ERROR: Please select a class and student's admission number before generating report", QMessageBox.Ok)
        else:

            self.sec_report3.ui.name_label.setText(row[1])
            self.sec_report3.ui.class_label.setText(row[3])
            self.sec_report3.ui.sex_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.sec_report3.ui.photo_label.setPixmap(QPixmap(pixmap))

            try:        
                cmd3 = "SELECT * FROM t_sec_scores_third WHERE stud_no = ?"
                cur.execute(cmd3, (admission_no,))
                row = cur.fetchone()
                self.sec_report3.ui.qur_c1_label.setText(str(row[3]))
                self.sec_report3.ui.qur_c2_label.setText(str(row[4]))
                self.sec_report3.ui.qur_ass_label.setText(str(row[5]))
                self.sec_report3.ui.qur_exam_label.setText(str(row[6]))
                self.sec_report3.ui.qur_total_label.setText(str(row[7]))

                if row[7] < 40:
                    self.sec_report3.ui.qur_grade_label.setText("F")
                    self.sec_report3.ui.qur_remark_label.setText("Fail")
                elif row[7] >= 40 and row[7] < 50:
                    self.sec_report3.ui.qur_grade_label.setText("D")
                    self.sec_report3.ui.qur_remark_label.setText("Pass")
                elif row[7] >= 50 and row[7] < 60:
                    self.sec_report3.ui.qur_grade_label.setText("C")
                    self.sec_report3.ui.qur_remark_label.setText("Good")
                elif row[7] >= 60 and row[7] < 70:
                    self.sec_report3.ui.qur_grade_label.setText("B")
                    self.sec_report3.ui.qur_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.qur_grade_label.setText("A")
                    self.sec_report3.ui.qur_remark_label.setText("Excellent")

                self.sec_report3.ui.ibadat_c1_label.setText(str(row[8]))
                self.sec_report3.ui.ibadat_c2_label.setText(str(row[9]))
                self.sec_report3.ui.ibadat_ass_label.setText(str(row[10]))
                self.sec_report3.ui.ibadat_exam_label.setText(str(row[11]))
                self.sec_report3.ui.ibadat_total_label.setText(str(row[12]))

                if row[12] < 40:
                    self.sec_report3.ui.ibadat_grade_label.setText("F")
                    self.sec_report3.ui.ibadat_remark_label.setText("Fail")
                elif row[12] >= 40 and row[12] < 50:
                    self.sec_report3.ui.ibadat_grade_label.setText("D")
                    self.sec_report3.ui.ibadat_remark_label.setText("Pass")
                elif row[12] >= 50 and row[12] < 60:
                    self.sec_report3.ui.ibadat_grade_label.setText("C")
                    self.sec_report3.ui.ibadat_remark_label.setText("Good")
                elif row[12] >= 60 and row[12] < 70:
                    self.sec_report3.ui.ibadat_grade_label.setText("B")
                    self.sec_report3.ui.ibadat_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.ibadat_grade_label.setText("A")
                    self.sec_report3.ui.ibadat_remark_label.setText("Excellent")

                self.sec_report3.ui.arabic1_c1_label.setText(str(row[13]))
                self.sec_report3.ui.arabic1_c2_label.setText(str(row[14]))
                self.sec_report3.ui.arabic1_ass_label.setText(str(row[15]))
                self.sec_report3.ui.arabic1_exam_label.setText(str(row[16]))
                self.sec_report3.ui.arabic1_total_label.setText(str(row[17]))

                if row[17] < 40:
                    self.sec_report3.ui.arabic1_grade_label.setText("F")
                    self.sec_report3.ui.arabic1_remark_label.setText("Fail")
                elif row[17] >= 40 and row[17] < 50:
                    self.sec_report3.ui.arabic1_grade_label.setText("D")
                    self.sec_report3.ui.arabic1_remark_label.setText("Pass")
                elif row[17] >= 50 and row[17] < 60:
                    self.sec_report3.ui.arabic1_grade_label.setText("C")
                    self.sec_report3.ui.arabic1_remark_label.setText("Good")
                elif row[17] >= 60 and row[17] < 70:
                    self.sec_report3.ui.arabic1_grade_label.setText("B")
                    self.sec_report3.ui.arabic1_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.arabic1_grade_label.setText("A")
                    self.sec_report3.ui.arabic1_remark_label.setText("Excellent")

                self.sec_report3.ui.nahwu_c1_label.setText(str(row[18]))
                self.sec_report3.ui.nahwu_c2_label.setText(str(row[19]))
                self.sec_report3.ui.nahwu_ass_label.setText(str(row[20]))
                self.sec_report3.ui.nahwu_exam_label.setText(str(row[21]))
                self.sec_report3.ui.nahwu_total_label.setText(str(row[22]))

                if row[22] < 40:
                    self.sec_report3.ui.nahwu_grade_label.setText("F")
                    self.sec_report3.ui.nahwu_remark_label.setText("Fail")
                elif row[22] >= 40 and row[22] < 50:
                    self.sec_report3.ui.nahwu_grade_label.setText("D")
                    self.sec_report3.ui.nahwu_remark_label.setText("Pass")
                elif row[22] >= 50 and row[22] < 60:
                    self.sec_report3.ui.nahwu_grade_label.setText("C")
                    self.sec_report3.ui.nahwu_remark_label.setText("Good")
                elif row[22] >= 60 and row[22] < 70:
                    self.sec_report3.ui.nahwu_grade_label.setText("B")
                    self.sec_report3.ui.nahwu_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.nahwu_grade_label.setText("A")
                    self.sec_report3.ui.nahwu_remark_label.setText("Excellent")

                self.sec_report3.ui.eng_c1_label.setText(str(row[23]))
                self.sec_report3.ui.eng_c2_label.setText(str(row[24]))
                self.sec_report3.ui.eng_ass_label.setText(str(row[25]))
                self.sec_report3.ui.eng_exam_label.setText(str(row[26]))
                self.sec_report3.ui.eng_total_label.setText(str(row[27]))

                if row[27] < 40:
                    self.sec_report3.ui.eng_grade_label.setText("F")
                    self.sec_report3.ui.eng_remark_label.setText("Fail")
                elif row[27] >= 40 and row[27] < 50:
                    self.sec_report3.ui.eng_grade_label.setText("D")
                    self.sec_report3.ui.eng_remark_label.setText("Pass")
                elif row[27] >= 50 and row[27] < 60:
                    self.sec_report3.ui.eng_grade_label.setText("C")
                    self.sec_report3.ui.eng_remark_label.setText("Good")
                elif row[27] >= 60 and row[27] < 70:
                    self.sec_report3.ui.eng_grade_label.setText("B")
                    self.sec_report3.ui.eng_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.eng_grade_label.setText("A")
                    self.sec_report3.ui.eng_remark_label.setText("Excellent")

                self.sec_report3.ui.math_c1_label.setText(str(row[28]))
                self.sec_report3.ui.math_c2_label.setText(str(row[29]))
                self.sec_report3.ui.math_ass_label.setText(str(row[30]))
                self.sec_report3.ui.math_exam_label.setText(str(row[31]))
                self.sec_report3.ui.math_total_label.setText(str(row[32]))

                if row[32] < 40:
                    self.sec_report3.ui.math_grade_label.setText("F")
                    self.sec_report3.ui.math_remark_label.setText("Fail")
                elif row[32] >= 40 and row[32] < 50:
                    self.sec_report3.ui.math_grade_label.setText("D")
                    self.sec_report3.ui.math_remark_label.setText("Pass")
                elif row[32] >= 50 and row[32] < 60:
                    self.sec_report3.ui.math_grade_label.setText("C")
                    self.sec_report3.ui.math_remark_label.setText("Good")
                elif row[32] >= 60 and row[32] < 70:
                    self.sec_report3.ui.math_grade_label.setText("B")
                    self.sec_report3.ui.math_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.math_grade_label.setText("A")
                    self.sec_report3.ui.math_remark_label.setText("Excellent")

                self.sec_report3.ui.bas_sc_c1_label.setText(str(row[33]))
                self.sec_report3.ui.bas_sc_c2_label.setText(str(row[34]))
                self.sec_report3.ui.bas_sc_ass_label.setText(str(row[35]))
                self.sec_report3.ui.bas_sc_exam_label.setText(str(row[36]))
                self.sec_report3.ui.bas_sc_total_label.setText(str(row[37]))

                if row[37] < 40:
                    self.sec_report3.ui.bas_sc_grade_label.setText("F")
                    self.sec_report3.ui.bas_sc_remark_label.setText("Fail")
                elif row[37] >= 40 and row[37] < 50:
                    self.sec_report3.ui.bas_sc_grade_label.setText("D")
                    self.sec_report3.ui.bas_sc_remark_label.setText("Pass")
                elif row[37] >= 50 and row[37] < 60:
                    self.sec_report3.ui.bas_sc_grade_label.setText("C")
                    self.sec_report3.ui.bas_sc_remark_label.setText("Good")
                elif row[37] >= 60 and row[37] < 70:
                    self.sec_report3.ui.bas_sc_grade_label.setText("B")
                    self.sec_report3.ui.bas_sc_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.bas_sc_grade_label.setText("A")
                    self.sec_report3.ui.bas_sc_remark_label.setText("Excellent")

                self.sec_report3.ui.religion_c1_label.setText(str(row[38]))
                self.sec_report3.ui.religion_c2_label.setText(str(row[39]))
                self.sec_report3.ui.religion_ass_label.setText(str(row[40]))
                self.sec_report3.ui.religion_exam_label.setText(str(row[41]))
                self.sec_report3.ui.religion_total_label.setText(str(row[42]))

                if row[42] < 40:
                    self.sec_report3.ui.religion_grade_label.setText("F")
                    self.sec_report3.ui.religion_remark_label.setText("Fail")
                elif row[42] >= 40 and row[42] < 50:
                    self.sec_report3.ui.religion_grade_label.setText("D")
                    self.sec_report3.ui.religion_remark_label.setText("Pass")
                elif row[42] >= 50 and row[42] < 60:
                    self.sec_report3.ui.religion_grade_label.setText("C")
                    self.sec_report3.ui.religion_remark_label.setText("Good")
                elif row[42] >= 60 and row[42] < 70:
                    self.sec_report3.ui.religion_grade_label.setText("B")
                    self.sec_report3.ui.religion_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.religion_grade_label.setText("A")
                    self.sec_report3.ui.religion_remark_label.setText("Excellent")

                self.sec_report3.ui.civic_c1_label.setText(str(row[43]))
                self.sec_report3.ui.civic_c2_label.setText(str(row[44]))
                self.sec_report3.ui.civic_ass_label.setText(str(row[45]))
                self.sec_report3.ui.civic_exam_label.setText(str(row[46]))
                self.sec_report3.ui.civic_total_label.setText(str(row[47]))

                if row[47] < 40:
                    self.sec_report3.ui.civic_grade_label.setText("F")
                    self.sec_report3.ui.civic_remark_label.setText("Fail")
                elif row[47] >= 40 and row[47] < 50:
                    self.sec_report3.ui.civic_grade_label.setText("D")
                    self.sec_report3.ui.civic_remark_label.setText("Pass")
                elif row[47] >= 50 and row[47] < 60:
                    self.sec_report3.ui.civic_grade_label.setText("C")
                    self.sec_report3.ui.civic_remark_label.setText("Good")
                elif row[47] >= 60 and row[47] < 70:
                    self.sec_report3.ui.civic_grade_label.setText("B")
                    self.sec_report3.ui.civic_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.civic_grade_label.setText("A")
                    self.sec_report3.ui.civic_remark_label.setText("Excellent")

                self.sec_report3.ui.cca_c1_label.setText(str(row[48]))
                self.sec_report3.ui.cca_c2_label.setText(str(row[49]))
                self.sec_report3.ui.cca_ass_label.setText(str(row[50]))
                self.sec_report3.ui.cca_exam_label.setText(str(row[51]))
                self.sec_report3.ui.cca_total_label.setText(str(row[52]))

                if row[52] < 40:
                    self.sec_report3.ui.cca_grade_label.setText("F")
                    self.sec_report3.ui.cca_remark_label.setText("Fail")
                elif row[52] >= 40 and row[52] < 50:
                    self.sec_report3.ui.cca_grade_label.setText("D")
                    self.sec_report3.ui.cca_remark_label.setText("Pass")
                elif row[52] >= 50 and row[52] < 60:
                    self.sec_report3.ui.cca_grade_label.setText("C")
                    self.sec_report3.ui.cca_remark_label.setText("Good")
                elif row[52] >= 60 and row[52] < 70:
                    self.sec_report3.ui.cca_grade_label.setText("B")
                    self.sec_report3.ui.cca_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.cca_grade_label.setText("A")
                    self.sec_report3.ui.cca_remark_label.setText("Excellent")

                self.sec_report3.ui.prevoc_c1_label.setText(str(row[53]))
                self.sec_report3.ui.prevoc_c2_label.setText(str(row[54]))
                self.sec_report3.ui.prevoc_ass_label.setText(str(row[55]))
                self.sec_report3.ui.prevoc_exam_label.setText(str(row[56]))
                self.sec_report3.ui.prevoc_total_label.setText(str(row[57]))

                if row[57] < 40:
                    self.sec_report3.ui.prevoc_grade_label.setText("F")
                    self.sec_report3.ui.prevoc_remark_label.setText("Fail")
                elif row[57] >= 40 and row[57] < 50:
                    self.sec_report3.ui.prevoc_grade_label.setText("D")
                    self.sec_report3.ui.prevoc_remark_label.setText("Pass")
                elif row[57] >= 50 and row[57] < 60:
                    self.sec_report3.ui.prevoc_grade_label.setText("C")
                    self.sec_report3.ui.prevoc_remark_label.setText("Good")
                elif row[57] >= 60 and row[57] < 70:
                    self.sec_report3.ui.prevoc_grade_label.setText("B")
                    self.sec_report3.ui.prevoc_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.prevoc_grade_label.setText("A")
                    self.sec_report3.ui.prevoc_remark_label.setText("Excellent")

                self.sec_report3.ui.french_c1_label.setText(str(row[58]))
                self.sec_report3.ui.french_c2_label.setText(str(row[59]))
                self.sec_report3.ui.french_ass_label.setText(str(row[60]))
                self.sec_report3.ui.french_exam_label.setText(str(row[61]))
                self.sec_report3.ui.french_total_label.setText(str(row[62]))

                if row[62] < 40:
                    self.sec_report3.ui.french_grade_label.setText("F")
                    self.sec_report3.ui.french_remark_label.setText("Fail")
                elif row[62] >= 40 and row[62] < 50:
                    self.sec_report3.ui.french_grade_label.setText("D")
                    self.sec_report3.ui.french_remark_label.setText("Pass")
                elif row[62] >= 50 and row[62] < 60:
                    self.sec_report3.ui.french_grade_label.setText("C")
                    self.sec_report3.ui.french_remark_label.setText("Good")
                elif row[62] >= 60 and row[62] < 70:
                    self.sec_report3.ui.french_grade_label.setText("B")
                    self.sec_report3.ui.french_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.french_grade_label.setText("A")
                    self.sec_report3.ui.french_remark_label.setText("Excellent")

                self.sec_report3.ui.hausa_c1_label.setText(str(row[63]))
                self.sec_report3.ui.hausa_c2_label.setText(str(row[64]))
                self.sec_report3.ui.hausa_ass_label.setText(str(row[65]))
                self.sec_report3.ui.hausa_exam_label.setText(str(row[66]))
                self.sec_report3.ui.hausa_total_label.setText(str(row[67]))

                if row[67] < 40:
                    self.sec_report3.ui.hausa_grade_label.setText("F")
                    self.sec_report3.ui.hausa_remark_label.setText("Fail")
                elif row[67] >= 40 and row[67] < 50:
                    self.sec_report3.ui.hausa_grade_label.setText("D")
                    self.sec_report3.ui.hausa_remark_label.setText("Pass")
                elif row[67] >= 50 and row[67] < 60:
                    self.sec_report3.ui.hausa_grade_label.setText("C")
                    self.sec_report3.ui.hausa_remark_label.setText("Good")
                elif row[67] >= 60 and row[67] < 70:
                    self.sec_report3.ui.hausa_grade_label.setText("B")
                    self.sec_report3.ui.hausa_remark_label.setText("Very Good")
                else:
                    self.sec_report3.ui.hausa_grade_label.setText("A")
                    self.sec_report3.ui.hausa_remark_label.setText("Excellent")

                self.sec_report3.ui.total_scores3_label.setText(str(row[68]))
                self.sec_report3.ui.avg3_label.setText(str(row[69]))
                self.sec_report3.ui.total_cum_label.setText(str(row[70]))
                self.sec_report3.ui.avg_cum_label.setText(str(row[71]))

                if row[69] < 40:
                    self.sec_report3.ui.master_com_label.setText("Bad result. Be careful.")
                    self.sec_report3.ui.head_com_label.setText("Bad result.")
                elif row[69] >= 40 and row[69] < 50:
                    self.sec_report3.ui.master_com_label.setText("Weak result. Work hard.")
                    self.sec_report3.ui.head_com_label.setText("Weak result.")
                elif row[69] >= 50 and row[69] < 60:
                    self.sec_report3.ui.master_com_label.setText("Fair result. Work hard.")
                    self.sec_report3.ui.head_com_label.setText("Fair result.")
                elif row[69] >= 60 and row[69] < 70:
                    self.sec_report3.ui.master_com_label.setText("Good result. Put more effort.")
                    self.sec_report3.ui.head_com_label.setText("Good result.")
                else:
                    self.sec_report3.ui.master_com_label.setText("Excellent result. Keep on.")
                    self.sec_report3.ui.head_com_label.setText("Excellent result.")

                cmd9 = "SELECT * FROM t_sec_scores_first WHERE stud_no = ?"
                cur.execute(cmd9, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.sec_report3.ui.total_scores_label.setText("None")
                    self.sec_report3.ui.avg_label.setText("None")
                elif row[68] == None and row[69] == None:
                    self.sec_report3.ui.total_scores_label.setText("None")
                    self.sec_report3.ui.avg_label.setText("None")
                else:
                    self.sec_report3.ui.total_scores_label.setText(str(row[68]))
                    self.sec_report3.ui.avg_label.setText(str(row[69]))

                cmd10 = "SELECT * FROM t_sec_scores_second WHERE stud_no = ?"
                cur.execute(cmd10, (admission_no,))
                row = cur.fetchone()
                if row == None:
                    self.sec_report3.ui.total_scores2_label.setText("None")
                    self.sec_report3.ui.avg2_label.setText("None")
                elif row[68] == None and row[69] == None:
                    self.sec_report3.ui.total_scores2_label.setText("None")
                    self.sec_report3.ui.avg2_label.setText("None")
                else:
                    self.sec_report3.ui.total_scores2_label.setText(str(row[68]))
                    self.sec_report3.ui.avg2_label.setText(str(row[69]))

                positions = []
                cmd11 = "SELECT * FROM t_sec_scores_third WHERE score_class = ? ORDER BY avg DESC"
                cur.execute(cmd11, (classes_combo,))
                rows = cur.fetchall()
                for row in rows:
                    positions.append(row[1])
                self.sec_report3.ui.out_of_label.setText(str(len(positions)))
                for i in range(len(positions)):
                    if admission_no == positions[i]:
                        if i in range (10, len(positions), 100):
                            self.sec_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (11, len(positions), 100):
                            self.sec_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (12, len(positions), 100):
                            self.sec_report3.ui.position_label.setText(str(i+1)+"th")
                        elif i in range (0, len(positions), 10):
                            self.sec_report3.ui.position_label.setText(str(i+1)+"st")
                        elif i in range (1, len(positions), 10):
                            self.sec_report3.ui.position_label.setText(str(i+1)+"nd")
                        elif i in range (2, len(positions), 10):
                            self.sec_report3.ui.position_label.setText(str(i+1)+"rd")
                        else:
                            self.sec_report3.ui.position_label.setText(str(i+1)+"th")

                cmd4 = "SELECT * FROM t_classes WHERE class_name = ?"
                cur.execute(cmd4, (classes_combo,))
                row = cur.fetchone()
                self.sec_report3.ui.master_name_label.setText(str(row[1]))

                cmd5 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
                cur.execute(cmd5)
                row = cur.fetchone()
                self.sec_report3.ui.head_name_label.setText(row[1])

                cmd6 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd6)
                row = cur.fetchone()
                self.sec_report3.ui.next_term_label.setText(row[3])

                cmd7 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd7)
                row = cur.fetchone()
                self.sec_report3.ui.fees_label.setText(row[4])

                cmd8 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
                cur.execute(cmd8)
                row = cur.fetchone()
                self.sec_report3.ui.session_label.setText(row[2])

                if self.ui.att_a_radio.isChecked() == False and self.ui.att_b_radio.isChecked() == False and self.ui.att_c_radio.isChecked() == False and self.ui.att_d_radio.isChecked() == False and self.ui.att_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grade in attendance", QMessageBox.Ok)

                elif self.ui.con_a_radio.isChecked() == False and self.ui.con_b_radio.isChecked() == False and self.ui.con_c_radio.isChecked() == False and self.ui.con_d_radio.isChecked() == False and self.ui.con_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grades in conduct", QMessageBox.Ok)

                elif self.ui.neat_a_radio.isChecked() == False and self.ui.neat_b_radio.isChecked() == False and self.ui.neat_c_radio.isChecked() == False and self.ui.neat_d_radio.isChecked() == False and self.ui.neat_e_radio.isChecked() == False:
                    QMessageBox.critical(self, "Printing Report", "ERROR: Please select student's grades in neatness", QMessageBox.Ok)
                else:
                    self.printReport3()

            except Error:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all student's scores have been recorded in all subjects", QMessageBox.Ok)
            except TypeError:
                QMessageBox.critical(self, "Generating Report", "ERROR: Please ensure all student's scores have been recorded in all subjects", QMessageBox.Ok)





    def displayRadios(self):
        if self.ui.att_a_radio.isChecked():
            self.sec_report3.ui.att_a_label.setText("v")
            self.sec_report3.ui.att_b_label.setText("")
            self.sec_report3.ui.att_c_label.setText("")
            self.sec_report3.ui.att_d_label.setText("")
            self.sec_report3.ui.att_e_label.setText("")

        elif self.ui.att_b_radio.isChecked():
            self.sec_report3.ui.att_a_label.setText("")
            self.sec_report3.ui.att_b_label.setText("v")
            self.sec_report3.ui.att_c_label.setText("")
            self.sec_report3.ui.att_d_label.setText("")
            self.sec_report3.ui.att_e_label.setText("")

        elif self.ui.att_c_radio.isChecked():
            self.sec_report3.ui.att_a_label.setText("")
            self.sec_report3.ui.att_b_label.setText("")
            self.sec_report3.ui.att_c_label.setText("v")
            self.sec_report3.ui.att_d_label.setText("")
            self.sec_report3.ui.att_e_label.setText("")

        elif self.ui.att_d_radio.isChecked():
            self.sec_report3.ui.att_a_label.setText("")
            self.sec_report3.ui.att_b_label.setText("")
            self.sec_report3.ui.att_c_label.setText("")
            self.sec_report3.ui.att_d_label.setText("v")
            self.sec_report3.ui.att_e_label.setText("")

        elif self.ui.att_e_radio.isChecked():
            self.sec_report3.ui.att_a_label.setText("")
            self.sec_report3.ui.att_b_label.setText("")
            self.sec_report3.ui.att_c_label.setText("")
            self.sec_report3.ui.att_d_label.setText("")
            self.sec_report3.ui.att_e_label.setText("v")

        if self.ui.con_a_radio.isChecked():
            self.sec_report3.ui.con_a_label.setText("v")
            self.sec_report3.ui.con_b_label.setText("")
            self.sec_report3.ui.con_c_label.setText("")
            self.sec_report3.ui.con_d_label.setText("")
            self.sec_report3.ui.con_e_label.setText("")

        elif self.ui.con_b_radio.isChecked():
            self.sec_report3.ui.con_a_label.setText("")
            self.sec_report3.ui.con_b_label.setText("v")
            self.sec_report3.ui.con_c_label.setText("")
            self.sec_report3.ui.con_d_label.setText("")
            self.sec_report3.ui.con_e_label.setText("")

        elif self.ui.con_c_radio.isChecked():
            self.sec_report3.ui.con_a_label.setText("")
            self.sec_report3.ui.con_b_label.setText("")
            self.sec_report3.ui.con_c_label.setText("v")
            self.sec_report3.ui.con_d_label.setText("")
            self.sec_report3.ui.con_e_label.setText("")

        elif self.ui.con_d_radio.isChecked():
            self.sec_report3.ui.con_a_label.setText("")
            self.sec_report3.ui.con_b_label.setText("")
            self.sec_report3.ui.con_c_label.setText("")
            self.sec_report3.ui.con_d_label.setText("v")
            self.sec_report3.ui.con_e_label.setText("")

        elif self.ui.con_e_radio.isChecked():
            self.sec_report3.ui.con_a_label.setText("")
            self.sec_report3.ui.con_b_label.setText("")
            self.sec_report3.ui.con_c_label.setText("")
            self.sec_report3.ui.con_d_label.setText("")
            self.sec_report3.ui.con_e_label.setText("v")

        if self.ui.neat_a_radio.isChecked():
            self.sec_report3.ui.neat_a_label.setText("v")
            self.sec_report3.ui.neat_b_label.setText("")
            self.sec_report3.ui.neat_c_label.setText("")
            self.sec_report3.ui.neat_d_label.setText("")
            self.sec_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.sec_report3.ui.neat_a_label.setText("")
            self.sec_report3.ui.neat_b_label.setText("v")
            self.sec_report3.ui.neat_c_label.setText("")
            self.sec_report3.ui.neat_d_label.setText("")
            self.sec_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_b_radio.isChecked():
            self.sec_report3.ui.neat_a_label.setText("")
            self.sec_report3.ui.neat_b_label.setText("v")
            self.sec_report3.ui.neat_c_label.setText("")
            self.sec_report3.ui.neat_d_label.setText("")
            self.sec_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_c_radio.isChecked():
            self.sec_report3.ui.neat_a_label.setText("")
            self.sec_report3.ui.neat_b_label.setText("")
            self.sec_report3.ui.neat_c_label.setText("v")
            self.sec_report3.ui.neat_d_label.setText("")
            self.sec_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_d_radio.isChecked():
            self.sec_report3.ui.neat_a_label.setText("")
            self.sec_report3.ui.neat_b_label.setText("")
            self.sec_report3.ui.neat_c_label.setText("")
            self.sec_report3.ui.neat_d_label.setText("v")
            self.sec_report3.ui.neat_e_label.setText("")

        elif self.ui.neat_e_radio.isChecked():
            self.sec_report3.ui.neat_a_label.setText("")
            self.sec_report3.ui.neat_b_label.setText("")
            self.sec_report3.ui.neat_c_label.setText("")
            self.sec_report3.ui.neat_d_label.setText("")
            self.sec_report3.ui.neat_e_label.setText("v")


    def printReport3(self):
        # Create printer
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            # Start painter
            painter.begin(printer)
            # Grab a widget you want to print
            screen = self.sec_report3.grab()
            # Draw grabbed pixmap
            painter.drawPixmap(50, 50, screen)
            # End painting
            painter.end()

class SecReport3(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SecReport3rdForm()
        self.ui.setupUi(self)

        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit.hide()


        self.ui.print_date_label.setText(self.ui.dateTimeEdit.text())

        self.ui.dateTimeEdit.hide()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    sec_scores_record = SecScoresRecord()
    sec_scores_record.show()
    sys.exit(app.exec_())
