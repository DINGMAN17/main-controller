import string

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
            message = self.socket.recv(1024).decode("UTF-8")
            msg_list = message.split("\n")
            filtered_messages = [self.remove_escape_char(msg).strip() for msg in msg_list]
            valid_messages = [msg for msg in filtered_messages if len(msg) > 0]
            return valid_messages
        except OSError:
            raise ClientDisconnectException()

    def remove_escape_char(self, input_str):
        return ''.join(c for c in input_str if c in string.printable)

    def send_message(self, msg):
        try:
            self._socket.sendall(msg.encode())
        except OSError:
            raise ClientDisconnectException()
