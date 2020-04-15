import threading
import socket
import time


class UDPTools():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recieved_ip = ''
        self.recieved_port = 0
        self.address_request = False

    def address_request_flag(self):
        self.address_request = True

    def bind(self, host, port):
        self.socket.bind((host, port))

    def set_broadcast(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def set_reusable(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def sending(self, message):
        self.socket.sendto(f'{message}'.encode("utf-8"), ('<broadcast>', self.port))

    def send(self):
        while not self.stopped:
            try:
                while not self.stopped:
                    self.sending(f'{str(self.host)} {str(self.port)}')
                    time.sleep(2)
            except:
                pass

    def recieve(self):
        while not self.stopped:
            try:
                while not self.stopped:
                    data, address = self.socket.recvfrom(1024)
                    message = data.decode("utf-8").split()
                    print(address)
                    self.recieved_ip = message[0]
                    self.recieved_port = message[1]
                    print(message[0])
                    if self.address_request:
                        self.socket.sendto(
                            (f'{self.host} {str(self.port)}').encode("utf-8"), address)
                    time.sleep(2)
            except OSError:
                pass

    def start_UDP_thread_send(self):
        self.stopped = False
        Thread_send = threading.Thread(target=self.send, daemon=True)
        Thread_send.start()

    def start_UDP_thread_recieve(self):
        self.stopped = False
        Thread_recieve = threading.Thread(target=self.recieve, daemon=True)
        Thread_recieve.start()

    def transfer_value(self):
        return self.recieved_ip, self.recieved_port

    def stopped_connection(self):
        self.stopped = True
        self.socket.close()
