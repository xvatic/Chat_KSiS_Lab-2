from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from client_gui import Ui_Form
from time import gmtime, strftime


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
        self.MARKER_CONNECT = 'connect'
        self.MARKER_DISCONNECT = 'disconnect'
        self.MARKER_ALL = 'all'
        self.MARKER_COMMON = 'common'
        self.message_list = []
        self.clients = []
        self.reciever_address = self.MARKER_ALL

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

    def renew_clients(self, marker, sender_id, login):
        if marker == self.MARKER_CONNECT:
            self.clients.append(sender_id)
            self.ui.comboBox_chatParticipants.addItem(login)
        elif marker == self.MARKER_DISCONNECT:
            self.clients.pop(sender_id)
            self.ui.comboBox_chatParticipants.remove(login)

    def show_message(self, sender_id, reciever, message):
        if reciever == self.MARKER_ALL:
            self.ui.textEdit_chatView.append(message)

    def message_processing(self):
        data = self.TCPSocket.get_message()
        if data[0] == self.MARKER_CLIENTS:
            for i in range(1, len(data), 2):
                self.ui.comboBox_chatParticipants.addItem(data[i])
                self.clients.append(data[i+1])
            return

        marker = data[0]
        sender_id = data[1]
        reciever = data[2]
        login = data[3]
        message = data[3] + '~'.join(data[4:])

        print(data)
        if data[0] == self.MARKER_CLIENTS:
            for i in range(1, len(data), 2):
                self.ui.comboBox_chatParticipants.addItem(data[i])
                self.clients.append(data[i+1])

        self.renew_clients(marker, sender_id, login)
        self.show_message(sender_id, reciever, message)

    def set_tcp_socket(self, socket):
        self.TCPSocket = socket

    def convert(self):
        message = self.ui.textEdit_messageInput.toPlainText()
        if message:
            self.sending(self.MARKER_COMMON, self.reciever_address, message, True)

    def sending(self, marker, reciever, message, append):
        time = strftime("%H:%M:%S %d-%m-%Y", gmtime())
        final_message = f'{time}{message}'

        self.message_list.append([reciever, final_message])
        self.TCPSocket.sending(marker, reciever, message)

        if append:
            self.ui.textEdit_chatView.append(f'{final_message}')


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
    application.ui.pushButton_sendMessage.clicked.connect(application.convert)

    sys.exit(app.exec_())
