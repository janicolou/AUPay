# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Nico\AUPay\src\windows\ui\AddUserDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(464, 321)
        Dialog.setFocusPolicy(QtCore.Qt.NoFocus)
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Dialog.setAutoFillBackground(False)
        Dialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonSave_addUser = QtWidgets.QPushButton(Dialog)
        self.buttonSave_addUser.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.buttonSave_addUser.setFont(font)
        self.buttonSave_addUser.setObjectName("buttonSave_addUser")
        self.horizontalLayout.addWidget(self.buttonSave_addUser)
        self.buttonCancel_addUser = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.buttonCancel_addUser.setFont(font)
        self.buttonCancel_addUser.setObjectName("buttonCancel_addUser")
        self.horizontalLayout.addWidget(self.buttonCancel_addUser)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.cardID_addUser = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.cardID_addUser.setFont(font)
        self.cardID_addUser.setReadOnly(True)
        self.cardID_addUser.setObjectName("cardID_addUser")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cardID_addUser)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.schoolID_addUser = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.schoolID_addUser.setFont(font)
        self.schoolID_addUser.setObjectName("schoolID_addUser")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.schoolID_addUser)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.password_addUser = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.password_addUser.setFont(font)
        self.password_addUser.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.password_addUser.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.password_addUser.setFrame(True)
        self.password_addUser.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_addUser.setClearButtonEnabled(False)
        self.password_addUser.setObjectName("password_addUser")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.password_addUser)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.userType_addUser = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.userType_addUser.setFont(font)
        self.userType_addUser.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.userType_addUser.setEditable(False)
        self.userType_addUser.setFrame(True)
        self.userType_addUser.setObjectName("userType_addUser")
        self.userType_addUser.addItem("")
        self.userType_addUser.addItem("")
        self.userType_addUser.addItem("")
        self.userType_addUser.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.userType_addUser)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.secret_addUser = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.secret_addUser.setFont(font)
        self.secret_addUser.setReadOnly(True)
        self.secret_addUser.setObjectName("secret_addUser")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.secret_addUser)
        self.label_6 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.otpt_addUser = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.otpt_addUser.setFont(font)
        self.otpt_addUser.setObjectName("otpt_addUser")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.otpt_addUser)
        self.buttonScanId_addUser = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.buttonScanId_addUser.setFont(font)
        self.buttonScanId_addUser.setObjectName("buttonScanId_addUser")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.buttonScanId_addUser)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add User"))
        self.buttonSave_addUser.setText(_translate("Dialog", "Save"))
        self.buttonCancel_addUser.setText(_translate("Dialog", "Cancel"))
        self.label_5.setText(_translate("Dialog", "Card ID:"))
        self.label.setText(_translate("Dialog", "School ID:"))
        self.label_2.setText(_translate("Dialog", "Password:"))
        self.label_3.setText(_translate("Dialog", "User Type:"))
        self.userType_addUser.setItemText(0, _translate("Dialog", "User"))
        self.userType_addUser.setItemText(1, _translate("Dialog", "Business"))
        self.userType_addUser.setItemText(2, _translate("Dialog", "Teller"))
        self.userType_addUser.setItemText(3, _translate("Dialog", "Admin"))
        self.label_4.setText(_translate("Dialog", "Secret:"))
        self.label_6.setText(_translate("Dialog", "OTP:"))
        self.buttonScanId_addUser.setText(_translate("Dialog", "Scan ID"))
