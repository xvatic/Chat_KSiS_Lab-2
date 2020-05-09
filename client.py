from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
import pickle
import pyglet
from client_gui import Ui_Form
from time import localtime, strftime


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.signal = New_message_event_handle()
        self.signal.message_processing.connect(self.message_processing)
        self.MODE_CLIENTS = '03'
        self.MODE_CONNECT = '01'
        self.MODE_DISCONNECT = '02'
        self.MODE_COMMON = '00'
        self.MODE_HISTORY = '04'

        self.MARKER_ALL = '10'
        self.message_list = []
        self.clients = {}
        self.reciever_address = self.MARKER_ALL
        self.sound = pyglet.media.load('files/sms_uvedomlenie_na_iphone.wav', streaming=False)

    def search(self):
        ClIENT_HOST = socket.gethostbyname(socket.gethostname())
        ClIENT_PORT = 12345
        UDPSocket = UDPTools(ClIENT_HOST, ClIENT_PORT)
        UDPSocket.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        UDPSocket.start_UDP_thread_recieve()
        UDPSocket.start_UDP_thread_send()
        time.sleep(0.5)
        host, port = UDPSocket.flush()
        needed_host = str(host)
        needed_port = int(port)
        UDPSocket.stopped_connection()
        self.TCPSocket.set_host_and_port(needed_host, needed_port)
        self.TCPSocket.set_login(application.ui.textEdit_setName.toPlainText())
        self.TCPSocket.connect()
        self.history()

    def notify(self, sender_id, reciever):
        self.sound.play()
        if reciever == self.MARKER_ALL:
            self.ui.notification_label.setText('ALL')
        else:
            self.ui.notification_label.setText(self.clients[sender_id])

    def leave(self):
        self.TCPSocket.disconnect()
        self.message_list.clear()
        self.ui.comboBox_chatParticipants.clear()
        self.ui.textEdit_chatView.clear()

    def switch_to_private(self):

        for address in self.clients:
            if self.clients[address] == str(self.ui.comboBox_chatParticipants.currentText()):
                self.reciever_address = address
        self.ui.textEdit_chatView.clear()
        for message in self.message_list:
            data = message.split('~')
            if (data[1] == self.reciever_address and data[2] != self.MARKER_ALL) or (data[1] == 'me' and data[2] == self.reciever_address):
                self.show_message(data[1], data[2], data[4])

    def return_to_all(self):
        self.ui.textEdit_chatView.clear()
        self.reciever_address = self.MARKER_ALL
        for message in self.message_list:
            data = message.split('~')
            if data[2] == self.MARKER_ALL:
                self.show_message(data[1], data[2], data[4])

    def history(self):
        self.sending(self.MODE_HISTORY, self.MARKER_ALL, '04', False)

    def renew_clients(self, mode, sender_id, login):
        if mode == self.MODE_CONNECT:
            self.clients[sender_id] = login
            self.ui.comboBox_chatParticipants.addItem(login)
        elif mode == self.MODE_DISCONNECT:
            index = 0
            for address in self.clients:
                if address == sender_id:
                    break
                else:
                    index += 1
            del self.clients[sender_id]
            self.ui.comboBox_chatParticipants.removeItem(index)

    def store(self, history):
        for i in history:
            if history[i] != self.MODE_HISTORY:
                mode = history[i][1]
                sender_id = history[i][2]
                reciever = history[i][3]
                login = history[i][4]
                message = history[i][5]
                self.message_list.append(f'{mode}~{sender_id}~{reciever}~{login}~{message}')

    def serialize(self, message_dictionary):
        message_byte_form = pickle.dumps(message_dictionary)
        return message_byte_form

    def deserialize(self, message_byte_form):
        message_dictionary = pickle.loads(message_byte_form)
        return message_dictionary

    def show_message(self, sender_id, reciever, message):
        if sender_id == self.reciever_address or (reciever == self.MARKER_ALL and self.reciever_address == self.MARKER_ALL) or (sender_id == 'me' and reciever == self.reciever_address):
            self.ui.textEdit_chatView.append(message)

    def message_processing(self):
        processed_data = {}
        data = self.TCPSocket.flush()
        try:
            processed_data = self.deserialize(data)
        except EOFError:
            pass

        if processed_data:
            if processed_data == {}:
                return
            if processed_data[1] == self.MODE_CLIENTS:
                for id in processed_data[2]:
                    self.ui.comboBox_chatParticipants.addItem(processed_data[2][id])
                    self.clients[id] = processed_data[2][id]

                return

            if processed_data[1] == self.MODE_HISTORY:
                self.store(processed_data)

                for message in self.message_list:
                    data = message.split('~')

                    self.show_message(data[1], data[2], data[4])

                return
            mode = processed_data[1]
            sender_id = processed_data[2]
            reciever = processed_data[3]
            login = processed_data[4]
            message = processed_data[5]

            self.notify(sender_id, reciever)
            self.renew_clients(mode, sender_id, login)
            self.show_message(sender_id, reciever, message)
            self.message_list.append(f'{mode}~{sender_id}~{reciever}~{login}~{message}')

    def set_tcp_socket(self, socket):
        self.TCPSocket = socket

    def convert(self):
        message = self.ui.textEdit_messageInput.toPlainText()
        if message:
            self.sending(self.MODE_COMMON, self.reciever_address, message, True)

    def sending(self, mode, reciever, message, append):
        time = strftime("%H:%M:%S %d-%m-%Y", localtime())
        final_message = f'{time}{message}'
        if mode != self.MODE_HISTORY:
            self.message_list.append(f'{mode}~me~{reciever}~me~{final_message}')
        self.TCPSocket.sending(mode, reciever, message)

        if append:
            self.ui.textEdit_chatView.append(f'{final_message}')


class New_message_event_handle(QObject):
    message_processing = pyqtSignal()


if __name__ == "__main__":
    import sys
    import socket
    import threading
    import time

    from network import TCPTools, UDPTools

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()
    TCPSocket = TCPTools(application.signal.message_processing)
    application.set_tcp_socket(TCPSocket)

    application.ui.pushbutton_Connect.clicked.connect(application.search)
    application.ui.pushButton_sendMessage.clicked.connect(application.convert)
    application.ui.pushButton_switch.clicked.connect(application.switch_to_private)
    application.ui.pushButton_toall.clicked.connect(application.return_to_all)
    application.ui.pushbutton_Disconnect.clicked.connect(application.leave)

    sys.exit(app.exec_())
