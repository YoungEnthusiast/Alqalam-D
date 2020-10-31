import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import QByteArray, QDateTime, QBuffer, QIODevice

from adminform import Ui_Form
from inherstudedit import StudEdit
import sqlite3
from sqlite3 import Error

class InherAdmin(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.stud_edit = StudEdit()

        self.displayUsers()
        self.displayClasses()

        self.ui.class_edit_lineEdit.hide()
        self.ui.form_master_edit_lineEdit.hide()
        self.ui.class_update_btn.hide()
        self.ui.class_add_lineEdit.hide()
        self.ui.class_save_btn.hide()
        self.ui.form_master_lineEdit.hide()

        self.ui.user_save_btn.hide()
        self.ui.username_label.hide()
        self.ui.password_label.hide()
        self.ui.class_edit_label.hide()
        self.ui.form_master_edit_label.hide()
        self.ui.class_add_label.hide()
        self.ui.form_master_add_label.hide()
        self.ui.username_lineEdit.hide()
        self.ui.password_lineEdit.hide()
        self.ui.principal_edit_lineEdit.hide()
        self.ui.headmaster_edit_lineEdit.hide()
        self.ui.principal_update_btn.hide()
        self.ui.headmaster_update_btn.hide()
        self.ui.session_lineEdit.hide()
        self.ui.session_label.hide()
        self.ui.next_term_lineEdit.hide()
        self.ui.next_term_label.hide()
        self.ui.mgmt_update_btn.hide()
        self.ui.fees_label.hide()
        self.ui.fees_lineEdit.hide()

        self.ui.class_edit_btn.clicked.connect(self.showEditClass)
        self.ui.class_update_btn.clicked.connect(self.editClass)
        self.ui.class_delete_btn.clicked.connect(self.deleteClass)
        self.ui.add_new_btn.clicked.connect(self.showAddClass)
        self.ui.class_save_btn.clicked.connect(self.saveClass)
        self.ui.stud_edit_btn.clicked.connect(self.showEditStud)
        self.stud_edit.ui.update_btn.clicked.connect(self.editStud)
        self.stud_edit.ui.browse_btn.clicked.connect(self.browseImage)
        self.ui.stud_del_btn.clicked.connect(self.deleteStud)
        self.ui.user_add_btn.clicked.connect(self.showAddUser)
        self.ui.user_save_btn.clicked.connect(self.saveUser)
        self.ui.user_delete_btn.clicked.connect(self.deleteUser)
        self.ui.class_comboBox2.currentTextChanged.connect(self.displayStuds)
        #Generates Current Date
        self.stud_edit.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.principal_edit_btn.clicked.connect(self.showEditPrin)
        self.ui.headmaster_edit_btn.clicked.connect(self.showEditHead)
        self.ui.mgmt_edit_btn.clicked.connect(self.showEditMgmt)

        self.ui.principal_update_btn.clicked.connect(self.editPrin)
        self.ui.headmaster_update_btn.clicked.connect(self.editHead)
        self.ui.mgmt_update_btn.clicked.connect(self.editMgmt)


    def displayUsers(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute("SELECT * FROM t_users ORDER BY username")
        rows = cur.fetchall()
        users = ["Select a user"]
        self.ui.user_comboBox.clear()
        for row in rows:
            users.append(row[0])
        self.ui.user_comboBox.addItems(users)
        con.close()

    def showAddUser(self):
        self.ui.user_save_btn.show()
        self.ui.username_label.show()
        self.ui.password_label.show()
        self.ui.username_lineEdit.show()
        self.ui.password_lineEdit.show()

    def saveUser(self):
        username = self.ui.username_lineEdit.text()
        password = self.ui.password_lineEdit.text()
        cmd = "INSERT INTO t_users(username, password) VALUES(?, ?)"
        try:
            con = sqlite3.connect("alqalamdb.db")
            con.execute("PRAGMA foreign_keys = 1")
            cur = con.cursor()
            cur.execute(cmd, (username, password, ))
            con.commit()
            QMessageBox.information(self, 'Adding User', username + " added successfully", QMessageBox.Ok)
            self.displayUsers()
        except Error:
            QMessageBox.critical(self, 'Adding User',"ERROR: "+ username + " already exists", QMessageBox.Ok)
        finally:
            con.close()
            self.ui.class_add_lineEdit.clear()

    def deleteUser(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        username = self.ui.user_comboBox.currentText()
        cmd = "DELETE FROM t_users WHERE username = ?"
        if username == "Select a user":
            QMessageBox.critical(self, 'Deleting User', "ERROR: Please select a user to delete", QMessageBox.Ok)
        else:
            buttonReply = QMessageBox.warning(self, 'Deleting User', "WARNING: Deleting this user means the user will not be able to use the system again. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (username,))
                con.commit()
                self.displayUsers()
                con.close()

    def showAddClass(self):
        self.ui.class_add_lineEdit.show()
        self.ui.class_save_btn.show()
        self.ui.class_add_label.show()
        self.ui.form_master_add_label.show()
        self.ui.form_master_lineEdit.show()

    def showEditClass(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        class_name = self.ui.class_comboBox.currentText()
        cmd1 = "SELECT * FROM t_classes WHERE class_name = ?"
        cur.execute(cmd1, (class_name,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Editing Class", "ERROR: Please select a class to edit", QMessageBox.Ok)
        else:
            self.ui.class_edit_lineEdit.show()
            self.ui.class_edit_lineEdit.setText(row[0])
            self.ui.class_update_btn.show()
            self.ui.class_edit_label.show()
            self.ui.form_master_edit_label.show()
            self.ui.form_master_edit_lineEdit.show()
            self.ui.form_master_edit_lineEdit.setText(row[1])

    def editClass(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        old_class = self.ui.class_comboBox.currentText()
        new_class = self.ui.class_edit_lineEdit.text()
        new_master = self.ui.form_master_edit_lineEdit.text()

        cmd1 = "SELECT class_name FROM t_classes WHERE class_name = ?"
        try:
            cur.execute(cmd1, (old_class,))
            row = cur.fetchone()
            if old_class == "Select a class":
                QMessageBox.critical(self, 'Editing Class', "ERROR: Please select a class to edit", QMessageBox.Ok)
            else:
                cmd2 = "UPDATE t_classes SET class_name = ?, form_master = ? WHERE class_name = ?"
                cur.execute(cmd2, (new_class, new_master, old_class,))
                con.commit()
                QMessageBox.information(self, "Class Modification", "Class modified successfully", QMessageBox.Ok)
                self.ui.class_edit_lineEdit.hide()
                self.ui.class_update_btn.hide()
                self.ui.class_edit_label.hide()
                self.ui.form_master_edit_label.hide()
                self.ui.form_master_edit_lineEdit.hide()
                self.displayClasses()
        except Error:
            QMessageBox.critical(self, "Editing Class","ERROR: "+ new_class + " already exists", QMessageBox.Ok)
        finally:
            con.close()


    def deleteClass(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        class_name = self.ui.class_comboBox.currentText()
        cmd = "DELETE FROM t_classes WHERE class_name = ?"
        if class_name == "Select a class":
            QMessageBox.critical(self, 'Deleting Class', "ERROR: Please select a class to delete", QMessageBox.Ok)
        else:
            buttonReply = QMessageBox.warning(self, 'Deleting Class', "WARNING: Deleting this class will delete all students in it. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (class_name,))
                con.commit()
                self.displayClasses()
                con.close()

    def saveClass(self):
        new_save_class = self.ui.class_add_lineEdit.text()
        new_form_master = self.ui.form_master_lineEdit.text()
        cmd = "INSERT INTO t_classes(class_name, form_master) VALUES(?, ?)"
        try:
            con = sqlite3.connect("alqalamdb.db")
            con.execute("PRAGMA foreign_keys = 1")
            cur = con.cursor()
            cur.execute(cmd, (new_save_class, new_form_master,))
            con.commit()
            QMessageBox.information(self, 'Adding Class', new_save_class + " added successfully", QMessageBox.Ok)
            self.displayClasses()
        except Error:
            QMessageBox.critical(self, 'Adding Class',"ERROR: "+ new_save_class + " already exists", QMessageBox.Ok)
        finally:
            con.close()

    def displayClasses(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        query = cur.execute('SELECT * FROM t_classes ORDER BY class_name')
        rows = cur.fetchall()
        classes = ["Select a class"]
        self.ui.class_comboBox.clear()
        self.ui.class_comboBox2.clear()
        for row in rows:
            classes.append(row[0])
        self.ui.class_comboBox.addItems(classes)
        self.ui.class_comboBox2.addItems(classes)
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

    def showEditStud(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        admission_no = self.ui.stud_name_comboBox.currentText()
        cmd1 = "SELECT * FROM t_studs WHERE admission_no = ?"
        cur.execute(cmd1, (admission_no,))
        row = cur.fetchone()
        if row == None:
            QMessageBox.critical(self, "Editing Student", "ERROR: Please select a student to edit", QMessageBox.Ok)
        else:
            self.stud_edit.showMaximized()
            self.stud_edit.ui.admission_edit.setText(row[0])
            self.stud_edit.ui.name_edit.setText(row[1])
            self.stud_edit.ui.date_edit.setText(row[2])
            self.stud_edit.ui.class_comboBox.setCurrentText(row[3])
            self.stud_edit.ui.sex_edit.setText(row[4])
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(row[5]))
            self.stud_edit.ui.image_label.setPixmap(QPixmap(pixmap))
            self.stud_edit.ui.address_lineEdit.setText(row[6])
            self.stud_edit.ui.parent_no_lineEdit.setText(row[7])

    def browseImage(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Image Files (*.png *.jpg *gif)')
        image_path = file_name[0]
        pixmap = QPixmap(image_path)
        self.stud_edit.ui.image_label.setPixmap(QPixmap(pixmap))

    def editStud(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        var_admission_no = self.ui.stud_name_comboBox.currentText()
        new_admission_no = self.stud_edit.ui.admission_edit.text()
        new_stud_name = self.stud_edit.ui.name_edit.text()
        new_dob = self.stud_edit.ui.date_edit.text()
        new_class = self.stud_edit.ui.class_comboBox.currentText()
        new_sex = self.stud_edit.ui.sex_edit.text()
        buff = QBuffer()
        buff.open(QIODevice.WriteOnly)
        pixmap = QPixmap(self.stud_edit.ui.image_label.pixmap())
        pixmap.save(buff, "PNG")
        binary_img = buff.data().toBase64().data()
        new_address = self.stud_edit.ui.address_lineEdit.text()
        new_parent_no = self.stud_edit.ui.parent_no_lineEdit.text()
        modified_date = self.stud_edit.ui.dateTimeEdit.text()
        cmd2 = "SELECT * FROM t_studs WHERE admission_no = ?"
        try:
            cur.execute(cmd2, (var_admission_no,))
            row = cur.fetchone()
            cmd3 = "UPDATE t_studs SET admission_no = ?, stud_name = ?, date_of_birth = ?, stud_class = ?, sex = ?, photo = ?, address = ?, parent_no =?, modified_date = ? WHERE admission_no = ?"
            cur.execute(cmd3, (new_admission_no, new_stud_name, new_dob, new_class, new_sex, binary_img, new_address, new_parent_no, modified_date, var_admission_no,))
            con.commit()
            QMessageBox.information(self, "Class Modification", "Student details modified successfully", QMessageBox.Ok)
            self.displayClasses()
        except Error:
            QMessageBox.critical(self, "Editing Student","ERROR: "+ new_admission_no + " already exists", QMessageBox.Ok)
        finally:
            con.close()
            self.stud_edit.close()

    def deleteStud(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        stud_no = self.ui.stud_name_comboBox.currentText()
        cmd = "DELETE FROM t_studs WHERE admission_no = ?"
        if stud_no == "Select an admission number":
            QMessageBox.critical(self, 'Deleting Class', "ERROR: Please select a student to delete", QMessageBox.Ok)
        else:
            buttonReply = QMessageBox.warning(self, "Deleting Student", "WARNING: Deleting this student will delete all the student's record in the system. Do you still wish to continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                cur.execute(cmd, (stud_no,))
                con.commit()
                self.displayClasses()
                con.close()

    def showEditPrin(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        cmd1 = "SELECT * FROM t_senior_users WHERE role = 'principal'"
        cur.execute(cmd1)
        row = cur.fetchone()
        if row == None:
            self.ui.principal_edit_lineEdit.show()
            self.ui.principal_update_btn.show()
        else:
            self.ui.principal_edit_lineEdit.show()
            self.ui.principal_edit_lineEdit.setText(row[1])
            self.ui.principal_update_btn.show()

    def editPrin(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        new_principal = self.ui.principal_edit_lineEdit.text()

        cmd1 = "SELECT * FROM t_senior_users WHERE role = 'principal'"
        try:
            row = cur.fetchone()
            cmd2 = "UPDATE t_senior_users SET role = 'principal', name = ? WHERE role = 'principal'"
            cur.execute(cmd2, (new_principal,))
            con.commit()
            QMessageBox.information(self, "Principal Modification", "Principal's name modified successfully", QMessageBox.Ok)
        except Error as e:
            QMessageBox.critical(self, "Editing Principal", str(e), QMessageBox.Ok)
        finally:
            con.close()

    def showEditHead(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        cmd1 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
        cur.execute(cmd1)
        row = cur.fetchone()
        if row == None:
            self.ui.headmaster_edit_lineEdit.show()
            self.ui.headmaster_update_btn.show()
        else:
            self.ui.headmaster_edit_lineEdit.show()
            self.ui.headmaster_edit_lineEdit.setText(row[1])
            self.ui.headmaster_update_btn.show()

    def editHead(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        new_headmaster = self.ui.headmaster_edit_lineEdit.text()

        cmd1 = "SELECT * FROM t_senior_users WHERE role = 'headmaster'"
        try:
            row = cur.fetchone()
            cmd2 = "UPDATE t_senior_users SET role = 'headmaster', name = ? WHERE role = 'headmaster'"
            cur.execute(cmd2, (new_headmaster,))
            con.commit()
            QMessageBox.information(self, "Headmaster Modification", "Headmaster's name modified successfully", QMessageBox.Ok)
        except Error as e:
            QMessageBox.critical(self, "Editing Headmaster", str(e), QMessageBox.Ok)
        finally:
            con.close()

    def showEditMgmt(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        cmd1 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
        cur.execute(cmd1)
        row = cur.fetchone()
        if row == None:
            self.ui.session_lineEdit.show()
            self.ui.session_label.show()
            self.ui.next_term_label.show()
            self.ui.next_term_lineEdit.show()
            self.ui.mgmt_update_btn.show()
        else:
            self.ui.session_lineEdit.show()
            self.ui.session_lineEdit.setText(row[2])
            self.ui.session_label.show()
            self.ui.next_term_label.show()
            self.ui.fees_label.show()
            self.ui.next_term_lineEdit.show()
            self.ui.next_term_lineEdit.setText(row[3])
            self.ui.fees_lineEdit.show()
            self.ui.fees_lineEdit.setText(row[4])
            self.ui.mgmt_update_btn.show()

    def editMgmt(self):
        con = sqlite3.connect("alqalamdb.db")
        con.execute("PRAGMA foreign_keys = 1")
        cur = con.cursor()
        new_session = self.ui.session_lineEdit.text()
        new_term = self.ui.next_term_lineEdit.text()
        new_fees = self.ui.fees_lineEdit.text()

        cmd1 = "SELECT * FROM t_senior_users WHERE role = 'mgmt'"
        try:
            row = cur.fetchone()
            cmd2 = "UPDATE t_senior_users SET role = 'mgmt', session = ?, term_begins = ?, fees = ? WHERE role = 'mgmt'"
            cur.execute(cmd2, (new_session, new_term, new_fees,))
            con.commit()
            QMessageBox.information(self, "Session and Term Modification", "Modified successfully", QMessageBox.Ok)
        except Error as e:
            QMessageBox.critical(self, "Session and Term Modification", str(e), QMessageBox.Ok)
        finally:
            con.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InherAdmin()
    widget.show()

    sys.exit(app.exec_())
