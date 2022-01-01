import queue
import threading
import socket
from command.commandinvoker import CommandInvoker


class ClientHandler:
    def __init__(self):
        self.has_admin = False
        self.controller_clients = {}
        self.command_queue = queue.Queue()
        self.level_data_queue = queue.Queue()
        self.mass_data_queue = queue.Queue()
        self.gyro_data_queue = queue.Queue()

    def send_message_data(self, user_socket):
        while True:
            data_list = [data_queue.get() for data_queue in [self.level_data_queue, self.gyro_data_queue,
                                                             self.mass_data_queue] if not data_queue.empty()]
            for data in data_list:
                user_socket.send(data.encode())
                print(data)

    def send_message_command(self):
        while True:
            if not self.command_queue.empty():
                command = self.command_queue.get()
                print(command)
                if command[0] in self.controller_clients:
                    self.controller_clients[command[0]].send(command.encode())

    def receive_message(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            self.process_message(data)

    def process_message(self, data):
        if data.startswith("CMD"):
            try:
                CommandInvoker.invoke(data, self.command_queue)
            except ValueError:
                print("Please enter a valid command")
        elif data.startswith("L"):  # data, DL1: angle; DL2: load cell
            self.level_data_queue.put(data)
        elif data.startswith("M"):
            self.mass_data_queue.put(data)
        elif data.startswith("G"):
            self.gyro_data_queue.put(data)

    def start_user(self, client_socket, admin=False):
        if admin:
            threading.Thread(target=self.send_message_command).start()
        threading.Thread(target=self.send_message_data, args=(client_socket,)).start()
        threading.Thread(target=self.receive_message, args=(client_socket,)).start()

    def start_controller(self, client_socket):
        threading.Thread(target=self.receive_message, args=(client_socket,)).start()

    def run(self, client_socket):
        try:
            while True:
                id_message = client_socket.recv(1024).decode()
                if id_message.startswith("ID"):
                    if ("admin" in id_message) and (not self.has_admin):
                        self.start_user(client_socket, admin=True)
                        # only one admin user is allowed
                        self.has_admin = True
                    elif "user" in id_message:
                        self.start_user(client_socket, admin=False)
                    elif "level" in id_message:
                        self.controller_clients["L"] = client_socket
                        self.start_controller(client_socket)
                    elif "mass" in id_message:
                        self.controller_clients["M"] = client_socket
                        self.start_controller(client_socket)
                    elif "gyro" in id_message:
                        self.controller_clients["G"] = client_socket
                        self.start_controller(client_socket)
                    break

        except socket.error:
            client_socket.close()
