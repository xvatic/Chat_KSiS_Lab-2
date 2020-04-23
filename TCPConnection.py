import socket
import threading
import time
from PyQt5 import QtCore, QtWidgets
from time import gmtime, strftime


class TCPTools(QtWidgets.QWidget):
    def __init__(self, signal):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.login = ''
        self.server_flag = False
        self.message_signal = signal

        self.MARKER_ALL = 'all'
        self.MARKER_CONNECT = 'connect'
        self.MARKER_DISCONNECT = 'disconnect'

    def sending(self, marker, reciever, message):
        time = strftime("%H:%M:%S %d-%m-%Y", gmtime())
        message = f' |{time}| {message}'
        try:
            self.socket.send(
                bytes(f'{marker}~{reciever}~[{self.login}]~{message}', encoding='UTF-8'))
        except OSError:
            pass

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.sending(self.MARKER_CONNECT, self.MARKER_ALL, 'connected')
        self.start_TCP_thread_recieve(None, None)

    def get_message(self):
        return self.message

    def set_login(self, value):
        self.login = value

    def set_host_and_port(self, host, port):
        self.host = host
        self.port = port

    def accept(self):
        connection, address = self.socket.accept()

        self.start_TCP_thread_recieve(connection, address)
        return connection, address

    def set_client_connection_info(self, connection, address):
        self.connection = connection
        self.address = address

    def get_client_connection_info(self):
        return self.connection, self.address

    def set_reusable(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def set_server_flag(self):
        self.server_flag = True

    def set_new_message(self, message):
        self.message = message

    def recieve(self, connection, address):
        while not self.stopped:
            try:
                while not self.stopped:
                    if self.server_flag:
                        data = connection.recv(1024).decode('utf-8').split('~')
                        self.set_client_connection_info(connection, address)
                    else:
                        data = self.socket.recv(1024).decode('utf-8').split('~')
                    self.set_new_message(data)
                    self.message_signal.emit()
                    time.sleep(2)
            except:
                self.stopped = True

    def start_TCP_thread_recieve(self, connection, address):
        self.stopped = False

        Thread_recieve = threading.Thread(
            target=self.recieve, args=(connection, address), daemon=True)
        Thread_recieve.start()

    def disconnect(self):
        self.sending(self.MARKER_DISCONNECT, self.MARKER_GLOBAL, "left")
        self.stopped = True
        self.socket.close()
