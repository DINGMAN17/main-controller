import logging
import threading
from datetime import datetime
import socket

from client_handler import ClientHandler


class Server:
    def __init__(self, timeout=60, debug=False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = timeout
        self.debug = debug

    def run(self):
        if self.debug:
            logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s - %(message)s',
                                level=logging.DEBUG)
        self.connect()
        self.listen()

    def connect(self):
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print('HOST IP:', host_ip)
        socket_address = ("192.168.10.104", 8080)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(socket_address)
        self.socket.listen(5)

        if self.debug:
            logging.debug('SERVER Listening...')
            print(datetime.now())
            print('SERVER Listening...', '\n')

    def listen(self):
        client_handler = ClientHandler()
        while True:
            client_socket, address = self.socket.accept()
            client_socket.setblocking(False)
            if self.debug:
                logging.debug(address[0])
                print('device with address:', address)
            client_socket.settimeout(self.timeout)
            if self.debug:
                print(datetime.now())
                print('CLIENT Connected:', client_socket, '\n')

            threading.Thread(target=client_handler.run, args=(client_socket,)).start()


if __name__ == "__main__":
    Server(timeout=86400, debug=True).run()
