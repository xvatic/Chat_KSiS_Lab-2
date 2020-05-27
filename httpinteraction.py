import socket
import threading
import time
from PyQt5 import QtCore, QtWidgets
from time import localtime, strftime
import pickle
from http import server, client


class HTTPTools(QtWidgets.QWidget):
    def __init__(self, signal):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.login = ''
        self.password = ''
        self.server_flag = False
        self.message_signal = signal
        self.MODE_KEY = 'mode'
        self.RECIEVER_KEY = 'reciever'
        self.PASSWORD_KEY = 'password'
        self.LOGIN_KEY = 'login'
        self.MESSAGE_KEY = 'message'
        self.ROOMS_KEY = 'rooms'

        self.MODE_CLIENTS = '03'
        self.MODE_CONNECT = '01'
        self.MODE_DISCONNECT = '02'
        self.MODE_COMMON = '00'
        self.MODE_HISTORY = '04'
        self.MODE_REGISTER = '05'
        self.MARKER_ROOM = '11'

    def serialize(self, message_dictionary):
        message_byte_form = pickle.dumps(message_dictionary)
        return message_byte_form

    def deserialize(self, message_byte_form):
        message_dictionary = pickle.loads(message_byte_form)
        return message_dictionary

    def fill(self, message):
        self.message = message

    def flush(self):
        return self.message

    def send_to_server(self, final_message):
        try:
            self.socket.send(final_message)
        except OSError:
            pass

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        final_message = {self.MODE_KEY: self.MODE_CONNECT,
                         self.PASSWORD_KEY: self.password, self.LOGIN_KEY: self.login}
        self.send_to_server(self.serialize(final_message))
        self.start_TCP_thread_recieve(None, None)

    def register(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        final_message = {self.MODE_KEY: self.MODE_REGISTER,
                         self.PASSWORD_KEY: self.password, self.LOGIN_KEY: self.login}
        self.send_to_server(self.serialize(final_message))
        self.start_TCP_thread_recieve(None, None)

    def set_login_and_password(self, login, password):
        self.login = login
        self.password = password

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

    def set_server_flag(self):
        self.server_flag = True

    def recieve(self, connection, address):
        while not self.stopped:
            try:
                while not self.stopped:
                    if self.server_flag:
                        data = connection.recv(1024)
                        self.set_client_connection_info(connection, address)
                    else:
                        data = self.socket.recv(1024)
                    self.fill(data)
                    self.message_signal.emit()
            except:
                self.stopped = True

    def start_TCP_thread_recieve(self, connection, address):
        self.stopped = False

        Thread_recieve = threading.Thread(
            target=self.recieve, args=(connection, address), daemon=True)
        Thread_recieve.start()

    def disconnect(self):
        self.sending(self.MODE_DISCONNECT, self.MARKER_ALL, "left")
        self.stopped = True
        self.socket.close()
