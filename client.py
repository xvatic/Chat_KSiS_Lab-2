from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from client_gui import Ui_Form


class Communicate(QObject):
    message_processing = pyqtSignal()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.signal = Communicate()
        self.signal.message_processing.connect(self.message_processing)
        self.MARKER_CLIENTS = 'active_clients'
        self.clients = []

    def search(self):
        ClIENT_HOST = socket.gethostbyname(socket.gethostname())
        ClIENT_PORT = 1234
        UDPSocket = UDPTools(ClIENT_HOST, ClIENT_PORT)
        UDPSocket.set_broadcast()
        UDPSocket.start_UDP_thread_recieve()
        UDPSocket.start_UDP_thread_send()
        time.sleep(0.05)
        host, port = UDPSocket.transfer_value()
        needed_host = str(host)
        needed_port = int(port)
        UDPSocket.stopped_connection()
        self.TCPSocket.set_host_and_port(needed_host, needed_port)
        self.TCPSocket.set_login(application.ui.textEdit_setName.toPlainText())
        self.TCPSocket.connect()

    def message_processing(self):
        data = self.TCPSocket.get_message()
        print(data)
        if data[0] == self.MARKER_CLIENTS:
            for i in range(1, len(data), 2):
                self.ui.comboBox_chatParticipants.addItem(data[i])
                self.clients.append(data[i+1])

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
    TCPSocket = TCPTools(application.signal.message_processing)
    application.set_tcp_socket(TCPSocket)

    application.ui.pushbutton_Connect.clicked.connect(application.search)

    sys.exit(app.exec_())
