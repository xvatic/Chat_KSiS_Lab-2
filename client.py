from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pickle
import pyglet
import http_settings
from client_gui import Ui_Form
from time import localtime, strftime
from os import path


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.signal = New_message_event_handle()
        self.signal.message_processing.connect(self.message_processing)
        self.signal.set_button.connect(self.set_button)
        self.signal.show_content_info.connect(self.show_content_info)
        self.signal.new_content.connect(self.new_content_signal)
        self.MODE_CLIENTS = '03'
        self.MODE_CONNECT = '01'
        self.MODE_DISCONNECT = '02'
        self.MODE_COMMON = '00'
        self.MODE_HISTORY = '04'
        self.MODE_CONTENT = '05'
        self.MODE_DELETE_CONTENT = '06'
        self.MODE_FILES_HISTORY = '07'
        self.CONTENT_NAME_KEY = 'content-name'
        self.CONTENT_INFO_KEY = 'content-info'

        self.MARKER_ALL = '10'
        self.message_list = []
        self.content_info = []
        self.clients = {}
        self.upload_files_button_info = {}
        self.download_files_button_info = {}
        self.upload_file_list = []
        self.download_file_list = []
        self.content_info = []
        self.sender_info = ''
        self.reciever_address = self.MARKER_ALL
        self.sound = pyglet.media.load('files/sms_uvedomlenie_na_iphone.wav', streaming=False)

        self.upload_file_layout = self.set_layout_with_scroll_area(
            self.ui.horizontalLayout, self.ui.scrollArea_2)
        self.download_file_layout = self.set_layout_with_scroll_area(
            self.ui.verticalLayout_2, self.ui.scrollArea_3)

    def set_layout_with_scroll_area(self, ui_layout, ui_scroll_area):
        layout = ui_layout
        Widget = Qt.QWidget()
        Widget.setLayout(layout)
        scroll_area = ui_scroll_area
        scroll_area.setWidget(Widget)
        return layout

    def add_button_into_layout(self, name, layout, button_dict, info, action, set_style=False):
        button = Qt.QPushButton(f'{name}')
        if set_style:
            button.setStyleSheet(f'background: #F0F0F0')
        layout.addWidget(button)
        button_dict[button] = info
        button.clicked.connect(action)

    def view_upload_files(self):
        for upload_file_info in self.upload_file_list:
            file_basename = upload_file_info[1]
            self.add_button_into_layout(file_basename, self.download_file_layout,
                                        self.download_files_button_info, upload_file_info[0], self.show_context_menu)
            self.download_file_list.append(
                ['me', self.reciever_address, upload_file_info[0], upload_file_info[1]])

    def clear_upload_file_layout(self):
        for button, file_id in self.upload_files_button_info.items():
            button.setParent(None)
        self.upload_file_list.clear()
        self.upload_files_button_info.clear()

    def download_file(self):
        sender = self.sender_info
        for button, file_id in self.download_files_button_info.items():
            if sender == button:
                for download_file_info in self.download_file_list:
                    if download_file_info[2] == file_id:
                        file_path = QtWidgets.QFileDialog.getSaveFileName(
                            self, 'Save file', f'/Users/zhenya_rs6/Desktop/Load/{download_file_info[3]}')[0]
                        if file_path:
                            response = self.HTTP_client.download(file_id, file_path)
                            self.check_errors_in_response(response)
                        break

    def delete_downloaded_file(self):
        sender = self.sender_info
        for button, file_id in self.download_files_button_info.items():
            if sender == button:
                button.setParent(None)
                deleted_button = button
                for download_file_info in self.download_file_list:
                    if download_file_info[2] == file_id:
                        response = self.HTTP_client.delete_downloaded_file(file_id)
                        if self.check_errors_in_response(response):
                            content = f'{file_id}~{download_file_info[3]}'
                            self.sending(self.MODE_DELETE_CONTENT, self.reciever_address,
                                         f'delete  : [FILE]{download_file_info[3]}', content, True)
                            self.download_file_list.remove(download_file_info)
                            break
                break
        self.download_files_button_info.pop(deleted_button)

    def show_file_info(self):
        sender = self.sender_info
        for button, file_id in self.download_files_button_info.items():
            if sender == button:
                for download_file_info in self.download_file_list:
                    if download_file_info[2] == file_id:
                        response = self.HTTP_client.get_file_info(file_id, download_file_info[3])
                        if self.check_errors_in_response(response):
                            self.show_notification(response[2])

    def show_context_menu(self):
        self.sender_info = self.sender()
        message_box = QtWidgets.QMessageBox()
        message_box.setText('Select')
        button = Qt.QPushButton('Dowload')
        button.clicked.connect(self.download_file)
        message_box.addButton(button, QtWidgets.QMessageBox.AcceptRole)
        button = Qt.QPushButton('Delete')
        button.clicked.connect(self.delete_downloaded_file)
        message_box.addButton(button, QtWidgets.QMessageBox.AcceptRole)
        button = Qt.QPushButton('Info')
        button.clicked.connect(self.show_file_info)
        message_box.addButton(button, QtWidgets.QMessageBox.AcceptRole)

        message_box.exec_()

    def search(self):
        ClIENT_HOST = socket.gethostbyname('localhost')
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
        self.TCPSocket.set_login(application.ui.lineEdit_setName.text())
        self.TCPSocket.connect()
        self.history()

    def new_content_signal(self):
        self.add_button_into_layout(
            self.content_info[0], self.content_info[1], self.content_info[2], self.content_info[3], self.content_info[4])

    def get_basename(self, file_path):
        return path.basename(file_path)

    def upload_file_thread(self, name, file_path):
        if file_path:
            file_basename = self.get_basename(file_path)
            response = self.HTTP_client.upload(file_path)
            if self.check_errors_in_response(response):
                self.content_info = [file_basename, self.upload_file_layout,
                                     self.upload_files_button_info, response[2], self.delete_uploaded_file]
                self.signal.new_content.emit()
                self.upload_file_list.append([response[2], file_basename])
        self.signal.set_button.emit()

    def attach_file(self):
        self.ui.pushButton_sendMessage.setVisible(False)
        file_path = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open File', '/Users/zhenya_rs6/Desktop/TestFiles')[0]
        threading.Thread(target=self.upload_file_thread, args=(
            http_settings.UPLOAD_TYPE, file_path), daemon=True).start()

    def delete_uploaded_file(self):
        sender = self.sender()
        for button, file_id in self.upload_files_button_info.items():
            if sender == button:
                response = self.HTTP_client.delete_uploaded_file(file_id)
                if self.check_errors_in_response(response):
                    button.setParent(None)
                    self.upload_files_button_info.pop(button)
                    for upload_file_info in self.upload_file_list:
                        if upload_file_info[0] == file_id:
                            self.upload_file_list.remove(upload_file_info)
                            break
                    return

    def set_button(self):
        self.ui.pushButton_sendMessage.setVisible(True)

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

        for button, file_id in self.download_files_button_info.items():
            button.setParent(None)
        self.download_files_button_info.clear()
        self.download_file_list.clear()

    def switch_to_private(self):
        for address in self.clients:
            if self.clients[address] == str(self.ui.comboBox_chatParticipants.currentText()):
                self.reciever_address = address
        self.ui.textEdit_chatView.clear()
        for message in self.message_list:
            data = message.split('~')
            if (data[1] == self.reciever_address and data[2] != self.MARKER_ALL) or (data[1] == 'me' and data[2] == self.reciever_address):
                self.show_message(data[1], data[2], data[4])
        self.show_files()

    def show_files(self):
        for button, file_id in self.download_files_button_info.items():
            button.setParent(None)
        self.download_files_button_info.clear()
        if self.reciever_address == self.MARKER_ALL:
            for download_file_info in self.download_file_list:
                if download_file_info[1] == self.reciever_address:
                    file_basename = download_file_info[3]
                    self.add_button_into_layout(file_basename, self.download_file_layout,
                                                self.download_files_button_info, download_file_info[2], self.show_context_menu)

        else:
            for download_file_info in self.download_file_list:
                if download_file_info[1] == self.reciever_address:
                    file_basename = download_file_info[3]
                    self.add_button_into_layout(file_basename, self.download_file_layout,
                                                self.download_files_button_info, download_file_info[2], self.show_context_menu)
                elif download_file_info[0] == self.reciever_address and download_file_info[1] != self.MARKER_ALL:
                    file_basename = download_file_info[3]
                    self.add_button_into_layout(file_basename, self.download_file_layout,
                                                self.download_files_button_info, download_file_info[2], self.show_context_menu)

    def return_to_all(self):
        self.ui.textEdit_chatView.clear()
        self.reciever_address = self.MARKER_ALL
        for message in self.message_list:
            data = message.split('~')
            if data[2] == self.MARKER_ALL:
                self.show_message(data[1], data[2], data[4])

        self.show_files()

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

    def show_content_info(self):
        self.show_notification(self.content_info[0])

    def show_notification(self, info):
        message_box = QMessageBox.information(self, 'title', info)

    def process_content(self, mode, sender, reciever, content):
        if mode == self.MODE_CONTENT:
            content_info = content[self.CONTENT_INFO_KEY].split('~')
            for i in range(1, len(content_info), 2):
                file_basename = content_info[i+1]
                if sender == self.reciever_address:
                    self.add_button_into_layout(file_basename, self.download_file_layout,
                                                self.download_files_button_info, content_info[i], self.show_context_menu)
                elif reciever == self.reciever_address and self.reciever_address == self.MARKER_ALL:
                    self.add_button_into_layout(file_basename, self.download_file_layout,
                                                self.download_files_button_info, content_info[i], self.show_context_menu)
                self.download_file_list.append(
                    [sender, reciever, content_info[i], content_info[i+1]])
        if mode == self.MODE_DELETE_CONTENT:
            content_info = content[self.CONTENT_INFO_KEY].split('~')
            for i in range(0, len(content_info), 2):
                for download_file_info in self.download_file_list:
                    if download_file_info[2] == content_info[i]:
                        for button, file_id in self.download_files_button_info.items():
                            if file_id == content_info[i]:
                                button.setParent(None)
                                self.download_files_button_info.pop(button)
                                break
                        self.download_file_list.remove(download_file_info)
                        break

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

            if processed_data[1] == self.MODE_FILES_HISTORY:
                files = processed_data[2].split('~')
                for i in range(1, len(files), 4):
                    self.download_file_list.append([files[i], files[i+1], files[i+2], files[i+3]])
                self.show_files()
                return
            mode = processed_data[1]
            sender_id = processed_data[2]
            reciever = processed_data[3]
            login = processed_data[4]
            message = processed_data[5]

            self.notify(sender_id, reciever)
            self.renew_clients(mode, sender_id, login)
            if mode != self.MODE_CONTENT and mode != self.MODE_DELETE_CONTENT:
                try:
                    self.show_message(sender_id, reciever, message[self.CONTENT_NAME_KEY])
                except:
                    print(message)
                    self.show_message(sender_id, reciever, message)
            else:
                self.show_message(sender_id, reciever, message[self.CONTENT_NAME_KEY])
            self.process_content(mode, sender_id, reciever, message)
            self.message_list.append(f'{mode}~{sender_id}~{reciever}~{login}~{message}')

    def check_errors_in_response(self, response):
        if response[0] != 200 and response[1] != 'OK':
            self.content_info = [f'ERROR {response[0]} {response[1]} {response[2]}']
            self.signal.show_content_info.emit()
            return False
        return True

    def set_tcp_socket(self, socket):
        self.TCPSocket = socket

    def set_http_client(self, client):
        self.HTTP_client = client
        self.HTTP_client.connect_to_server('', 8080)
        response = self.HTTP_client.initialization()
        self.check_errors_in_response(response)

    def convert(self):
        message = self.ui.textEdit_messageInput.toPlainText()
        if message:
            self.sending(self.MODE_COMMON, self.reciever_address, message, '', True)

        if len(self.upload_file_list) != 0:
            content_info = ''
            content_name = 'upload :'
            for upload_file in self.upload_file_list:
                content_info += f'~{upload_file[0]}~{upload_file[1]}'
                content_name += f'[FILE]{upload_file[1]}'
            print(content_info)
            self.sending(self.MODE_CONTENT, self.reciever_address, content_name, content_info, True)
            self.view_upload_files()
            self.clear_upload_file_layout()
            self.HTTP_client.clear_loaded_data()

    def sending(self, mode, reciever, message, content='', append='False'):
        time = strftime("%H:%M:%S %d-%m-%Y", localtime())

        final_message = f'{time}{message}'
        if content != '':
            message = {self.CONTENT_NAME_KEY: message, self.CONTENT_INFO_KEY: content}
        if mode != self.MODE_HISTORY:
            self.message_list.append(f'{mode}~me~{reciever}~me~{final_message}')
        self.TCPSocket.sending(mode, reciever, message)
        if append:
            self.ui.textEdit_chatView.append(f'{final_message}')


class New_message_event_handle(QObject):
    message_processing = pyqtSignal()
    show_content_info = pyqtSignal()
    new_content = pyqtSignal()
    set_button = pyqtSignal()


if __name__ == "__main__":
    import sys
    import socket
    import threading
    import time

    from network import TCPTools, UDPTools
    import http_client_option

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()
    TCPSocket = TCPTools(application.signal.message_processing)
    application.set_tcp_socket(TCPSocket)

    HTTPClient = http_client_option.HttpClient()
    application.set_http_client(HTTPClient)

    application.ui.pushbutton_Connect.clicked.connect(application.search)
    application.ui.pushButton_sendMessage.clicked.connect(application.convert)
    application.ui.pushButton_switch.clicked.connect(application.switch_to_private)
    application.ui.pushButton_toall.clicked.connect(application.return_to_all)
    application.ui.pushbutton_Disconnect.clicked.connect(application.leave)
    application.ui.pushButton_uploadFile.clicked.connect(application.attach_file)

    sys.exit(app.exec_())
