# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serverxmlgui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(570, 321)
        self.textEdit_server_log = QtWidgets.QTextEdit(Form)
        self.textEdit_server_log.setGeometry(QtCore.QRect(-10, 0, 581, 321))
        self.textEdit_server_log.setObjectName("textEdit_server_log")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
