from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dbHelper import add_user, find_user_by_id, update_user, delete_user, add_transaction, find_all_admins
from dbHelper.find_user import find_all_tellers
from fnHelper import get_random_secret, get_totp, verify_otp
from fnHelper.load_tables import *
from windows.ui.ui_AddUserDialog import Ui_Dialog as AddUserUi_Dialog
from windows.ui.ui_EditUserDialog import Ui_Dialog as EditUserUi_Dialog
from windows.ui.ui_DeleteUserDialog import Ui_Dialog as DeleteUserUi_Dialog
from windows.ui.ui_AddTransactionDialog import Ui_Dialog as AddTransaction_Dialog
from windows.ui.ui_AddSupplyDialog import Ui_Dialog as AddSupply_Dialog
from windows.ui.ui_EditMaxCreditDialog import Ui_Dialog as EditMaxCredit_Dialog
from windows.ui.ui_AddUserShortDialog import Ui_Dialog as AddUserShortUi_Dialog
from bson import ObjectId, Timestamp
from fnHelper.aupCard import AUPCard
from fnHelper.cryptography import hash
from datetime import *
from fnHelper.textSearch import *
from fnHelper.export_to_csv import *
from dbHelper.calculate_total_circulating_supply import calculate_total_circulating_supply
from fnHelper.refresh_clear import *
from fnHelper.refreshUserBalance import *
from windows.ProjectMainWindow import ProjectMainWindow

def editUser(self):
    selected_row = self.adminWindow_users_table.currentRow()
    item = self.adminWindow_users_table.item(selected_row, 0)
    if item is None:
        return print("select row to edit")
    id = ObjectId(self.adminWindow_users_table.item(selected_row, 0).text())
    current_user_data = find_user_by_id(id)
    edit_dialog = EditUserDialog(id)
    edit_dialog.table_updated.connect(lambda: load_users_to_table(self, self.adminWindow_users_table))
    edit_dialog.ui.cardID_editUser.setText(current_user_data['card_id'])
    edit_dialog.ui.schoolID_editUser.setText(current_user_data['school_id'])
    edit_dialog.ui.otpSecret_editUser.setText(current_user_data['secret_key'])
    def current_user_type(user_type):
        if user_type == 'user':
            return "User"
        elif user_type == 'admin':
            return "Admin"
        elif user_type == 'business':
            return "Business"
        elif user_type == 'teller':
            return "Teller"
    edit_dialog.ui.userType_editUser.setCurrentText(current_user_type(current_user_data['user_type']))
    edit_dialog.exec()

def deleteUser(self):
    selected_row = self.adminWindow_users_table.currentRow()
    item = self.adminWindow_users_table.item(selected_row, 0)
    if item is None:
        return print("select row to delete")
    id = self.adminWindow_users_table.item(selected_row, 0).text()
    delete_dialog = DeleteUserDialog(id)
    delete_dialog.table_updated.connect(lambda: load_users_to_table(self, self.adminWindow_users_table))
    delete_dialog.exec()
    
class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super(AddUserDialog, self).__init__(parent)
        self.addUserDialog()

    def addUserDialog(self):
        self.ui = AddUserUi_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonSave_addUser.clicked.connect(lambda: self.saveButton())
        self.ui.buttonCancel_addUser.clicked.connect(lambda: self.close())
        self.ui.buttonScanId_addUser.clicked.connect(lambda: self.scanID())
        self.ui.secret_addUser.setText(get_random_secret())
        self.totp = get_totp(self.ui.secret_addUser.text())
        self.ui.otpt_addUser.textChanged.connect(lambda: self.verifyOTP(self.ui.secret_addUser.text()))

    def scanID(self):
        self.ui.cardID_addUser.setText(AUPCard().get_uid())

    def checkFields(self):
        # paki check lahat ng fields if may laman 
        if not verify_otp(self.totp, self.ui.otpt_addUser.text()):
            print("Invalid OTP")
            return False
        return True

    def saveButton(self):
        newUser = {
            'card_id': hash(self.ui.cardID_addUser.text()),
            'school_id': self.ui.schoolID_addUser.text(),
            'password': hash(self.ui.password_addUser.text()),
            'secret_key': self.ui.secret_addUser.text(),
            'user_type': self.ui.userType_addUser.currentText().lower(),
            'max_credit': 0.00,
            'balance': 0.00,
        }
        if self.checkFields():
            add_user(newUser)
            self.close()

    def verifyOTP(self, otpSecret):
        totp = get_totp(otpSecret)
        if(verify_otp(totp, self.ui.otpt_addUser.text())):
            self.ui.buttonSave_addUser.setEnabled(True)
        else:
            self.ui.buttonSave_addUser.setEnabled(False)

