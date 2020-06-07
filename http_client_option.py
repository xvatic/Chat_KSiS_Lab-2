import os
import http.client
import http_settings


class HTTPClientHandler:
    def __init__(self):
        self.max_file_size = 24000000
        self.max_files_total_size = 150000
        self.unique_client_id = 0
        self.unique_file_id = 0
        self.loaded_file_names = []
        self.unacceptable_ext = ['.exe']
        self.client_upload_length = {}


class HTTPClient():
    def __init__(self, signal):
        self.client_id = None
        self.unique_file_id = 256
        self.file_info = {}

    def connect(self):
        pass

    def set_id(self):
        pass

    def upload(self):
        pass

    def download(self):
        pass

    def get_file_info(self):
        pass

    def delete_uploaded_file(self):
        pass

    def delete_downloaded_file(self):
        pass

    def clear_loaded_data(self):
        pass
