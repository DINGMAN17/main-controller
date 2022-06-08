import threading
import socket

from src.communication.client_handler import ClientHandler
from src.utils.logging import LogMessage


class ControlServer:
    def __init__(self, socket_address, timeout=60):
        self.socket = None
        self.timeout = timeout
        self.socket_address = socket_address

    def run(self):
        self.connect()
        self.accept_client()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.socket_address)
        self.socket.listen(5)
        LogMessage.start_server(self.socket_address)

    def accept_client(self):
        client_handler = ClientHandler()
        while True:
            client_socket, address = self.socket.accept()
            client_socket.setblocking(False)
            LogMessage.new_unidentified_client(address)
            client_socket.settimeout(self.timeout)
            threading.Thread(target=client_handler.run, args=(client_socket,)).start()


if __name__ == "__main__":
    ControlServer(socket_address=('192.168.1.6', 8080), timeout=86400).run()
