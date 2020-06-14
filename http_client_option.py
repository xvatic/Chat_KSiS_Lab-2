import os
import http.client
import http_settings


class HttpClient():
    def __init__(self):
        self.client_id = None
        self.unique_file_id = 256
        self.file_info = {}
        self.max_file_size = 85000
        self.max_files_total_size = 150000
        self.uploading_buffer = {}
        self.unacceptable_ext = ['.exe', '.out']
        self.current_size = 0

    def check_file(self, file_name, file_ext, file_length):
        err = 'large file'
        if file_length <= self.max_file_size:
            err = 'unacceptable_ext'
            if not file_ext in self.unacceptable_ext:
                err = 'total size reached'
                if self.current_size+file_length <= self.max_files_total_size:
                    err = 'file exists'
                    for key in self.uploading_buffer.keys():
                        if self.uploading_buffer[key][0] == file_name:

                            return err
                    return
        return err

    def connect_to_server(self, address, port):
        self.connection = http.client.HTTPConnection(address, port)

    def get_unique_file_id(self):
        self.unique_file_id += 1
        return id(self.unique_file_id)

    def initialization(self):
        headers = {http_settings.CLIENT_ID: str(self.client_id)}
        self.connection.request(method='INIT', url='/', body='', headers=headers)
        response = self.connection.getresponse()
        error = response.getheader(http_settings.ERROR)
        if not error:
            self.client_id = response.getheader(http_settings.CLIENT_ID)
        return response.status, response.reason, error

    def upload(self, file_path):
        full_file_name = os.path.basename(file_path)
        file_name = str(self.get_unique_file_id())
        file_extension = os.path.splitext(full_file_name)[1]
        file_size = os.path.getsize(file_path)
        headers = {http_settings.CONTENT_NAME: file_name, http_settings.CONTENT_EXT: file_extension,
                   http_settings.CLIENT_ID: str(self.client_id), http_settings.CONTENT_LEN: str(file_size)}
        self.connection.request(method='TEST', url='/', headers=headers)
        response = self.connection.getresponse()
        error = response.getheader(http_settings.ERROR)
        client_error = self.check_file(full_file_name, file_extension, file_size)
        if not error and not client_error:
            try:
                file = open(file_path, 'rb').read()
                self.connection.request(method='PUT', url='/', body=file, headers=headers)
                response = self.connection.getresponse()
                info = response.getheader(http_settings.ERROR)
                if not error:
                    self.current_size += file_size
                    file_id = response.getheader(http_settings.CONTENT_ID)
                    self.uploading_buffer[file_id] = [full_file_name, file_size]
                    self.file_info[file_id] = file_name
                    info = file_id
            except Exception as error:
                info = error
            return response.status, response.reason, info
        else:
            return 0, 'UPLOADING ERROR', client_error
        return response.status, response.reason, error

    def download(self, file_id, file_path):
        headers = {http_settings.CONTENT_ID: str(file_id)}
        self.connection.request(method='GET', url='/', headers=headers)
        response = self.connection.getresponse()
        error = response.getheader(http_settings.ERROR)
        if not error:
            file = response.read()
            saved_file = open(file_path, 'wb')
            saved_file.write(file)
            error = None
        return response.status, response.reason, error

    def get_file_info(self, file_id, file_name):
        headers = {http_settings.CONTENT_ID: str(file_id)}
        self.connection.request(method='HEAD', url='/', headers=headers)
        response = self.connection.getresponse()
        error = response.getheader(http_settings.ERROR)
        if not error:
            file_size = response.getheader(http_settings.CONTENT_SIZE)
            return response.status, response.reason, f'Name : {file_name}\nSize : {file_size}'
        return response.status, response.reason, error

    def delete_file(self, file_id, removable_type):
        headers = {http_settings.CONTENT_ID: str(file_id), http_settings.CLIENT_ID: str(
            self.client_id), http_settings.REMOVABLE_TYPE: removable_type}
        self.connection.request(method='DELETE', url='/', headers=headers)
        response = self.connection.getresponse()
        error = response.getheader(http_settings.ERROR)
        return response.status, response.reason, error

    def delete_uploaded_file(self, file_id):
        self.current_size -= self.uploading_buffer[file_id][1]
        self.uploading_buffer.pop(file_id)
        return self.delete_file(file_id, http_settings.UPLOAD_TYPE)

    def delete_downloaded_file(self, file_id):
        return self.delete_file(file_id, http_settings.DOWNLOAD_TYPE)

    def clear_loaded_data(self):
        headers = {http_settings.CLIENT_ID: str(self.client_id)}
        self.connection.request(method='CLEAR', url='/', headers=headers)
        self.current_size = 0
        self.uploading_buffer.clear()
        response = self.connection.getresponse()
