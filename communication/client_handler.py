import queue
import threading
import time

from message.command.command_executor import *
from utils import LogMessage
from message.command.command_invoker import CommandInvoker
from communication.client import *
from message.message import MessageType


class ClientHandler:
    def __init__(self):
        self.admin = None
        self.users = []
        self.controller_clients = {}
        self.alert_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.level_data_queue = queue.Queue()
        self.mass_data_queue = queue.Queue()
        self.gyro_data_queue = queue.Queue()

    def run(self, client_socket):
        while True:
            try:
                id_message = client_socket.recv(1024).decode().strip()
                client_type = Client.identify_client(id_message)
                client = Client(client_type, client_socket)

                if (client.client_type == ClientType.ADMIN) and (self.admin is None):
                    self.admin = client
                    self.start_admin(client)
                    # only one admin user is allowed
                    self.users.append(client)
                    LogMessage.add_client(client.client_type.name)
                elif client.client_type == ClientType.USER:
                    self.users.append(client)
                    LogMessage.add_client(client.client_type.name)
                elif client.client_type == ClientType.LEVEL:
                    self.controller_clients[ClientType.LEVEL] = client
                    self.start_controller(client)
                    LogMessage.add_client(client.client_type.name)
                elif client.client_type == ClientType.MASS:
                    self.controller_clients[ClientType.MASS] = client
                    self.start_controller(client)
                    LogMessage.add_client(client.client_type.name)
                elif client.client_type == ClientType.GYRO:
                    self.controller_clients[ClientType.GYRO] = client
                    self.start_controller(client)
                    LogMessage.add_client(client.client_type.name)
                break

            except ValueError as e:
                err = LogMessage.wrong_client()
                client_socket.send(err.encode())

            except OSError as e:
                LogMessage.disconnect()
                client_socket.close()
                break

    def start_admin(self, client):
        threading.Thread(target=self.send_message_command).start()
        threading.Thread(target=self.send_message_data).start()
        threading.Thread(target=self.receive_message, args=(client,)).start()

    def start_controller(self, client):
        threading.Thread(target=self.request_data, args=(client,)).start()
        threading.Thread(target=self.receive_message, args=(client,)).start()

    def send_message_data(self):
        while self.admin.connected:
            data_list = [data_queue.get() for data_queue in [self.level_data_queue, self.gyro_data_queue,
                                                             self.mass_data_queue] if not data_queue.empty()]
            for data in data_list:
                for user in self.users:
                    try:
                        user.socket.sendall(data.encode())
                    except OSError as e:
                        if user.client_type != ClientType.ADMIN:
                            self.users.remove(user)
                            LogMessage.remove_user()
                        else:
                            self.admin.set_disconnect()
                            self.alert()
                LogMessage.send_data(data)
                print(data)

    def send_message_command(self):
        while self.admin.connected:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get()
                    print(command)
                    client_type = ClientType(command[0])
                    if client_type in self.controller_clients and self.controller_clients[client_type].connected:
                        self.controller_clients[client_type].socket.sendall(command.encode())
                        LogMessage.send_command(command)
                    else:
                        self.admin.socket.sendall("intended client is not connected".encode())

            except OSError as e:
                self.alert()
                self.controller_clients[client_type].set_disconnect()
                LogMessage.disconnect(client_type.name)

    def request_data(self, client, interval=2):
        while client.connected:
            try:
                command = None
                if client.client_type == ClientType.MASS:
                    command = MassCommandExecutor.get_position()
                elif client.client_type == ClientType.GYRO:
                    command = GyroCommandExecutor.get_data()
                elif client.client_type == ClientType.LEVEL:
                    command = LevellingCommandExecutor.request_data()
                client.socket.sendall(command.encode())
                time.sleep(interval)
            except OSError:
                self.alert()
                client.set_disconnect()
                LogMessage.disconnect(client.client_type.name)

    def receive_message(self, client):
        while client.connected:
            try:
                data = client.socket.recv(1024).decode().strip()
                self.process_message(data)
            except ValueError as e:
                err = LogMessage.bad_request()
                client.socket.sendall(err)
            except (OSError, IndexError) as e:
                self.alert()
                client.set_disconnect()
                LogMessage.disconnect(client.client_type.name)

    def process_message(self, data):
        msg_type = MessageType(data[0])
        if msg_type == MessageType.COMMAND:
            command_to_send = CommandInvoker.invoke(data)
            if command_to_send is not None:
                self.command_queue.put(command_to_send)
        elif msg_type == MessageType.LEVEL_DATA:  # data, LD1: angle; LD2: load cell
            self.level_data_queue.put(data)
        elif msg_type == MessageType.MASS_DATA:
            self.mass_data_queue.put(data)
        elif msg_type == MessageType.GYRO_DATA:
            self.gyro_data_queue.put(data)

    def alert(self):
        # TODO: how to lock the system when critical condition occurs??
        print("alert!!!!!!")