import threading
import socket
import time
import pickle


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

    def send(self):
        while not self.stopped:
            try:
                while not self.stopped:
                    message = {1: str(self.host), 2: str(self.port)}
                    final_message = pickle.dumps(message)
                    self.socket.sendto(final_message, ('<broadcast>', self.port))
                    time.sleep(2)
            except:
                pass

    def recieve(self):
        while not self.stopped:
            try:
                while not self.stopped:
                    data, address = self.socket.recvfrom(1024)
                    message = pickle.loads(data)
                    self.recieved_ip = message[1]
                    self.recieved_port = message[2]

                    if self.address_request:
                        message = {1: str(self.host), 2: str(self.port)}
                        final_message = pickle.dumps(message)
                        self.socket.sendto(
                            final_message, address)
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
