from src.control.exceptions.process_execptions import ClientDisconnectException


class TcpService:
    def __init__(self, socket=None):
        self._socket = socket

    @property
    def socket(self):
        return self._socket

    @socket.setter
    def socket(self, socket):
        self._socket = socket

    def receive_message(self):
        try:
            message = self.socket.recv(1024).decode()
            msg_list = message.split("\n")
            valid_messages = [msg.strip() for msg in msg_list if len(msg.strip()) > 0]
            return valid_messages
        except OSError:
            raise ClientDisconnectException()

    def send_message(self, msg):
        try:
            self._socket.sendall(msg.encode())
        except OSError:
            raise ClientDisconnectException()
