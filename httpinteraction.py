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


class HttpRequestHandler(BaseHTTPRequestHandler):
    global storage
    storage = StorageHandler()

    def perform_INIT(self):
        client_id = storage.get_value_from_header(self.headers, http_settings.CLIENT_ID)
        if client_id == http_settings.NONE:
            unique_client_id = storage.get_unique_client_id()
            storage.client_upload_length[unique_client_id] = 0
            self.send_response(200)
            self.send_header(http_settings.CLIENT_ID, str(unique_client_id))
            self.end_headers()

        else:
            self.send_response(403)
            self.send_header(http_settings.ERROR,  'client exists')
            self.end_headers()

    def perform_GET(self):
        file_id = int(storage.get_value_from_header(self.headers, http_settings.CONTENT_ID))
        try:
            full_file_name = storage.file_id_and_name[file_id]
            self.send_response(200)
            self.end_headers()

            file = open(f'{http_settings.SERVICE_FILE_PATH}{full_file_name}', 'rb').read()
            self.wfile.write(file)

        except:
            self.send_response(404)
            self.send_header(http_settings.ERROR,  http_settings.NO_FILE)
            self.end_headers()

    def perform_TEST(self):
        file_name = str(storage.get_value_from_header(self.headers, http_settings.CONTENT_NAME))
        file_ext = storage.get_value_from_header(self.headers, http_settings.CONTENT_EXT)
        file_length = int(storage.get_value_from_header(self.headers, http_settings.CONTENT_LEN))
        client_id = int(storage.get_value_from_header(self.headers, http_settings.CLIENT_ID))

        err = storage.check_file(file_name, file_ext, file_length, client_id)
        if not err:
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(411)
            self.send_header(http_settings.ERROR, err)
            self.end_headers()

    def perfom_PUT(self):
        file_name = str(storage.get_value_from_header(self.headers, http_settings.CONTENT_NAME))
        file_ext = storage.get_value_from_header(self.headers, http_settings.CONTENT_EXT)
        file_length = int(storage.get_value_from_header(self.headers, http_settings.CONTENT_LEN))
        client_id = int(storage.get_value_from_header(self.headers, http_settings.CLIENT_ID))

        err = storage.check_file(file_name, file_ext, file_length, client_id)

        if not err:
            file = self.rfile.read(file_length)
            file_id = storage.save_file(file, file_name, file_ext, file_length, client_id)
            self.send_response(200)
            self.send_header(http_settings.CONTENT_ID, file_id)
            self.end_headers()
            return

        self.send_response(411)
        self.send_header(http_settings.ERROR, err)
        self.end_headers()

    def perfom_HEAD(self):
        file_id = int(storage.get_value_from_header(self.headers, http_settings.CONTENT_ID))
        try:

            full_file_name = storage.file_id_and_name[file_id]
            file_size = os.path.getsize(f'{http_settings.SERVICE_FILE_PATH}{full_file_name}')

            self.send_response(200)
            self.send_header(http_settings.CONTENT_SIZE, file_size)
            self.end_headers()

        except:
            self.send_response(404)
            self.send_header(http_settings.ERROR,  http_settings.NO_FILE)
            self.end_headers()

    def perfom_DELETE(self):
        file_id = int(storage.get_value_from_header(self.headers, http_settings.CONTENT_ID))
        client_id = int(storage.get_value_from_header(self.headers, http_settings.CLIENT_ID))
        type = storage.get_value_from_header(self.headers, http_settings.REMOVABLE_TYPE)

        if storage.delete_file(file_id, client_id, type):
            self.send_response(200)
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header(http_settings.ERROR, http_settings.NO_FILE)
            self.end_headers()

    def perfom_CLEAR(self):
        client_id = int(storage.get_value_from_header(self.headers, http_settings.CLIENT_ID))
        storage.client_upload_length[client_id] = 0
        self.send_response(200)
        self.end_headers()


class HttpServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def launch_server(self):
        self.server = HTTPServer((self.address, self.port), HttpRequestHandler)
        self.server.serve_forever()


if __name__ == '__main__':
    serv = HttpServer('', 8080)
    serv.launch_server()
