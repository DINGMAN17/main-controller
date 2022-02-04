import threading
from enum import Enum


class ClientType(Enum):
    ADMIN = "A"
    USER = "U"
    MASS = "M"
    GYRO = "G"
    LEVEL = "L"


class ClientStatus(Enum):
    READY = "ready"
    BUSY = "busy"
    ERROR = "warning"
    LOCK = "lock"


class Client:
    def __init__(self, client_type: ClientType, socket):
        self.client_type = client_type
        self.status = None
        self.lock = threading.Lock()
        self.socket = socket
        self.connected = True

    def set_disconnect(self):
        with self.lock:
            self.connected = False

    def set_status(self, status: ClientStatus):
        with self.lock:
            self.status = status

    @staticmethod
    def identify_client(id_message: str) -> ClientType:
        # sample id_message for admin: IDadmin
        if not id_message.startswith("ID"):
            raise ValueError("invalid id message")
        id_char = id_message[2].upper()
        client_type = ClientType(id_char)
        return client_type
