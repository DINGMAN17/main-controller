import logging
import threading
from datetime import datetime
import socket

from communication.client_handler import ClientHandler


class ControlServer:
    def __init__(self, timeout=60):
        self.socket = None
        self.timeout = timeout

    def run(self):
        self.connect()
        self.listen()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        port = 8080
        socket_address = ("172.23.11.115", port)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(socket_address)
        self.socket.listen(5)

        logging.info('SERVER Listening at (%s, %s)', "172.23.8.117", port)
        print('SERVER Listening at (%s, %s)', "172.23.11.115", port)

    def listen(self):
        client_handler = ClientHandler()
        while True:
            client_socket, address = self.socket.accept()
            client_socket.setblocking(False)
            logging.info("new client connected at (%s, %s)", address[0], address[1])
            client_socket.settimeout(self.timeout)
            print(datetime.now())
            print('CLIENT Connected:', client_socket, '\n')

            threading.Thread(target=client_handler.run, args=(client_socket,)).start()


if __name__ == "__main__":
    ControlServer(timeout=86400).run()
