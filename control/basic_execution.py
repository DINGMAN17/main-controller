import queue
import threading
import time
from typing import Optional

from communication.client import ClientStatus, Client
from control.task_list import Tasks, Task, TaskStatus
from message.command.command_executor import *
from message.command.command_invoker import CommandInvoker
from message.info.info import BaseInfoType
from message.info.info_invoker import InfoInvoker
from message.message import BaseMessageType
from utils import LogMessage


class BasicExecution:
    def __init__(self):
        self.admin = None
        self.users = []
        self.controller_clients = {}
        self.tasks_list = Tasks()
        self.e_stop = False
        self.lock = threading.Lock()
        self.data_queue = queue.Queue()
        self.info_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.status_queue = queue.Queue()
        self.system_command_queue = queue.Queue()
        self.admin_command_queue = queue.Queue()
        self.warning_queue = queue.Queue()
        self.emergency_queue = queue.Queue()
        self.info_controller = InfoInvoker()

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
                    err_msg = LogMessage.command_sent_fail()
                    self.admin.socket.sendall(err_msg.encode())
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
        if command.busy_command:
            self.ensure_client_availability(recipient)
        recipient.socket.sendall(command.value.encode())
        LogMessage.send_command(command)
        if command.busy_command:
            recipient.status = ClientStatus.BUSY
            self.tasks_list.start_task(command)

    def ensure_client_availability(self, recipient):
        # TODO: think about if the status is different from the system indication
        self.acquire_status(recipient)
        error_count = 0
        while recipient.status != ClientStatus.READY:
            self.acquire_status(recipient)
            error_count += 1
            if error_count >= 10:
                # TODO: handle warning!!
                raise SystemError("There's a conflict in the status")
            time.sleep(10)

    def acquire_status(self, recipient: Client):
        status_cmd = recipient.client_type.name[0] + "status\n"
        recipient.socket.sendall(status_cmd.encode())
        status_update = recipient.client_type.name + recipient.status.name
        self.admin.socket.sendall(status_update.encode())

    def send_message(self):
        while self.admin.connected:
            data_list = [msg_queue.get() for msg_queue in [self.info_queue, self.status_queue] if
                         not msg_queue.empty()]

            for data in data_list:
                LogMessage.send_to_user(data)
                self.send_single_data(data)

    def send_data(self):
        while self.admin.connected:
            if not self.data_queue.empty():
                data = self.data_queue.get() + "\n"
                self.send_single_data(data)
                LogMessage.receive_data(data)

    def send_single_data(self, data: str):
        for user in self.users:
            try:
                user.socket.sendall(data.encode())
            except OSError:
                self.handle_user_disconnection(user)

    def handle_controller_disconnect(self, recipient: Client):
        self.alert()
        with self.lock:
            recipient.connected = False
        LogMessage.disconnect(recipient.client_type.name)

    def handle_user_disconnection(self, user: Client):
        with self.lock:
            if user.client_type != ClientType.ADMIN:
                self.users.remove(user)
                LogMessage.remove_user()
            else:
                self.admin.connected = False
                LogMessage.disconnect(user.client_type.name)
                self.alert()

    def request_data(self, client, interval=1):
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
            admin_command_list = self.process_admin_command(message)
            [self.admin_command_queue.put(cmd) for cmd in admin_command_list if cmd is not None]
        elif client_type in [ClientType.LEVEL, ClientType.MASS, ClientType.GYRO]:
            self.process_controller_message(message)

    def process_admin_command(self, message: str) -> List[Command]:
        # e.g. A-C-L-stop
        command, admin_command_list = CommandInvoker.invoke(message[2:])
        self.tasks_list.current_integrated_command = command
        return admin_command_list

    def process_controller_message(self, message: str):
        # e.g. M-INFO-moved
        try:
            message_components = message.split("-")
            print(message_components)
            msg_type = BaseMessageType(message_components[1])
            if msg_type == BaseMessageType.DATA:
                self.data_queue.put(message)
            elif msg_type == BaseMessageType.INFO:
                print(message)
                self.process_info(message_components)
            elif msg_type == BaseMessageType.STATUS:
                self.update_status(message_components)
        except ValueError as e:
            print(e)

    def process_info(self, msg_components: list):
        try:
            self.info_controller.msg_components = msg_components
            self.info_controller.integrated_command = self.tasks_list.current_integrated_command
            output_dict = self.info_controller.invoke()
            self.tasks_list.current_integrated_command = self.info_controller.integrated_command
            output_info, output_command, output_status = (output_dict.get(key) for key in ["info", "command", "status"])
            if output_info is not None:
                # self.update_on_going_task(output_info)
                self.info_queue.put(output_info.value)
            if output_command is not None:
                self.update_system_command(output_command)
            if output_status is not None:
                self.update_status(status_update_info=output_status)
        except (AttributeError, ValueError) as e:
            info_not_classified = "-".join(msg_components) + "\n"
            self.info_queue.put(info_not_classified)

    def update_on_going_task(self, info_type: BaseInfoType):
        info_name = info_type.name
        if "DONE" in info_name:
            self.tasks_list.finish_task(ClientType(info_name[0]))

    def update_status(self, msg_components: list = None,
                      status_update_info: Optional[List[Tuple[ClientType, ClientStatus]]] = None):
        # L-STATUS-ready
        if status_update_info is None:
            client_type = ClientType(msg_components[0])
            status_str = msg_components[-1].strip().lower()
            status = ClientStatus(status_str)
            self.controller_clients[client_type].status = status
            self.status_queue.put("-".join(msg_components))
            LogMessage.update_client_status(client_type, status)
        else:
            for status_item in status_update_info:
                client_type, status = status_item
                self.controller_clients[client_type].status = status
                LogMessage.update_client_status(client_type, status)

    def update_system_command(self, output_command: list):
        for cmd in output_command:
            self.system_command_queue.put(cmd)
            future_task = Task(cmd, TaskStatus.WAIT)
            self.tasks_list.add_future_task(future_task)

    def alert(self):
        # TODO: how to lock the system when critical condition occurs??
        print("warning!!!!!!")

    def activate_E_stop(self):
        # TODO: how to clear all the future tasks, differentiate moving mass stop and E-stop
        # with self.admin_command_queue.mutex:
        #     self.admin_command_queue.queue.clear()
        with self.lock:
            self.e_stop = True
        self.tasks_list.clear_future_tasks()