def open_add_user_dialog(self):
    # Check if there is a selected row
    selected_items = self.adminWindow_users_table.selectedItems()
    if selected_items:
        # Clear the selection
        self.adminWindow_users_table.clearSelection()
    self.add_user_dialog = AddUserDialog()
    self.add_user_dialog.ui.buttonSave_addUser.clicked.connect(lambda: reload_users_table(self))
    self.add_user_dialog.exec_()
    
def reload_users_table(self):
    load_users_to_table(self, self.adminWindow_users_table)
    self.adminWindow_users_table.setCurrentItem(None)
    self.adminWindow_user_search.setText("")
    
def addTransaction(self):
    AddTransactionDialog().exec()

class EditUserDialog(QDialog):
    table_updated = pyqtSignal()
    def __init__(self, id, parent=None):
        super(EditUserDialog, self).__init__(parent)
        self.ui = EditUserUi_Dialog()
        self.ui.setupUi(self)
        idValidator = QIntValidator()
        idValidator.setRange(0, 100000)
        # self.ui.buttonSave_editUser.setEnabled(False)
        self.ui.buttonSave_editUser.clicked.connect(lambda: self.updateUser(id))
        self.ui.buttonCancel_editUser.clicked.connect(lambda: self.close())
        self.ui.buttonGenerate_editUser.clicked.connect(lambda: self.ui.otpSecret_editUser.setText(self.generateOTPSecret()))
        self.ui.otp_editUser.textChanged.connect(lambda: self.verifyOTP(self.ui.otpSecret_editUser.text()))
        self.ui.buttonScanID_editUser.clicked.connect(lambda: self.scanId())
        self.oldCardId = self.ui
        

    def scanId(self):
        self.ui.cardID_editUser.setEnabled(True)
        self.ui.cardID_editUser.setText(AUPCard().get_uid())
        
    def updateUser(self, id):
            userData = {
                '_id': ObjectId(id),
                'card_id': (lambda: self.ui.cardID_editUser.text(), lambda: hash(self.ui.cardID_editUser.text()))[self.ui.cardID_editUser.isEnabled()](),
                'school_id': self.ui.schoolID_editUser.text(),
                'password': hash(self.ui.password_editUser.text()),
                'secret_key': self.ui.otpSecret_editUser.text(),
                'user_type': self.ui.userType_editUser.currentText().lower(),
            }
            update_user(userData)
            self.table_updated.emit()
            self.close()
            
    def verifyOTP(self, otpSecret):
        totp = get_totp(otpSecret)
        if(verify_otp(totp, self.ui.otp_editUser.text())):
            self.ui.buttonSave_editUser.setEnabled(True)
        else:
            self.ui.buttonSave_editUser.setEnabled(False)

    def generateOTPSecret(self):
        newSecret = get_random_secret()
        self.totp = get_totp(self.ui.otpSecret_editUser.text())
        self.ui.otpSecret_editUser.setEnabled(True)
        self.ui.buttonSave_editUser.setEnabled(False)
        self.ui.otp_editUser.setEnabled(True)
        return newSecret

class DeleteUserDialog(QDialog):
    table_updated = pyqtSignal()
    def __init__(self, id, parent=None):
        super(DeleteUserDialog, self).__init__(parent)
        self.ui = DeleteUserUi_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonDelete_deleteUser.clicked.connect(lambda: self.deleteUser(id))
        self.ui.buttonCancel_deleteUser.clicked.connect(lambda: self.close())
    def deleteUser(self, id):
        delete_user(ObjectId(id))
        self.table_updated.emit()
        self.close()

