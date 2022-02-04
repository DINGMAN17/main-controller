import queue
import time

from communication.client import ClientStatus, Client
from control.task_list import Tasks, Task
from message.command.command_executor import *
from message.command.command_invoker import CommandInvoker
from message.info.info_invoker import InfoInvoker
from message.message import BaseMessageType
from utils import LogMessage


class BasicExecution:
    def __init__(self):
        self.admin = None
        self.users = []
        self.controller_clients = {}
        self.tasks_list = Tasks()
        self.data_queue = queue.Queue()
        self.info_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.status_queue = queue.Queue()
        self.system_command_queue = queue.Queue()
        self.admin_command_queue = queue.Queue()
        self.warning_queue = queue.Queue()
        self.emergency_queue = queue.Queue()

    def send_command_process(self):
        while self.admin.connected:
            self.send_command_from_queue(self.admin_command_queue)
            self.send_command_from_queue(self.system_command_queue)

    def send_command_from_queue(self, command_queue):
        recipient = None
        try:
            if not command_queue.empty():
                command = command_queue.get()
                recipient = self.check_recipient(command)
                if recipient is not None:
                    self.send_single_command(command, recipient)
                else:
                    self.admin.socket.sendall("ERR-intended client is not connected".encode())
        except (OSError, KeyError, SystemError):
            # TODO: check whether the recipient.set_disconnect() is correct
            self.handle_controller_disconnect(recipient)

    def check_recipient(self, command):
        recipient_type = command.recipient
        if recipient_type in self.controller_clients:
            recipient = self.controller_clients[recipient_type]
            if recipient.connected:
                return recipient
        return None

    def send_single_command(self, command: Command, recipient: Client):
        # think about if the status is different from the system indication
        if command.busy_command:
            self.acquire_status(recipient)
            error_count = 0
            while recipient.status != ClientStatus.READY:
                self.acquire_status(recipient)
                error_count += 1
                if error_count >= 10:
                    # TODO: handle warning!!
                    raise SystemError("There's a conflict in the status")
                time.sleep(2)
        recipient.socket.sendall(command.value.encode())
        command_type = command.command_type.name
        LogMessage.send_command(command)
        self.admin.socket.sendall(command_type.encode())
        # self.create_and_add_task(command)
        if command.busy_command:
            recipient.set_status(ClientStatus.BUSY)

    def acquire_status(self, recipient: Client):
        status_cmd = recipient.client_type.name[0] + "status\n"
        recipient.socket.sendall(status_cmd.encode())
        status_update = recipient.client_type.name + recipient.status.name
        self.admin.socket.sendall(status_update.encode())

    # def create_and_add_task(self, command: Command):
    #     new_task = Task(command)
    #     self.tasks_list.start_task(new_task)

    def send_message_data(self):
        while self.admin.connected:
            data_list = [data_queue.get() for data_queue in [self.info_queue] if not data_queue.empty()]
            for data in data_list:
                LogMessage.send_to_user(data)
                self.send_single_data(data)

    def send_single_data(self, data: str):
        for user in self.users:
            try:
                user.socket.sendall(data.encode())
            except OSError:
                self.handle_user_disconnection(user)

    def handle_controller_disconnect(self, recipient: Client):
        self.alert()
        recipient.set_disconnect()
        LogMessage.disconnect(recipient.client_type.name)

    def handle_user_disconnection(self, user: Client):
        if user.client_type != ClientType.ADMIN:
            self.users.remove(user)
            LogMessage.remove_user()
        else:
            self.admin.set_disconnect()
            LogMessage.disconnect(user.client_type.name)
            self.alert()

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
                self.handle_controller_disconnect(client)

    def receive_message(self, client: Client):
        while client.connected:
            try:
                message = client.socket.recv(1024).decode().strip()
                msg_list = message.split("\n")
                for msg in msg_list:
                    if len(msg) > 0:
                        self.process_general_message(msg, client.client_type)
            except OSError as e:
                self.handle_controller_disconnect(client)
            except Exception:
                LogMessage.bad_request()

    def process_general_message(self, message, client_type):
        if client_type == ClientType.ADMIN:
            admin_command_list = BasicExecution.process_admin_command(message)
            [self.admin_command_queue.put(cmd) for cmd in admin_command_list if cmd is not None]
        elif client_type in [ClientType.LEVEL, ClientType.MASS, ClientType.GYRO]:
            self.process_controller_message(message)

    @staticmethod
    def process_admin_command(message: str) -> list:
        # e.g. A-C-L-stop
        return CommandInvoker.invoke(message[2:])

    def process_controller_message(self, message: str):
        # e.g. M-INFO-moved
        try:
            message_components = message.split("-")
            msg_type = BaseMessageType(message_components[1])
            if msg_type == BaseMessageType.DATA:
                LogMessage.receive_data(message)
                self.data_queue.put(message)
            elif msg_type == BaseMessageType.INFO:
                self.process_info(message)
            elif msg_type == BaseMessageType.STATUS:
                self.update_status(message)
        except ValueError as e:
            print(e)

    def process_info(self, message):
        try:
            output_dict = InfoInvoker.invoke(message)
            output_info, output_command, output_status = (output_dict.get(key) for key in ["info", "command", "status"])
            if output_info is not None:
                self.info_queue.put(output_info)
            if output_command is not None:
                self.update_system_command(output_command)
            if output_status is not None:
                self.update_status(message, output_status)
        except AttributeError as e:
            self.info_queue.put(message)

    def update_status(self, message, status=None):
        # L-STATUS-ready
        msg_components = message.split("-")
        client_type = ClientType(msg_components[0])
        if status is None:
            status = ClientStatus(msg_components[-1])
        self.controller_clients[client_type].set_status(status)
        self.status_queue.put(message)
        send_message = client_type.name + "status changed to " + status.value
        self.admin.socket.sendall(send_message.encode())
        LogMessage.update_client_status(client_type, status)

    def update_system_command(self, output_command: list):
        for cmd in output_command:
            # TODO: how to find and update task status instead of creating a new task
            self.system_command_queue.put(cmd)

    def alert(self):
        # TODO: how to lock the system when critical condition occurs??
        print("warning!!!!!!")
