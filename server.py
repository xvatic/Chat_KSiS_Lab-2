from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from server_gui import Ui_Form

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
