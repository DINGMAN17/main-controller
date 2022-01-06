from enum import Enum


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
        self.connected = True

    def set_disconnect(self):
        self.connected = False

    @staticmethod
    def identify_client(id_message):
        # sample id_message for admin: IDadmin
        if not id_message.startswith("ID"):
            raise ValueError("invalid id message")
        id_char = id_message[2].upper()
        client_type = ClientType(id_char)
        return client_type

