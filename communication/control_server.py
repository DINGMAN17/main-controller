import threading
import socket

from communication.client_handler import ClientHandler
from utils import LogMessage


class ControlServer:
    def __init__(self, timeout=60):
        self.socket = None
        self.timeout = timeout

    def run(self):
        self.connect()
        self.accept_client()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = socket.gethostbyname(socket.gethostname())
        port = 8080
        socket_address = (host_ip, port)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(socket_address)
        self.socket.listen(5)

        LogMessage.start_server((host_ip, port))

    def accept_client(self):
        client_handler = ClientHandler()
        while True:
            client_socket, address = self.socket.accept()
            client_socket.setblocking(False)
            LogMessage.new_unidentified_client(address)
            client_socket.settimeout(self.timeout)
            threading.Thread(target=client_handler.run, args=(client_socket,)).start()


if __name__ == "__main__":
    ControlServer(timeout=86400).run()
