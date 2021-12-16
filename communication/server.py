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
        self.connect()
        self.listen()

    def connect(self):
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print('HOST IP:', host_ip)
        socket_address = (host_ip, 12345)
        self.socket.bind(socket_address)
        self.socket.listen(5)

        if self.debug:
            print(datetime.now())
            print('SERVER Listening...', '\n')

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print(address)
            client_socket.settimeout(self.timeout)
            if self.debug:
                print(datetime.now())
                print('CLIENT Connected:', client_socket, '\n')

            handler = ClientHandler(client_socket, address)
            threading.Thread(target=handler.send_video).start()


if __name__ == "__main__":
    Server(timeout=86400, debug=True).run()
