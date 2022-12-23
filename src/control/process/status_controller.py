import queue
import threading
from typing import Optional, List, Dict

from src.communication.client import ClientStatus, ClientType, Client
from src.control.exceptions.process_execptions import IntendedClientIsNotConnectedException, \
    IntendedClientDoesNotExistException
from src.control.process.paser import Paser
from src.control.task_list import Tasks
from src.message.command.command_executor import Command
from src.utils.logging import LogMessage


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]


class StatusController(Singleton):
    def __init__(self):
        self._admin: Optional[Client] = None
        self._users: List[Optional[Client]] = []
        self._controller_clients: Dict[Optional[ClientType]] = {}
        self._tasks_list: Tasks = Tasks()
        self._current_integrated_command: Optional[Command] = None
        self._status_queue = queue.Queue()
        self._current_task_queue = queue.Queue()
        self._lock = threading.RLock()

    @property
    def current_integrated_command(self):
        return self._current_integrated_command

    @current_integrated_command.setter
    def current_integrated_command(self, integrated_command):
        with self._lock:
            self._current_integrated_command = integrated_command

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def admin(self, admin):
        with self._lock:
            self._admin = admin

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, users):
        self._users = users

    def add_user(self, user):
        with self._lock:
            self._users.append(user)

    @property
    def status_queue(self):
        return self._status_queue

    def get_status_from_queue(self) -> List[ClientStatus]:
        with self._lock:
            status_list = []
            while not self.status_queue.empty():
                status_list.append(self.status_queue.get())
            return status_list

    def clear_status_queue(self):
        with self.status_queue.mutex:
            self.status_queue.queue.clear()

    @property
    def controller_clients(self):
        return self._controller_clients

    @controller_clients.setter
    def controller_clients(self, controller_clients: dict):
        with self._lock:
            self._controller_clients = controller_clients

    def add_controller_client(self, controller: Client):
        with self._lock:
            self._controller_clients[controller.client_type] = controller

    @property
    def tasks_list(self):
        return self._tasks_list

    def get_subsystem_client(self, client_type: ClientType) -> Client:
        with self._lock:
            try:
                return self.controller_clients[client_type]
            except KeyError:
                raise IntendedClientDoesNotExistException()

    def get_connected_subsystem_status(self):
        with self._lock:
            [self.add_status_to_queue(client_type, client.status) for client_type, client in
             self.controller_clients.items()]

    def get_subsystem_status(self, recipient_type: ClientType) -> ClientStatus:
        with self._lock:
            if recipient_type in self.controller_clients:
                recipient = self.get_subsystem_client(recipient_type)
                if recipient.connected:
                    return recipient.status
                else:
                    raise IntendedClientIsNotConnectedException()
            else:
                raise IntendedClientDoesNotExistException()

    def check_recipient_status_for_busy_command(self, recipient_type: ClientType) -> bool:
        with self._lock:
            recipient_status = self.get_subsystem_status(recipient_type)
            return recipient_status == ClientStatus.READY

    def update_recipient_status_after_sending_command(self, command: Command) -> [ClientStatus, ClientStatus]:
        with self._lock:
            update_status = False
            new_status = None
            if command.lock_system:
                new_status = ClientStatus.LOCK
                update_status = True
            elif command.busy_command:
                new_status = ClientStatus.BUSY
                update_status = True
            if update_status:
                self.update_and_add_status(command.recipient, new_status)
            return update_status, new_status

    def update_and_add_status(self, subsystem_type: ClientType, new_status: ClientStatus):
        with self._lock:
            subsystem = self.controller_clients[subsystem_type]
            subsystem.status = new_status
            print("update status")
            LogMessage.update_client_status(subsystem_type, new_status)
            self.add_status_to_queue(subsystem_type, new_status)

    def add_status_to_queue(self, subsystem_type: ClientType, new_status: ClientStatus):
        with self._lock:
            status_msg = Paser.parse_status_msg_send(subsystem_type, new_status)
            self._status_queue.put(status_msg)

    def get_admin_connection_state(self) -> bool:
        with self._lock:
            return self.admin.connected

    def update_admin_connection_state(self, connection_state: bool):
        with self._lock:
            self.admin.connected = connection_state

    def update_subsystem_connection_state(self, connection_state: bool, subsystem_type: ClientType):
        with self._lock:
            subsystem_client = self.controller_clients[subsystem_type]
            subsystem_client.connected = connection_state
