from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

from server_gui import Ui_Form


class Communicate(QObject):
    new_message_serv = pyqtSignal()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.clients = {}
        self.message_list = []
        self.client_info = {}
        self.MARKER_GLOBAL = 'global'
        self.MARKER_CONNECT = 'connect'
        self.MARKER_DISCONNECT = 'disconnect'
        self.MARKER_CLIENTS = 'clients'

        self.signal = Communicate()
        self.signal.new_message_serv.connect(self.new_message_serv)

    def request_processing(self, marker, login, client_id, connection):
        if marker == self.MARKER_CONNECT:
            active_clients = ''
            for id_value, login_value in self.client_info.items():
                active_clients += f'~{login_value}~{id_value}'

            connection.send(bytes(f'active_clients{active_clients}'.encode('utf-8')))

            self.client_info[client_id] = login

    def new_message_serv(self):
        data = self.TCPSocket_app.get_message()
        connection, address = self.TCPSocket_app.get_client_connection_info()
        marker, reciever, login, message_content = data[0], data[1], data[2], data[3:]

        client_id, client_ip = str(address[1]), address[0]
        self.request_processing(marker, login, client_id, connection)

#        if marker == self.MARKER_CONNECT:
    #        return f'{marker}~{client_id}~{reciever}~{login}~{message}'

    def set_tcp_socket(self, socket):
        self.TCPSocket_app = socket

    def thread_option(self):
        while True:
            connection, address = self.TCPSocket_app.accept()
            self.clients[connection] = str(address[1])

    def start(self):
        thread = threading.Thread(target=self.thread_option, daemon=True)
        thread.start()


if __name__ == "__main__":

    import sys
    import socket
    import threading
    import time

    from UDPInteraction import UDPTools
    from TCPConnection import TCPTools
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 1234
    GENERAl_GATE = '0.0.0.0'

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()

    UDPSocket = UDPTools(HOST, PORT)
    UDPSocket.set_reusable()
    UDPSocket.bind(GENERAl_GATE, PORT)
    UDPSocket.address_request_flag()
    UDPSocket.start_UDP_thread_recieve()

    TCPSocket = TCPTools(application.signal.new_message_serv)
    TCPSocket.set_reusable()
    TCPSocket.socket.bind((HOST, PORT))
    TCPSocket.socket.listen(10)
    TCPSocket.set_server_flag()
    application.set_tcp_socket(TCPSocket)
    application.start()

    sys.exit(app.exec_())
