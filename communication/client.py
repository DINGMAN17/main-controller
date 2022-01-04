from enum import Enum, auto


class ClientType(Enum):
    ADMIN = "A"
    USER = "U"
    MASS = "M"
    GYRO = "G"
    LEVEL = "L"


class Client:
    # TODO: integrate client class to client_handler class
    def __init__(self, client_type, socket):
        self.client_type = client_type
        self.socket = socket

    def check_connection(self):
        pass


if __name__ == "__main__":
    str = "hello"
    print(str.upper())