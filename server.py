from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
import pickle

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
        self.MARKER_ALL = 'all'
        self.MARKER_CONNECT = 'connect'
        self.MARKER_DISCONNECT = 'disconnect'
        self.MARKER_COMMON = 'common'
        self.MARKER_CLIENTS = 'clients'
        self.MARKER_HISTORY = 'history'

        self.signal = Communicate()
        self.signal.new_message_serv.connect(self.new_message_serv)

    def request_processing(self, mode, login, client_id, connection):
        if mode == self.MARKER_CONNECT:
            clients = {1: 'active_clients', 2: self.client_info}
            connection.send(pickle.dumps(clients))

            self.client_info[client_id] = login

    def new_message_serv(self):
        data = self.TCPSocket_app.flush()
        processed_data = pickle.loads(data)
        connection, address = self.TCPSocket_app.get_client_connection_info()

        mode, reciever, login, message_content = processed_data[
            1], processed_data[2], processed_data[3], processed_data[4]
        print(processed_data)

        client_id, client_ip = str(address[1]), address[0]
        self.request_processing(mode, login, client_id, connection)
        '''
        message = '~'.join(message_content)
        message_converted = f'|{client_ip}:{PORT}|{message}'
        final_message = ''
        if reciever == self.MARKER_ALL:
            self.message_list.append(f'{mode}~{client_id}~{reciever}~{login}~{message_converted}')

        if marker == self.MARKER_COMMON:
            final_message = f'{mode}~{client_id}~{reciever}~{login}~::{message_converted}'

        if marker == self.MARKER_CONNECT or marker == self.MARKER_DISCONNECT:
            final_message = f'{mode}~{client_id}~{reciever}~{login}~::{message_converted}'

        self.ui.textEdit_server_log.append(f'{message} {address}')
        self.sending(final_message, reciever, connection)
        '''

    def sending(self, message, reciever, connection):
        for client_value, address_value in self.clients.items():
            if connection != client_value:
                if address_value == reciever:
                    client_value.send(bytes(message.encode('utf-8')))
                elif reciever == self.MARKER_ALL:
                    client_value.send(bytes(message.encode('utf-8')))


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
