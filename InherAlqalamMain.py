import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QAction, QFileDialog, QTableWidgetItem
from PyQt5.QtCore import QDateTime, QBuffer, QIODevice, QByteArray
from PyQt5.QtGui import QPixmap, QIcon

from AlqalamMainWindow import Ui_MainWindow
from StudRegForm import Ui_StudRegForm
from adminauthentication import Ui_AdminAuthForm
from ChangePwdForm import Ui_ChangePwdForm
from studentslist import Ui_Form
from inherstuddisplay import StudDisplay
from inheradmin import InherAdmin
from inhernurscoresrecord import NurScoresRecord, NurScoresRecord2nd, NurScoresRecord3rd, NurScoresView, NurScoresView2, NurScoresView3
from inherpriscoresrecord import PriScoresRecord, PriScoresRecord2, PriScoresRecord3, PriScoresView, PriScoresView2, PriScoresView3
from inhersecscoresrecord import SecScoresRecord,  SecScoresView, SecScoresRecord2, SecScoresView2, SecScoresRecord3, SecScoresView3
import sqlite3
from sqlite3 import Error


class InherAlqalam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.studRegForm = InherStudReg()
        self.inher_list = StudList()
        self.inher_nur_score = NurScoresRecord()
        self.inher_nur_score_2nd = NurScoresRecord2nd()
        self.inher_nur_score_3rd = NurScoresRecord3rd()

        self.nur_score = NurScoresView()
        self.nur_score2 = NurScoresView2()
        self.nur_score3 = NurScoresView3()

        self.inher_pri_score = PriScoresRecord()
        self.inher_pri_score2 = PriScoresRecord2()
        self.inher_pri_score3 = PriScoresRecord3()

        self.pri_score = PriScoresView()
        self.pri_score2 = PriScoresView2()
        self.pri_score3 = PriScoresView3()

        self.inher_sec_score = SecScoresRecord()
        self.inher_sec_score2 = SecScoresRecord2()
        self.inher_sec_score3 = SecScoresRecord3()

        self.sec_score = SecScoresView()
        self.sec_score2 = SecScoresView2()
        self.sec_score3 = SecScoresView3()

        self.ui.actionNew.triggered.connect(self.showStudReg)
        self.ui.actionLogin.triggered.connect(self.showAdminAuth)
        self.ui.actionView_Students.triggered.connect(self.showInherList)
        self.ui.menuRecord.triggered.connect(self.displayNurRecordScore)
        self.ui.actionRecord_New_2.triggered.connect(self.displayNurRecordScore2nd)
        self.ui.menuRecord3.triggered.connect(self.displayNurRecordScore3rd)
        self.ui.actionView_Scores.triggered.connect(self.displayNurRecordView)
        self.ui.actionView_Scores_3.triggered.connect(self.displayNurRecordView2)
        self.ui.actionView_Scores_4.triggered.connect(self.displayNurRecordView3)

        self.ui.actionRecord_New.triggered.connect(self.displayPriRecordScore)
        self.ui.actionRecord_New_4.triggered.connect(self.displayPriRecordScore2)
        self.ui.actionRecord_New_5.triggered.connect(self.displayPriRecordScore3)

        self.ui.actionView_Scores_5.triggered.connect(self.displayPriRecordView)
        self.ui.actionView_Scores_6.triggered.connect(self.displayPriRecordView2)
        self.ui.actionView_Scores_7.triggered.connect(self.displayPriRecordView3)

        self.ui.actionRecord_New_6.triggered.connect(self.displaySecRecordScore)
        self.ui.actionRecord_New_7.triggered.connect(self.displaySecRecordScore2)
        self.ui.actionRecord_New_8.triggered.connect(self.displaySecRecordScore3)

        self.ui.actionView_Scores_8.triggered.connect(self.displaySecRecordView)
        self.ui.actionView_Scores_9.triggered.connect(self.displaySecRecordView2)
        self.ui.actionView_Scores_10.triggered.connect(self.displaySecRecordView3)

        self.ui.actionExit.triggered.connect(self.close)

        #self.inher_list.ui.class_sort_comboBox.currentTextChanged.connect(self.listClass)
    def showStudReg(self):
        self.studRegForm.showMaximized()

    def showAdminAuth(self):
        self.inher_admin = InherAdminAuthentication()
        self.inher_admin.showMaximized()

    def closeEvent(self, event):
        buttonReply = QMessageBox.question(self, 'Exit Application', "Are you sure you want to completely close the application?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            event.accept()
            self.studRegForm.close()
        else:
            event.ignore()

    def showInherList(self):
        self.inher_list.showMaximized()

    def displayNurRecordScore(self):
        self.inher_nur_score.showMaximized()

    def displayNurRecordScore2nd(self):
        self.inher_nur_score_2nd.showMaximized()

    def displayNurRecordScore3rd(self):
        self.inher_nur_score_3rd.showMaximized()

    def displayNurRecordView(self):
        self.nur_score.showMaximized()

    def displayPriRecordView(self):
        self.pri_score.showMaximized()

    def displayPriRecordView2(self):
        self.pri_score2.showMaximized()

    def displayPriRecordView3(self):
        self.pri_score3.showMaximized()

    def displayNurRecordView2(self):
        self.nur_score2.showMaximized()

    def displayNurRecordView3(self):
        self.inher_nur_score_3rd.hide()
        self.nur_score3.showMaximized()

    def displayPriRecordScore(self):
        self.inher_pri_score.showMaximized()

    def displayPriRecordScore2(self):
        self.inher_pri_score2.showMaximized()

    def displayPriRecordScore3(self):
        self.inher_pri_score3.showMaximized()

    def displaySecRecordScore(self):
        self.inher_sec_score.showMaximized()

    def displaySecRecordScore2(self):
        self.inher_sec_score2.showMaximized()

    def displaySecRecordScore3(self):
        self.inher_sec_score3.showMaximized()

    def displaySecRecordView(self):
        self.sec_score.showMaximized()

    def displaySecRecordView2(self):
        self.sec_score2.showMaximized()

    def displaySecRecordView3(self):
        self.sec_score3.showMaximized()




class InherStudReg(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StudRegForm()
        self.ui.setupUi(self)

        self.list_studs = StudList()

        self.displayClasses()
        #Calling displayDate
        self.ui.calendarWidget.selectionChanged.connect(self.displayDate)
        #Calling Current Date
        self.ui.save_btn.clicked.connect(self.displayCurrentDate)
        #Calling openFileDialog
        self.ui.browse_btn.clicked.connect(self.browseImage)
        #Generates Current Date
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.clear_btn.clicked.connect(self.clearAll)

        self.ui.save_btn.clicked.connect(self.insertStud)

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_classes ORDER BY class_name')
        classes = ["Select a class"]
        rows = cur.fetchall()
        for row in rows:
            classes.append(row[0])
        self.ui.class_comboBox.addItems(classes)
        con.commit()
        cur.close()
        con.close()

    def browseImage(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Image Files (*.png *.jpg *gif)')
        image_path = file_name[0]

        pixmap = QPixmap(image_path)
        self.ui.image_label.setPixmap(QPixmap(pixmap))

    def insertStud(self):
        if self.ui.admission_edit.text() == "":
            QMessageBox.critical(self, "Registration", "ERROR: Please supply an admission number", QMessageBox.Ok)
        elif self.ui.name_edit.text() == "":
            QMessageBox.critical(self, "Registration", "ERROR: Please supply a name.", QMessageBox.Ok)
        elif self.ui.class_comboBox.currentText() == "Select a class":
            QMessageBox.critical(self, "Registration", "ERROR: Please select a class.", QMessageBox.Ok)
        else:
            try:
                con = sqlite3.connect("alqalamdb.db")
                con.execute("PRAGMA foreign_keys = 1")
                cur = con.cursor()
                admission_no = self.ui.admission_edit.text()
                stud_name = self.ui.name_edit.text()
                date_of_birth = self.ui.dateEdit.text()
                stud_class = self.ui.class_comboBox.currentText()
                sex = self.ui.sex_comboBox.currentText()
                buff = QBuffer()
                buff.open(QIODevice.WriteOnly)
                pixmap = QPixmap(self.ui.image_label.pixmap())
                pixmap.save(buff, "PNG")
                binary_img = buff.data().toBase64().data()
                address = self.ui.address_lineEdit.text()
                parent_no = self.ui.parent_no_lineEdit.text()
                reg_date = self.ui.dateTimeEdit.text()
                cur.execute("INSERT INTO t_studs(admission_no, stud_name, date_of_birth, stud_class, sex, photo, address, parent_no, reg_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (admission_no, stud_name, date_of_birth, stud_class, sex, binary_img, address, parent_no, reg_date))
                con.commit()
                QMessageBox.information(self, "Registration", "Student has been added successfully", QMessageBox.Ok)
                self.list_studs.listStuds()
            except Error:
                #QMessageBox.critical(self, "Registration", str(e), QMessageBox.Ok)
                QMessageBox.critical(self, "Registration", "ERROR: The admission number should not be a duplicate of an existing student.", QMessageBox.Ok)
            except TypeError as e:
                QMessageBox.critical(self, "Registration", str(e), QMessageBox.Ok)
            finally:
                con.close()

    def clearAll(self):
        self.ui.admission_edit.clear()
        self.ui.name_edit.clear()
        self.ui.address_lineEdit.clear()
        self.ui.parent_no_lineEdit.clear()
    #Display Date
    def displayDate(self):
        self.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())
    #Display Current Date
    def displayCurrentDate(self):
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

class InherAdminAuthentication(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminAuthForm()
        self.ui.setupUi(self)
        self.inher_admin = InherAdmin()

        self.inher_alqalam = InherAlqalam()
        self.inher_change = InherChangePwd()
        self.ui.signin_btn.clicked.connect(self.loginAdmin)
        self.ui.change_btn.clicked.connect(self.showChange)
        self.ui.change_btn.clicked.connect(self.close)

    def loginAdmin(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        username = self.ui.user_lineEdit.text()
        password = self.ui.pwdlineEdit.text()
        cmd = "SELECT username, password FROM t_admins WHERE username = ? AND password = ?"
        cur.execute(cmd, (username, password))
        row = cur.fetchone()
        if row == None:
            self.ui.response_label.setText("Incorrect username or password")
        else:
            self.ui.response_label.setText("")
            QMessageBox.information(self, "Authentication", "You are successfully logged in", QMessageBox.Ok)
            self.inher_admin.showMaximized()
            self.hide()
        con.close()

    def showChange(self):
        self.inher_change.showMaximized()


class InherChangePwd(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ChangePwdForm()
        self.ui.setupUi(self)

        self.ui.update_btn.clicked.connect(self.updatePwd)

    def updatePwd(self):
        con = sqlite3.connect("alqalamdb.db")
        cur = con.cursor()
        username = self.ui.userlineEdit.text()
        old_password = self.ui.oldpwdlineEdit.text()
        new_password = self.ui.newpwdlineEdit.text()
        new_password2 = self.ui.new2pwdlineEdit.text()
        cmd1 = "SELECT username, password FROM t_admins WHERE username = ? AND password = ?"
        cur.execute(cmd1, (username, old_password,))
        row = cur.fetchone()
        if row == None:
            self.ui.response_label.setText("Incorrect username or password")
        else:
            if new_password == new_password2:
                cmd2 = "UPDATE t_admins SET password = ? WHERE username = ?"
                cur.execute(cmd2, (new_password, username,))
                con.commit()
                QMessageBox.information(self, "Authentication", "Password changed successfully", QMessageBox.Ok)
            else:
                self.ui.response_label.setText("The two new passwords do not match")
        con.close()



class StudList(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.stud_display = StudDisplay()


        #self.ui.class_sort_btn.clicked.connect(self.displaySortedNo)
        self.ui.class_comboBox.currentTextChanged.connect(self.displaySortedNo)

        self.ui.stud_search_btn.clicked.connect(self.searchStud)
        #self.ui.class_sort_btn.clicked.connect(self.listClass)
        self.ui.switch_btn.clicked.connect(self.listStuds)
        self.ui.class_comboBox.currentTextChanged.connect(self.listClass)

        self.displayClasses()
        self.listStuds()

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_classes ORDER BY class_name')
        classes = ["Select a class"]
        rows = cur.fetchall()
        for row in rows:
            classes.append(row[0])
        self.ui.class_comboBox.addItems(classes)
        con.commit()
        con.close()

    def listStuds(self):
        self.ui.tableWidget_2.hide()
        self.ui.total_label_2.setText("")
        self.ui.tableWidget.setRowCount(0)

        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        cmd = "SELECT * FROM t_studs ORDER BY admission_no"
        cur.execute(cmd)
        rows = cur.fetchall()
        total_rows = len(rows)
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                if column_number == 5:
                    pixmap = QPixmap()
                    pixmap.loadFromData(QByteArray.fromBase64(column_data))
                    icon = QIcon(pixmap)
                    it.setIcon(icon)
                else:
                    it.setText(str(column_data))
                self.ui.tableWidget.setItem(row_number, column_number, it)
        #self.ui.tableWidget.verticalHeader().setDefaultSectionSize(100)
        #self.inher_list.ui.total_label.setText("")
        self.ui.total_label.setText("Students Total: " + str(total_rows))
        self.ui.tableWidget.show()
        self.ui.tableWidget.setColumnWidth(0,125)
        self.ui.tableWidget.setColumnWidth(1,260)
        self.ui.tableWidget.setColumnWidth(2,185)
        self.ui.tableWidget.setColumnWidth(3,130)
        self.ui.tableWidget.setColumnWidth(4,90)
        self.ui.tableWidget.setColumnWidth(5,120)
        self.ui.tableWidget.setColumnWidth(6,345)
        self.ui.tableWidget.setColumnWidth(7,130)
        self.ui.tableWidget.setColumnWidth(8,340)
        self.ui.tableWidget.setColumnWidth(9,340)
        #self.inher_list.ui.tableWidget.horizontalHeader().setDefaultSectionSize(170)

        con.close()

    def listClass(self):
        self.ui.tableWidget.hide()
        self.ui.total_label.setText("")
        self.ui.tableWidget_2.setRowCount(0)
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ?"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget_2.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                it = QTableWidgetItem()
                if column_number == 5:
                    pixmap = QPixmap()
                    pixmap.loadFromData(QByteArray.fromBase64(column_data))
                    icon = QIcon(pixmap)
                    it.setIcon(icon)
                else:
                    it.setText(str(column_data))
                self.ui.tableWidget_2.setItem(row_number, column_number, it)

        self.ui.tableWidget_2.show()
        self.ui.tableWidget_2.setColumnWidth(0,125)
        self.ui.tableWidget_2.setColumnWidth(1,260)
        self.ui.tableWidget_2.setColumnWidth(2,185)
        self.ui.tableWidget_2.setColumnWidth(3,130)
        self.ui.tableWidget_2.setColumnWidth(4,90)
        self.ui.tableWidget_2.setColumnWidth(5,120)
        self.ui.tableWidget_2.setColumnWidth(6,345)
        self.ui.tableWidget_2.setColumnWidth(7,130)
        self.ui.tableWidget_2.setColumnWidth(8,340)
        self.ui.tableWidget_2.setColumnWidth(9,340)
        self.ui.class_comboBox.show()
        con.close()

    def displaySortedNo(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        classes_combo = self.ui.class_comboBox.currentText()
        cmd = "SELECT * FROM t_studs WHERE stud_class = ?"
        cur.execute(cmd, (classes_combo,))
        rows = cur.fetchall()
        total_classes_rows = len(rows)
        self.ui.total_label_2.setText(self.ui.class_comboBox.currentText() + " Total:" + str(total_classes_rows))
        con.close()

    def searchStud(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        admission_no = self.ui.stud_search_lineEdit.text()
        cmd = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd, (admission_no,))
        row = cur.fetchone()
        if admission_no == "":
            QMessageBox.critical(self, "Searching Student", "ERROR: Please fill in an admission number to search", QMessageBox.Ok)

        elif row == None:
            self.ui.response_label.setText("No student found for adimission number: " + self.ui.stud_search_lineEdit.text())
        else:
            self.ui.response_label.setText("")
            self.stud_display.showMaximized()
            self.stud_display.ui.admission_label.setText(row[0])
            self.stud_display.ui.name_label.setText(row[1])
            self.stud_display.ui.dob_label.setText(row[2])
            self.stud_display.ui.class_label.setText(row[3])
            self.stud_display.ui.gender_label.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.stud_display.ui.photo_label.setPixmap(QPixmap(pixmap))
            self.stud_display.ui.address_label.setText(row[6])
            self.stud_display.ui.parent_no_label.setText(row[7])
            self.stud_display.ui.reg_date_label.setText(row[8])
        con.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = InherAlqalam()
    mainWindow.showMaximized()
    sys.exit(app.exec_())
