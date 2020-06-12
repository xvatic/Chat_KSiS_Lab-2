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
        Form.resize(872, 500)
        self.comboBox_chatParticipants = QtWidgets.QComboBox(Form)
        self.comboBox_chatParticipants.setGeometry(QtCore.QRect(680, 60, 191, 26))
        self.comboBox_chatParticipants.setObjectName("comboBox_chatParticipants")

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 190, 291))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget(Form)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 190, 291))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 131, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.pushButton_switch = QtWidgets.QPushButton(Form)
        self.pushButton_switch.setGeometry(QtCore.QRect(680, 30, 191, 26))
        self.pushButton_switch.setObjectName("pushButton_switch")
        self.pushButton_switch.setText('Switch')
        self.pushButton_toall = QtWidgets.QPushButton(Form)
        self.pushButton_toall.setGeometry(QtCore.QRect(680, 90, 191, 26))
        self.pushButton_toall.setObjectName("pushButton_toall")
        self.pushButton_toall.setText('To All')
        self.notification_label = QtWidgets.QLabel(Form)
        self.notification_label.setGeometry(QtCore.QRect(10, 0, 200, 10))
        self.notification_label.setObjectName('notification_label')
        self.notification_label.setText('notifications')
        self.textEdit_chatView = QtWidgets.QTextEdit(Form)
        self.textEdit_chatView.setGeometry(QtCore.QRect(200, 10, 351, 291))
        self.textEdit_chatView.setReadOnly(True)
        self.textEdit_chatView.setObjectName("textEdit_chatView")
        self.textEdit_chatView.setFont(QtGui.QFont("Arial", 12))
        self.textEdit_messageInput = QtWidgets.QTextEdit(Form)
        self.textEdit_messageInput.setGeometry(QtCore.QRect(200, 320, 211, 31))
        self.textEdit_messageInput.setObjectName("textEdit_messageInput")
        self.pushButton_sendMessage = QtWidgets.QPushButton(Form)
        self.pushButton_sendMessage.setGeometry(QtCore.QRect(230, 360, 113, 32))
        self.pushButton_sendMessage.setObjectName("pushButton_sendMessage")
        self.pushButton_uploadFile = QtWidgets.QPushButton(Form)
        self.pushButton_uploadFile.setGeometry(QtCore.QRect(230, 400, 113, 32))
        self.pushButton_uploadFile.setObjectName("pushButton_uploadFile")
        self.pushbutton_Connect = QtWidgets.QPushButton(Form)
        self.pushbutton_Connect.setGeometry(QtCore.QRect(720, 190, 113, 32))
        self.pushbutton_Connect.setObjectName("pushbutton_Disconnect")
        self.pushbutton_Disconnect = QtWidgets.QPushButton(Form)
        self.pushbutton_Disconnect.setGeometry(QtCore.QRect(720, 290, 113, 32))
        self.pushbutton_Disconnect.setObjectName("pushbutton_Disconnect")
        self.lineEdit_setName = QtWidgets.QLineEdit(Form)
        self.lineEdit_setName.setGeometry(QtCore.QRect(720, 160, 101, 21))
        self.lineEdit_setName.setObjectName("textEdit_setName")

        self.scrollArea_2 = QtWidgets.QScrollArea(Form)
        self.scrollArea_2.setGeometry(QtCore.QRect(200, 440, 521, 31))
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget(Form)
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 519, 29))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 521, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.scrollArea_3 = QtWidgets.QScrollArea(Form)
        self.scrollArea_3.setGeometry(QtCore.QRect(551, 10, 151, 351))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget(Form)
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 169, 291))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 169, 291))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_uploadFile.setText(_translate("Form", "Attachment"))
        self.pushButton_sendMessage.setText(_translate("Form", "Send"))
        self.pushbutton_Connect.setText(_translate("Form", "Register"))
        self.pushbutton_Disconnect.setText(_translate("Form", "Disconnect"))
