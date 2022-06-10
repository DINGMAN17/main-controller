import queue
import threading
from typing import Optional

from src.communication.client import Client, ClientType
from src.control.exceptions.process_execptions import SendCommandStatusCheckFailException, AdminDisconnectException, \
    ClientDisconnectException

from src.control.process.status_controller import StatusController
from src.message.command.command import IntegrationCommandType
from src.message.command.command_executor import Command
from src.message.command.command_invoker import CommandInvoker
from src.utils.logging import LogMessage


class AdminController:
    def __init__(self, status_controller: StatusController):
        self.status_controller = status_controller
        self.command_invoker = CommandInvoker()
        self._admin_command_queue = queue.Queue()
        self._latest_command = None
        self._latest_integrated_command_type = None

    @property
    def latest_command(self):
        return self._latest_command

    @latest_command.setter
    def latest_command(self, command):
        self._latest_command = command

    @property
    def admin_command_queue(self):
        return self._admin_command_queue

    def add_admin_or_user(self, client: Client):
        if client.client_type == ClientType.ADMIN:
            # only one admin user is allowed
            self.status_controller.admin = client
        self.status_controller.add_user(client)

    def get_admin_connection_state(self):
        return self.status_controller.get_admin_connection_state()

    def activate(self):
        threading.Thread(target=self.send_command_loop).start()
        threading.Thread(target=self.receive_command_loop).start()

    def receive_command_loop(self):
        while self.get_admin_connection_state():
            try:
                self.receive_and_process_command()
            except ClientDisconnectException:
                print('subsystem diconnected')

    def receive_and_process_command(self):
        valid_msg_list = self.receive_command()
        [self.process_command(msg) for msg in valid_msg_list]

    def receive_command(self):
        valid_msg_list = self.status_controller.admin.tcp_service.receive_message()
        LogMessage.receive_command(valid_msg_list)
        return valid_msg_list

    def process_command(self, msg):
        # e.g. A-C-L-stop
        self.command_invoker.msg_components = msg
        self.command_invoker.invoke()
        commands_list = self.command_invoker.commands_to_send
        self._latest_integrated_command_type = self.command_invoker.command_type
        [self.add_command_to_queue(cmd) for cmd in commands_list if cmd is not None]

    def send_command_loop(self):
        while self.get_admin_connection_state():
            try:
                self.send_and_verify_command()
            except SendCommandStatusCheckFailException as e:
                err_msg = LogMessage.command_sent_fail()
                print(err_msg)
            except ClientDisconnectException:
                print("AdminDisconnectException")

    def send_and_verify_command(self):
        command = self.get_command_from_queue()
        if command is not None:
            if not self.verify_before_sending(command):
                raise SendCommandStatusCheckFailException()
            recipient = self.status_controller.get_subsystem_client(command.recipient)
            self.send_command(recipient, command)
            self._latest_command = command
            self.update_after_sending_command()

    def send_command(self, recipient, command):
        recipient.tcp_service.send_message(command.value)
        LogMessage.send_command(command)

    def verify_before_sending(self, command: Command):
        if command.busy_command:
            recipient_status_check = self.status_controller.check_recipient_status_for_busy_command(command.recipient)
            return recipient_status_check
        return True

    def get_command_from_queue(self) -> Optional[Command]:
        if not self.admin_command_queue.empty():
            return self.admin_command_queue.get()
        return None

    def add_command_to_queue(self, command):
        self.admin_command_queue.put(command)

    def update_after_sending_command(self):
        try:
            # update the status of sub controller
            self.status_controller.update_recipient_status_after_sending_command(self.latest_command)
            # update if the command is integrated command
            self.update_integrated_command()
        except AdminDisconnectException:
            print("AdminDisconnectException")

    def update_integrated_command(self):
        if self._latest_integrated_command_type.name in IntegrationCommandType.__members__:
            self.status_controller.current_integrated_command = self._latest_integrated_command_type

