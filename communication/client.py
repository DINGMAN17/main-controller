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
    LOCK = "lock" # when the system is stopping


class Client:
    def __init__(self, client_type: ClientType, socket):
        self._client_type = client_type
        self._status = None
        self.lock = threading.Lock()
        self.socket = socket
        self._connected = True

    @property
    def client_type(self):
        return self._client_type

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        with self.lock:
            self._connected = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: ClientStatus):
        with self.lock:
            self._status = status

    @staticmethod
    def identify_client(id_message: str) -> ClientType:
        # sample id_message for admin: IDadmin
        if not id_message.startswith("ID"):
            raise ValueError("invalid id message")
        id_char = id_message[2].upper()
        client_type = ClientType(id_char)
        return client_type
