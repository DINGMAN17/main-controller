import threading
import socket

from src.communication.client_handler import ClientsHandler
from src.utils.logging import LogMessage


class ControlServer:
    def __init__(self, socket_address, timeout=60):
        self._socket = None
        self._timeout = timeout
        self._socket_address = socket_address

    def run(self):
        self.connect()
        self.accept_client()

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(self._socket_address)
        self._socket.listen(5)
        LogMessage.start_server(self._socket_address)

    def accept_client(self):
        client_handler = ClientsHandler()

        # TODO: rethink about the condition, how to turn the server off
        while True:
            client_socket, address = self._socket.accept()
            client_socket.setblocking(False)
            LogMessage.new_unidentified_client(address)
            client_socket.settimeout(self._timeout)
            threading.Thread(target=client_handler.run, args=(client_socket,)).start()


if __name__ == "__main__":
    ControlServer(socket_address=('192.168.1.6', 8080), timeout=86400).run()
