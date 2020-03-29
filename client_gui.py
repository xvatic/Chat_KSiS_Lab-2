# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiclient.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(582, 402)
        self.comboBox_chatParticipants = QtWidgets.QComboBox(Form)
        self.comboBox_chatParticipants.setGeometry(QtCore.QRect(380, 60, 191, 26))
        self.comboBox_chatParticipants.setObjectName("comboBox_chatParticipants")
        self.textEdit_chatView = QtWidgets.QTextEdit(Form)
        self.textEdit_chatView.setGeometry(QtCore.QRect(50, 40, 301, 251))
        self.textEdit_chatView.setReadOnly(True)
        self.textEdit_chatView.setObjectName("textEdit_chatView")
        self.textEdit_messageInput = QtWidgets.QTextEdit(Form)
        self.textEdit_messageInput.setGeometry(QtCore.QRect(90, 320, 211, 31))
        self.textEdit_messageInput.setObjectName("textEdit_messageInput")
        self.pushButton_sendMessage = QtWidgets.QPushButton(Form)
        self.pushButton_sendMessage.setGeometry(QtCore.QRect(110, 360, 113, 32))
        self.pushButton_sendMessage.setObjectName("pushButton_sendMessage")
        self.pushbutton_Connect = QtWidgets.QPushButton(Form)
        self.pushbutton_Connect.setGeometry(QtCore.QRect(420, 190, 113, 32))
        self.pushbutton_Connect.setObjectName("pushbutton_Connect")
        self.textEdit_setName = QtWidgets.QTextEdit(Form)
        self.textEdit_setName.setGeometry(QtCore.QRect(420, 160, 101, 21))
        self.textEdit_setName.setObjectName("textEdit_setName")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_sendMessage.setText(_translate("Form", "Send"))
        self.pushbutton_Connect.setText(_translate("Form", "Register"))
