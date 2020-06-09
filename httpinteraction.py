import socket
import threading
import time
from PyQt5 import QtCore, QtWidgets
from time import localtime, strftime
import pickle
import http.client
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import http_settings


class StorageHandler:
    def __init__(self):
        self.max_file_size = 24000000
        self.max_files_total_size = 150000
        self.unique_client_id = 0
        self.unique_file_id = 0
        self.loaded_file_names = []
        self.unacceptable_ext = ['.exe']
        self.client_upload_length = {}
        self.file_id_and_name = {}

    def get_value_from_header(self, header, needed):
        for header in str(headers).split('\n'):
            if header.startswith(needed):
                return header[len(needed)+2:]
            return False

    def save_file(self, file, file_name, file_ext, file_length, client_id):
        save_str = f'{file_name}{file_ext}'
        file_id = self.get_unique_file_id()
        self.file_id_and_name[file_id] = save_str
        sef.loaded_file_names.append(file_name)
        saved_file = open(f'{http_settings.SERVICE_FILE_PATH}{save_str}', 'wb')
        saved_file.write(file)
        self.client_upload_length[client_id] += file_length

        return file_id

    def delete_file(self, file_id, client_id, type):
        try:
            full_file_name = self.file_id_and_name[file_id]
            if type == http_settings.UPLOAD_TYPE:
                file_size = os.path.getsize(f'{self.SERVICE_FILE_PATH}{full_file_name}')
                self.client_upload_length[client_id] -= file_size

            os.remove(f'{http_settings.SERVICE_FILE_PATH}{full_file_name}')
            self.file_id_and_name.pop(file_id)
            file_name = os.path.splitext(full_file_name)[0]
            self.loaded_file_names.remove(file_name)
            return True
        except:
            return False

    def check_file(self, file_name, file_ext, file_length, client_id):
        err = 'size reached'
        if file_length <= self.max_file_size:
            err = 'unacceptable_ext'
            if not file_ext in self.unacceptable_ext:
                err = 'max_file_size'
                if self.client_upload_length[client_id]+file_length <= self.max_files_total_size:
                    err = 'file name'
                    if not file_name in self.loaded_file_names:
                        err = 'client exists'
                        if str(client_id) != http_settings.NONE:
                            return
        return err

    def get_unique_client_id(self):
        self.unique_client_id += 1
        return self.unique_client_id

    def get_unique_file_id(self):
        self.unique_file_id += 1
        return self.unique_file_id


class HTTPHandler(BaseHTTPRequestHandler):
    global handler
    handler = StorageHandler()


class HTTPServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def launch_server(self):
        self.server = HTTPServer((self.address, self.port), HTTPHandler)
        self.server.server_forever()
