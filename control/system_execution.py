import threading

from communication.client import Client, ClientType
from control.basic_execution import BasicExecution
from utils import LogMessage


class SystemExecution:
    def __init__(self):
        self.new_client = None
        self.basic_execution = BasicExecution()

    def identify_client(self, client_socket) -> None:
        client_not_identified = True
        while client_not_identified:
            try:
                id_message = client_socket.recv(1024).decode().strip()
                client_type = Client.identify_client(id_message)
                client = Client(client_type, client_socket)
                valid_client = self.create_valid_client(client)
                if valid_client:
                    self.new_client = client
                    LogMessage.add_client(client.client_type.name)
                    client_not_identified = False
            except ValueError:
                err = LogMessage.wrong_client()
                client_socket.send(err.encode())
            except OSError:
                LogMessage.disconnect()
                client_socket.close()
                break

    def create_valid_client(self, client: Client) -> bool:
        valid_client = True
        if client.client_type == ClientType.ADMIN:
            self.basic_execution.admin = client
            # only one admin user is allowed
            self.basic_execution.users.append(client)
        elif client.client_type == ClientType.USER:
            self.basic_execution.users.append(client)
        elif client.client_type == ClientType.LEVEL:
            self.basic_execution.controller_clients[ClientType.LEVEL] = client
        elif client.client_type == ClientType.MASS:
            self.basic_execution.controller_clients[ClientType.MASS] = client
        elif client.client_type == ClientType.GYRO:
            self.basic_execution.controller_clients[ClientType.GYRO] = client
        else:
            valid_client = False
        return valid_client

    def start_client(self):
        if self.new_client.client_type == ClientType.ADMIN:
            self.start_admin()
        if self.new_client.client_type in [ClientType.LEVEL, ClientType.MASS, ClientType.GYRO]:
            self.start_controller()

    def start_admin(self):
        threading.Thread(target=self.basic_execution.send_command_process).start()
        threading.Thread(target=self.basic_execution.send_message).start()
        threading.Thread(target=self.basic_execution.send_data).start()
        threading.Thread(target=self.basic_execution.receive_message, args=(self.new_client,)).start()

    def start_controller(self):
        threading.Thread(target=self.basic_execution.request_data, args=(self.new_client,)).start()
        threading.Thread(target=self.basic_execution.receive_message, args=(self.new_client,)).start()
