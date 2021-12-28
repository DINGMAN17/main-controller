import queue
import threading
from command.commandinvoker import CommandInvoker


class ClientHandler:
    def __init__(self):
        self.level_command_queue = queue.Queue()
        self.level_data_queue = queue.Queue()
        self.command_invoker = CommandInvoker()

    def send_message(self, client_socket, data_queue):
        while True:
            if not data_queue.empty():
                data = data_queue.get()
                print(data)
                client_socket.send(data.encode())

    def receive_message(self, client_socket, data_queue):
        while True:
            data = client_socket.recv(1024).decode()
            self.process_message(data, data_queue)

    def process_message(self, data, data_queue):
        if data.startswith("cmd"):
            self.command_invoker.execute(data, data_queue)
        elif data.startswith("Debug"):
            data_queue.put(data)
        elif data.startswith("D"):  # data, DL1: angle; DL2: load cell
            data_queue.put(data)

    def start_user(self, client_socket):
        threading.Thread(target=self.send_message, args=(client_socket, self.level_command_queue,)).start()
        threading.Thread(target=self.receive_message, args=(client_socket, self.level_data_queue,)).start()

    def start_levelling(self, client_socket):
        threading.Thread(target=self.send_message, args=(client_socket, self.level_data_queue,)).start()
        threading.Thread(target=self.receive_message, args=(client_socket, self.level_command_queue,)).start()

    def run(self, socket):
        try:
            while True:
                data = socket.recv(1024).decode()
                if data.startswith("ID"):
                    if "levelling" in data:
                        self.start_levelling(socket)
                    if "user" in data:
                        self.start_user(socket)
                    break
        except socket.error:
            socket.close()


