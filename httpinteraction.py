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


class HTTPHandler(BaseHTTPRequestHandler):
    global handler
    handler = Handler()


class HTTPServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def launch_server(self):
        self.server = HTTPServer((self.address, self.port), HTTPHandler)
        self.server.server_forever()