class AddUserShortDialog(QDialog):
    def __init__(self, user, parent=None):
        super(AddUserShortDialog, self).__init__(parent)
        self.ui = AddUserShortUi_Dialog()
        self.ui.setupUi(self)
        self.ui.button_add_user.clicked.connect(lambda: self.add_user())

    def add_user(self):
        if self.ui.line_school_id.text() != "":
            new_user = {
                'card_id': hash(AUPCard().get_uid()),
                'school_id': self.ui.line_school_id.text(),
                'password': hash('Shine On, Dear AUP!'),
                'secret_key': "",
                'user_type': self.ui.combo_user_type.currentText().lower(),
                'max_credit': 0.00,
                'balance': 0.00,
            }
            if new_user['card_id']:
                add_user(new_user)
                QMessageBox.information(self, "Success", f"User {new_user['school_id']} added") 
                self.close()
            else:
               QMessageBox.critical(self, "Error", "No RFID Detected") 
        else:
            QMessageBox.critical(self, "Error", "School ID Required")

class AddTransactionDialog(QDialog):
    table_updated = pyqtSignal()
    def __init__(self, user, parent=None):
        super(AddTransactionDialog, self).__init__(parent)
        self.ui = AddTransaction_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonSave_addTransaction.clicked.connect(lambda: self.addTransaction(user))
        self.ui.buttonCancel_addTransaction.clicked.connect(lambda: self.close())
        self.ui.adminWindow_addTransactionSourceId.setText('ffffffffffffffffffffffff') # coinbase id
        self.ui.buttonEditSourceID.clicked.connect(lambda: self.ui.adminWindow_addTransactionSourceId.setReadOnly(False))

    def addTransaction(self, user):
        newTransaction =  {
            "timestamp": Timestamp(int(datetime.today().timestamp()), 1),
            "source_id": ObjectId(self.ui.adminWindow_addTransactionSourceId.text()),
            "destination_id": ObjectId(self.ui.adminWindow_addDestinationId.text()),
            "amount": float(self.ui.adminWindow_addTransactionAmount.text()),
            "description": self.ui.adminWindow_addTransactionDescription.text()
        }
        add_transaction(newTransaction)
        self.table_updated.emit()
        self.close()

class AddSupplyDialog(QDialog):
    table_updated = pyqtSignal()
    def __init__(self, parent=None):
        super(AddSupplyDialog, self).__init__(parent)
        self.ui = AddSupply_Dialog()
        self.ui.setupUi(self)
        self.verified_admins = []
        for teller in find_all_tellers():
            self.ui.comboBox.addItem(teller['school_id'], teller['_id'])
        self.ui.button_admin1.clicked.connect(lambda: self.verify_admin("admin1"))
        self.ui.button_admin2.clicked.connect(lambda: self.verify_admin("admin2"))
        self.ui.pushButton.clicked.connect(lambda: self.addTransaction())

    def verify_admin(self, admin_number):
        current_admin = hash(AUPCard().get_uid())
        admins = find_all_admins()
        for admin in admins:
            if not self.verified_admins.__contains__(current_admin) and admin['card_id'] == current_admin:
                self.verified_admins.append(admin['card_id'])
                print(self.verified_admins)
                match admin_number:
                    case "admin1": self.ui.button_admin1.setEnabled(False)
                    case "admin2": self.ui.button_admin2.setEnabled(False)
                break
        current_admin = ""
        self.check_verification()

    def check_verification(self):
        if not self.ui.button_admin1.isEnabled() and not self.ui.button_admin2.isEnabled():
            self.ui.pushButton.setEnabled(True)

    def addTransaction(self):
        newTransaction =  {
            "timestamp": Timestamp(int(datetime.today().timestamp()), 1),
            "source_id": ObjectId('ffffffffffffffffffffffff'),
            "destination_id": ObjectId(self.ui.comboBox.currentData()),
            "amount": float(self.ui.doubleSpinBox.value()),
            "description": 'coinbase transaction'
        }
        print(newTransaction)
        add_transaction(newTransaction)
        self.close()

