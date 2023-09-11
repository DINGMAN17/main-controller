import threading
from enum import Enum

from src.communication.tcp_service import TcpService
from src.control.exceptions.process_execptions import UnknownClientException, NotValidSubsystemException


class ClientType(Enum):
    ADMIN = "A"
    USER = "U"
    MASS = "M"
    GYRO = "G"
    LEVEL = "L"


class ClientStatus(Enum):
    """
    An Enum of status of a client.

    Attributes:
    WAIT: before the client is identified.
    BUSY: when the system is performing an exclusive task.
    EMERG: stop all the operations.
    ERROR: stop all the operations except auto-stabilizing & auto-levelling.
    LOCK: when the system is stopping, new command is not allowed.
    """

    WAIT = "wait"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    EMERG = "emergency"
    LOCK = "lock"  # when the system is stopping


class Client:
    def __init__(self, client_type: ClientType, socket, name=None):
        self._client_type = client_type
        self._status = ClientStatus.WAIT
        self.lock = threading.Lock()
        self.tcp_service = TcpService(socket)
        self._connected = True
        self._name = name

    @property
    def client_type(self):
        return self._client_type

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value: bool):
        with self.lock:
            self._connected = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: ClientStatus):
        with self.lock:
            self._status = status

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @staticmethod
    def identify_client(id_message: str) -> ClientType:
        # sample id_message for admin: IDadmin
        if not id_message.startswith("ID"):
            raise UnknownClientException()
        id_char = id_message[2].upper()
        try:
            client_type = ClientType(id_char)
        except ValueError:
            raise NotValidSubsystemException()
        return client_type
