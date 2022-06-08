from src.communication.client import Client, ClientType
from src.control.exceptions.process_execptions import NotValidSubsystemException
from src.control.process.admin_controller import AdminController
from src.control.process.status_controller import StatusController
from src.control.process.subsystem_controller import SubsystemController
from src.utils.logging import LogMessage


# TODO: add logging
class SystemExecution:
    def __init__(self):
        self.status_controller = StatusController()
        self.admin_controller = AdminController(self.status_controller)
        self.subsystem_controller = SubsystemController(self.status_controller)

    def get_admin(self):
        return self.status_controller.admin

    def get_controllers(self):
        return self.status_controller.controller_clients

    def get_users(self):
        return self.status_controller.users

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

    def get_id_message(self, client_socket):
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
        elif new_client.client_type != ClientType.USER:
            self.subsystem_controller.execute_subsystem(new_client)
