import queue
import threading
from typing import Optional, List

from src.communication.client import Client, ClientType
from src.control.exceptions.network_exceptions import ClientDisconnectException
from src.control.exceptions.process_execptions import SendCommandStatusCheckFailException, \
    IntendedClientDoesNotExistException

from src.control.process.status_controller import StatusController
from src.message.command.command import IntegrationCommandType, BaseCommandType
from src.message.command.command_executor import Command
from src.message.command.command_invoker import CommandInvoker
from src.message.error.error import NetworkErrorType
from src.message.exceptions.command_exception import InvalidCommandTypeException
from src.utils.logging import LogMessage


class AdminController:
    #TODO: handle admin when admin disconnect and reconnect
    def __init__(self, status_controller: StatusController):
        self.status_controller: StatusController = status_controller
        self.command_invoker: CommandInvoker = CommandInvoker()
        self._admin_command_queue: queue = queue.Queue()
        self._latest_sent_command: Optional[Command] = None
        self._latest_input_command_type: Optional[BaseCommandType] = None

    @property
    def latest_input_command_type(self):
        return self._latest_input_command_type

    @latest_input_command_type.setter
    def latest_input_command_type(self, input_command):
        self._latest_input_command_type = input_command

    @property
    def admin_command_queue(self):
        return self._admin_command_queue

    def send_update_to_users(self, update_list: list):
        for user in self.status_controller.users:
            try:
                [user.tcp_service.send_message(update) for update in update_list]
            except ClientDisconnectException:
                pass

    def add_admin_or_user(self, client: Client):
        if client.client_type == ClientType.ADMIN:
            # only one admin user is allowed
            self.status_controller.admin = client
        self.status_controller.add_user(client)

    def get_admin_connection_state(self) -> bool:
        return self.status_controller.get_admin_connection_state()

    def activate(self):
        threading.Thread(target=self.send_command_loop).start()
        threading.Thread(target=self.receive_command_loop).start()

    def receive_command_loop(self):
        while self.get_admin_connection_state():
            try:
                self.receive_and_process_command()
            except ClientDisconnectException:
                print('admin diconnected')
                self.handle_admin_disconnect()
                break

    def receive_and_process_command(self):
        valid_msg_list = self.receive_command()
        [self.process_command(msg) for msg in valid_msg_list]

    def receive_command(self) -> List[Optional[str]]:
        valid_msg_list = self.status_controller.admin.tcp_service.receive_message()
        LogMessage.receive_command(valid_msg_list)
        return valid_msg_list

    def process_command(self, msg):
        # e.g. A-C-L-stop
        try:
            self.command_invoker.msg_components = msg
            self.command_invoker.invoke()
            commands_list = self.command_invoker.commands_to_send
            self._latest_input_command_type = self.command_invoker.command_type
            self.add_and_verify_command_to_queue(commands_list)
        except InvalidCommandTypeException:
            pass
        except SendCommandStatusCheckFailException:
            pass

    def add_and_verify_command_to_queue(self, commands_list: List[Command]):
        for cmd in commands_list:
            if not self.verify_recipient_status(cmd):
                raise SendCommandStatusCheckFailException()
        [self.add_command_to_queue(cmd) for cmd in commands_list if self.verify_recipient_status(cmd)]

    def send_command_loop(self):
        while self.get_admin_connection_state():
            try:
                self.send_command_and_update()
            except ClientDisconnectException:
                print("AdminDisconnectException")
                self.handle_admin_disconnect()
                break

    def send_command_and_update(self):
        command = self.get_command_from_queue()
        if command is not None:
            try:
                recipient = self.status_controller.get_subsystem_client(command.recipient)
                self.send_command(recipient, command)
                self._latest_sent_command = command
                self.update_after_sending_command()
            except IntendedClientDoesNotExistException:
                pass

    def send_command(self, recipient, command):
        try:
            recipient.tcp_service.send_message(command.value)
            LogMessage.send_command(command)
        except ClientDisconnectException:
            print(recipient.name, " is not connected")

    def verify_recipient_status(self, command: Command) -> bool:
        if command.busy_command:
            recipient_status_check = self.status_controller.check_recipient_status_for_busy_command(command.recipient)
            return recipient_status_check
        return True

    def get_command_from_queue(self) -> Optional[Command]:
        if not self.admin_command_queue.empty():
            return self.admin_command_queue.get()
        return None

    def add_command_to_queue(self, command: Command):
        self.admin_command_queue.put(command)

    def update_after_sending_command(self):
        try:
            # update the status of sub controller
            self.status_controller.update_recipient_status_after_sending_command(self._latest_sent_command)
            # update if the command is integrated command
            self.update_integrated_command()
        except ClientDisconnectException:
            print("AdminDisconnectException")
            self.handle_admin_disconnect()

    def update_integrated_command(self):
        if self._latest_input_command_type.name in IntegrationCommandType.__members__:
            self.status_controller.current_integrated_command = self._latest_input_command_type

    def handle_admin_disconnect(self):
        self.status_controller.system_error = NetworkErrorType.ADMIN_DISCONNECT
        self.restore_safe_mode()

    def restore_safe_mode(self):
        stop_command_list = CommandInvoker.activate_Estop()
        self.admin_command_queue.queue.clear()
        [self.add_command_to_queue(cmd) for cmd in stop_command_list if
         self.status_controller.check_recipient_status_for_safe_mode(cmd.recipient)]