class EditMaxCreditDialog(QDialog):
    table_updated = pyqtSignal()
    def __init__(self, main_widget, user, parent=None):
        super(EditMaxCreditDialog, self).__init__(parent)
        self.ui = EditMaxCredit_Dialog()
        self.ui.setupUi(self)

        for teller in find_all_users():
            self.ui.comboBox.addItem(teller['school_id'], teller['_id'])
        self.ui.pushButton.clicked.connect(lambda: self.edit_max_credit(main_widget))

    def edit_max_credit(self, main_widget):
        userData = {
            '_id': self.ui.comboBox.currentData(),
            'max_credit': self.ui.doubleSpinBox.value(),
        }
        if update_user(userData):
            QMessageBox.information(self, "Success", "User updated.")
            self.close()
        else:
            QMessageBox.warning(self, "Failed", "Update user failed.")



def open_add_transaction_dialog(self, user):
    # Check if there is a selected row
    selected_items = self.adminWindow_transactions_table.selectedItems()
    if selected_items:
        # Clear the selection
        self.adminWindow_transactions_table.clearSelection()
    self.   _transaction_dialog = AddTransactionDialog(user)
    self.add_transaction_dialog.ui.buttonSave_addTransaction.clicked.connect(lambda: reload_transactions_table(self, user))
    self.add_transaction_dialog.exec_()
    
def reload_transactions_table(self, user):
    load_transactions_to_table(self, self.adminWindow_transactions_table, user)
    # refresh_bar_chart(self.adminWindow_transactions_table, self.graphicsView_3)
    self.adminWindow_transactions_table.setCurrentItem(None)
    self.adminWindow_transaction_search.setText("")

def refresh_analytics(self: ProjectMainWindow, user):
    pass

def refresh_transactions(self: ProjectMainWindow, user):
    pass

def refresh_dashboard(self: ProjectMainWindow, user):
    self.lineTotalCirculating_administrator.setText(str(calculate_total_circulating_supply()))
    self.refresh_administrator.clicked.connect(lambda: refreshUserBalance())
    self.buttonAddUser_short_administrator.clicked.connect(lambda: AddUserShortDialog(user).exec())
    self.buttonAddSupply_administrator.clicked.connect(lambda: AddSupplyDialog().exec_())
    self.buttonEditMaxCredit_administrator.clicked.connect(lambda: EditMaxCreditDialog(self, user).exec_())

def dateChanged(self: ProjectMainWindow, user):
    pass

def searchChanged(self: ProjectMainWindow, user, text):
    pass

def refresh_all(self: ProjectMainWindow, user):
    refresh_dashboard(self, user)
    refresh_transactions(self, user)
    refresh_analytics(self, user)

def AdminWindow(self: ProjectMainWindow, user):
    print(__name__)
    refresh_all(self, user)
    self.dateTo_administrator.setDate(QDate.currentDate())
    self.buttonAddUser_administrator.clicked.connect(lambda: open_add_user_dialog(self))
    self.buttonEditUser_administrator.clicked.connect(lambda: editUser(self))
    self.buttonDeleteUser_administrator.clicked.connect(lambda: deleteUser(self))
    self.buttonAddTransaction_administrator.clicked.connect(lambda: open_add_transaction_dialog(self, user))
    load_users_to_table(self, self.adminWindow_users_table)
    load_transactions_to_table(self, self.adminWindow_transactions_table, user)
    self.adminWindow_user_search.textChanged.connect(lambda text: search_users(text, self.adminWindow_users_table))
    self.adminWindow_transaction_search.textChanged.connect(lambda text: search_transactions(text, self.adminWindow_transactions_table))
    load_bar_chart(self.adminWindow_transactions_table, self.graphicsView_3)
    self.dateFrom_administrator.dateChanged.connect(lambda: search_transactions_by_date(self.adminWindow_transactions_table, self.dateFrom_administrator, self.dateTo_administrator))
    self.dateTo_administrator.dateChanged.connect(lambda: search_transactions_by_date(self.adminWindow_transactions_table, self.dateFrom_administrator, self.dateTo_administrator))
    self.export_administrator.clicked.connect(lambda: export_to_csv(self.adminWindow_transactions_table, f"{user['school_id']}_{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.csv"))
    self.buttonClearTransactions_administrator.clicked.connect(lambda: clear_date(self.dateFrom_administrator, self.dateTo_administrator, self.adminWindow_transactions_table))
    # self.refresh_administrator.clicked.connect(lambda: resfresh_table(self, self.adminWindow_users_table))
    
 
    





