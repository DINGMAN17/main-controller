import logging
import queue
import threading
from command.commandinvoker import CommandInvoker


class ClientHandler:
    def __init__(self):
        self.has_admin = False
        self.users = []
        self.controller_clients = {}
        self.command_queue = queue.Queue()
        self.level_data_queue = queue.Queue()
        self.mass_data_queue = queue.Queue()
        self.gyro_data_queue = queue.Queue()

    def send_message_data(self):
        while True:
            data_list = [data_queue.get() for data_queue in [self.level_data_queue, self.gyro_data_queue,
                                                             self.mass_data_queue] if not data_queue.empty()]
            for data in data_list:
                [user_socket.send(data.encode()) for user_socket in self.users]
                logging.info("data sent to user: %s", data)
                print(data)

    def send_message_command(self):
        try:
            while True:
                if not self.command_queue.empty():
                    command = self.command_queue.get()
                    print(command)
                    if command[0] in self.controller_clients:
                        self.controller_clients[command[0]].send(command.encode())
                        logging.info("command sent to subcontroller: %s", command)
        except OSError as e:
            logging.exception("Connection error while sending command")

    def receive_message(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            self.process_message(data)

    def process_message(self, data):
        if data.startswith("CMD"):
            try:
                CommandInvoker.invoke(data, self.command_queue)
            except ValueError:
                logging.exception("invalid command")
                print("Please enter a valid command")
        elif data.startswith("L"):  # data, DL1: angle; DL2: load cell
            self.level_data_queue.put(data)
        elif data.startswith("M"):
            self.mass_data_queue.put(data)
        elif data.startswith("G"):
            self.gyro_data_queue.put(data)

    def start_user(self, client_socket):
        threading.Thread(target=self.send_message_command).start()
        threading.Thread(target=self.send_message_data).start()
        threading.Thread(target=self.receive_message, args=(client_socket,)).start()

    def start_controller(self, client_socket):
        threading.Thread(target=self.receive_message, args=(client_socket,)).start()

    def run(self, client_socket):
        try:
            while True:
                id_message = client_socket.recv(1024).decode()
                if id_message.startswith("ID"):
                    if ("admin" in id_message) and (not self.has_admin):
                        self.start_user(client_socket)
                        # only one admin user is allowed
                        self.has_admin = True
                        self.users.append(client_socket)
                        logging.info("admin is added")
                    elif "user" in id_message:
                        self.users.append(client_socket)
                        logging.info("a new user is added")
                    elif "level" in id_message:
                        self.controller_clients["L"] = client_socket
                        self.start_controller(client_socket)
                        logging.info("levelling controller is added")
                    elif "mass" in id_message:
                        self.controller_clients["M"] = client_socket
                        self.start_controller(client_socket)
                        logging.info("mass controller is added")
                    elif "gyro" in id_message:
                        self.controller_clients["G"] = client_socket
                        self.start_controller(client_socket)
                        logging.info("gyro is added")
                    break

        except OSError as e:
            logging.exception("socket connection error")
            client_socket.close()
