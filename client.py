from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from client_gui import Ui_Form


class Communicate(QObject):
    new_message = pyqtSignal()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.signal = Communicate()
        self.signal.new_message.connect(self.new_message)

    def search(self):
        ClIENT_HOST = socket.gethostbyname(socket.gethostname())
        ClIENT_PORT = 1234
        UDPSocket = UDPTools(ClIENT_HOST, ClIENT_PORT)
        UDPSocket.set_broadcast()
        UDPSocket.start_UDP_thread_recieve()
        UDPSocket.start_UDP_thread_send()
        time.sleep(0.05)
        host, port = UDPSocket.transfer_value()
        print(host, port)
        needed_host = str(host)
        needed_port = int(port)
        UDPSocket.stopped_connection()
        self.TCPSocket.set_host_and_port(needed_host, needed_port)
        self.TCPSocket.set_login(application.ui.textEdit_setName.toPlainText())
        self.TCPSocket.connect()

    def new_message(self):
        data = self.TCPSocket.get_message()

    def set_tcp_socket(self, socket):
        self.TCPSocket = socket


if __name__ == "__main__":
    import sys
    import socket
    import threading
    import time
    from UDPInteraction import UDPTools
    from TCPConnection import TCPTools

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()
    TCPSocket = TCPTools(application.signal.new_message)
    application.set_tcp_socket(TCPSocket)

    application.ui.pushbutton_Connect.clicked.connect(application.search)
    sys.exit(app.exec_())
