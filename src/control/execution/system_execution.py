import threading

from typing import List

from src.communication.client import Client, ClientType
from src.control.exceptions.process_execptions import NotValidSubsystemException
from src.control.process.admin_controller import AdminController
from src.control.process.system_controller import SystemController
from src.control.process.subsystem_controller import SubsystemController
from src.utils.logging import LogMessage


# TODO: add logging
class SystemExecution:
    def __init__(self):
        self.system_controller = SystemController()
        self.admin_controller = AdminController(self.system_controller)
        self.subsystem_controller = SubsystemController(self.system_controller)

    def get_admin(self) -> Client:
        return self.system_controller.admin

    def get_controllers(self) -> dict:
        return self.system_controller.controller_clients

    def get_users(self) -> List[Client]:
        return self.system_controller.users

    def identify_client(self, client_socket) -> Client:
        client_not_identified = True
        while client_not_identified:
            try:
                new_client = self.create_client(client_socket)
                self.add_valid_client(new_client)
                client_not_identified = False
                return new_client
            except NotValidSubsystemException:
                err = LogMessage.wrong_client()
            except OSError:
                LogMessage.disconnect()
                client_socket.close()
                break

    def create_client(self, client_socket):
        id_msg = self.get_id_message(client_socket)
        client_type = Client.identify_client(id_msg)
        return Client(client_type, client_socket)

    def get_id_message(self, client_socket) -> str:
        id_message = client_socket.recv(1024).decode().strip()
        return id_message

    def add_valid_client(self, new_client):
        if new_client.client_type in [ClientType.ADMIN, ClientType.USER]:
            self.admin_controller.add_admin_or_user(new_client)
        else:
            self.subsystem_controller.add_active_subsystem_client(new_client)
        LogMessage.add_client(new_client.client_type.name)

    def activate_process(self, new_client):
        if new_client.client_type == ClientType.ADMIN:
            self.admin_controller.activate()
            threading.Thread(target=self.send_update_from_subcontroller_to_admin).start()
        elif new_client.client_type != ClientType.USER:
            # if client belongs to sub systems
            self.subsystem_controller.execute_subsystem(new_client)

    def send_update_from_subcontroller_to_admin(self):
        self.clear_old_updates_from_subcontrollers()
        self.system_controller.get_connected_subsystem_status()
        while self.system_controller.get_admin_connection_state():
            update_list = self.subsystem_controller.get_update_from_subcontroller()
            status_list = self.system_controller.get_status_from_queue()
            self.admin_controller.send_update_to_users(status_list + update_list)

    def clear_old_updates_from_subcontrollers(self):
        self.system_controller.clear_status_queue()
        self.subsystem_controller.clear_queue(queue_type="data")
