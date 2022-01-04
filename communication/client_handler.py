import logging
import queue
import threading
from command.commandinvoker import CommandInvoker
from communication.client import *
from communication.message import MessageType


class ClientHandler:
    def __init__(self):
        self.has_admin = False
        self.users = []
        self.controller_clients = {}
        self.command_queue = queue.Queue()
        self.level_data_queue = queue.Queue()
        self.mass_data_queue = queue.Queue()
        self.gyro_data_queue = queue.Queue()

    def run(self, client_socket):
        while True:
            try:
                id_message = client_socket.recv(1024).decode()
                client_type = self.identify_client(id_message)

                if (client_type == ClientType.ADMIN) and (not self.has_admin):
                    self.start_user(client_socket)
                    # only one admin user is allowed
                    self.has_admin = True
                    self.users.append(client_socket)
                    logging.info("admin is added")
                elif client_type == ClientType.USER:
                    self.users.append(client_socket)
                    logging.info("a new user is added")
                elif client_type == ClientType.LEVEL:
                    self.controller_clients[ClientType.LEVEL] = client_socket
                    self.start_controller(client_socket)
                    logging.info("levelling controller is added")
                elif client_type == ClientType.MASS:
                    self.controller_clients[ClientType.MASS] = client_socket
                    self.start_controller(client_socket)
                    logging.info("mass controller is added")
                elif client_type == ClientType.GYRO:
                    self.controller_clients[ClientType.GYRO] = client_socket
                    self.start_controller(client_socket)
                    logging.info("gyro is added")
                break

            except ValueError as e:
                err = "ERROR: wrong client type"
                logging.exception(err)
                client_socket.send(err.encode())

            except OSError as e:
                logging.exception("socket connection error occurred while trying to identify client type")
                client_socket.close()
                break

    def identify_client(self, id_message):
        # sample id_message for admin: IDadmin
        if not id_message.startswith("ID"):
            raise ValueError("invalid id message")
        id_char = id_message[2].upper()
        client_type = ClientType(id_char)
        return client_type

    def start_user(self, client_socket):
        threading.Thread(target=self.send_message_command).start()
        threading.Thread(target=self.send_message_data).start()
        threading.Thread(target=self.receive_message, args=(client_socket,)).start()

    def start_controller(self, client_socket):
        threading.Thread(target=self.receive_message, args=(client_socket,)).start()

    def send_message_data(self):
        try:
            while True:
                data_list = [data_queue.get() for data_queue in [self.level_data_queue, self.gyro_data_queue,
                                                                 self.mass_data_queue] if not data_queue.empty()]
                for data in data_list:
                    [user_socket.send(data.encode()) for user_socket in self.users]
                    logging.info("data sent to user: %s", data)
                    print(data)
        except OSError as e:
            logging.exception("Connection error while sending data to user")

    def send_message_command(self):
        try:
            while True:
                if not self.command_queue.empty():
                    command = self.command_queue.get()
                    print(command)
                    client_type = ClientType(command[0])
                    if client_type in self.controller_clients:
                        self.controller_clients[client_type].send(command.encode())
                        logging.info("command sent to subcontroller: %s", command)
        except OSError as e:
            logging.exception("Connection error while sending command to sub-controller")

    def receive_message(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                self.process_message(data)
        except OSError as e:
            logging.exception("Connection error while receiving message")

    def process_message(self, data):
        try:
            msg_type = MessageType(data[0])
            if msg_type == MessageType.COMMAND:
                CommandInvoker.invoke(data, self.command_queue)
            elif msg_type == MessageType.LEVEL_DATA:  # data, DL1: angle; DL2: load cell
                self.level_data_queue.put(data)
            elif msg_type == MessageType.MASS_DATA:
                self.mass_data_queue.put(data)
            elif msg_type == MessageType.GYRO_DATA:
                self.gyro_data_queue.put(data)

        except ValueError:
            logging.exception("invalid message type")
            print("Please send a valid message")




