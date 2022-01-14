import queue
import threading
import time

from message.command.command_executor import *
from message.info.info import MassInfoType
from message.info.info_executor import MassInfoExecutor
from message.message import BaseMessageType
from utils import LogMessage
from message.command.command_invoker import CommandInvoker
from communication.client import *


# TODO: solve admin disconnect, reconnect not recognise problem
class ClientHandler:
    def __init__(self):
        self.admin = None
        self.users = []
        self.controller_clients = {}
        self.clients_status = {}
        self.data_queue = queue.Queue()
        self.info_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.status_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.warning_queue = queue.Queue()
        self.emergency_queue = queue.Queue()

    def run(self, client_socket):
        while True:
            try:
                id_message = client_socket.recv(1024).decode().strip()
                client_type = Client.identify_client(id_message)
                client = Client(client_type, client_socket)
                if self.create_valid_client(client):
                    LogMessage.add_client(client.client_type.name)
                    break

            except ValueError as e:
                err = LogMessage.wrong_client()
                client_socket.send(err.encode())

            except OSError as e:
                LogMessage.disconnect()
                client_socket.close()
                break

    def create_valid_client(self, client):
        if client.client_type == ClientType.ADMIN:
            if (self.admin is not None) and self.admin.connected:
                return False
            self.admin = client
            self.start_admin(client)
            # only one admin user is allowed
            self.users.append(client)
        elif client.client_type == ClientType.USER:
            self.users.append(client)
        elif client.client_type == ClientType.LEVEL:
            self.controller_clients[ClientType.LEVEL] = client
            self.start_controller(client)
        elif client.client_type == ClientType.MASS:
            self.controller_clients[ClientType.MASS] = client
            self.start_controller(client)
        elif client.client_type == ClientType.GYRO:
            self.controller_clients[ClientType.GYRO] = client
            self.start_controller(client)
        return True

    def start_admin(self, client):
        threading.Thread(target=self.send_message_command).start()
        threading.Thread(target=self.send_message_data).start()
        threading.Thread(target=self.receive_message, args=(client,)).start()

    def start_controller(self, client):
        threading.Thread(target=self.request_data, args=(client,)).start()
        threading.Thread(target=self.receive_message, args=(client,)).start()

    def send_message_data(self):
        while self.admin.connected:
            data_list = [data_queue.get() for data_queue in [self.info_queue, self.error_queue] if
                         not data_queue.empty()]

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
                LogMessage.send_to_user(data)
                print(data)

    def send_message_command(self):
        while self.admin.connected:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get()
                    print("received command from user: " + command)
                    client_type = ClientType(command[0])
                    if client_type in self.controller_clients and self.controller_clients[client_type].connected:
                        self.controller_clients[client_type].socket.sendall(command.encode())
                        LogMessage.send_command(command)
                        print("sent command to controller: " + command)
                    else:
                        self.admin.socket.sendall("intended client is not connected".encode())

            except OSError as e:
                self.alert()
                self.controller_clients[client_type].set_disconnect()
                LogMessage.disconnect(client_type.name)

    def request_data(self, client, interval=10):
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
                message = client.socket.recv(1024).decode().strip()
                data_list = message.split("\n")
                for data in data_list:
                    if len(data) > 0:
                        self.process_general_message(data, client.client_type)
            except OSError as e:
                self.alert()
                client.set_disconnect()
                LogMessage.disconnect(client.client_type.name)
            except Exception as e:
                err = LogMessage.bad_request()

    def process_general_message(self, message, client_type):
        if client_type == ClientType.ADMIN:
            self.process_admin_message(message)
        elif client_type in [ClientType.LEVEL, ClientType.MASS, ClientType.GYRO]:  # data, LD1: angle; LD2: load cell
            self.process_controller_message(message)

    def process_admin_message(self, message):
        message_components = message.split("-")
        msg_type = BaseMessageType(message_components[1])
        if msg_type == BaseMessageType.COMMAND:
            self.process_command(message[2:])

    def process_command(self, message):
        command_to_send = CommandInvoker.invoke(message)  # start from "C-L-stop"
        if command_to_send is not None:
            commands_list = command_to_send.split("\n")
            [self.command_queue.put(cmd + "\n") for cmd in commands_list if len(cmd) > 0]

    def process_controller_message(self, message):
        message_components = message.split("-")
        msg_type = BaseMessageType(message_components[1])
        if msg_type == BaseMessageType.DATA:
            LogMessage.receive_data(message)
            self.data_queue.put(message)
        elif msg_type == BaseMessageType.INFO:
            print("info queue: " + message)
            self.process_info(message)
        elif msg_type == BaseMessageType.ERROR:
            self.error_queue.put(message)

    def process_info(self, message):
        # "M-INFO-moved"
        try:
            msg = message.split("-")[-1]
            info, command = MassInfoExecutor.execute(MassInfoType(msg))
            if info is not None:
                self.info_queue.put(info)
            if command is not None:
                self.command_queue.put(command)
        except ValueError as e:
            print(e)

    def alert(self):
        # TODO: how to lock the system when critical condition occurs??
        print("alert!!!!!!")
