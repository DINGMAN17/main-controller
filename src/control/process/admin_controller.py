import threading
from typing import Optional, List

from src.communication.client import Client, ClientStatus
from src.control.exceptions.operation_exceptions import ClientDisconnectException, AdminDisconnectException
from src.control.execution.command_processor import CommandProcessor

from src.utils.logging import LogMessage


class AdminController:
    """
    This class keeps track of the admin status and deals with all the operations related to admin.

    Main operations involved:
    1. receive commands from admin
    2. send updates & data to admin
    """

    def __init__(self, admin: Client, cmd_processor: CommandProcessor):
        self.admin: Client = admin
        self.cmd_processor: CommandProcessor = cmd_processor

    def activate(self):
        try:
            threading.Thread(target=self.receive_command_loop).start()
        except ClientDisconnectException:
            self.report_admin_error()
            raise AdminDisconnectException

    def send_update_to_admin(self, update: str):
        self.admin.tcp_service.send_message(update)

    def receive_command_loop(self):
        while self.admin.connected:
            recv_cmd_list = self.receive_command()
            self.cmd_processor.add_new_unprocessed_command_list(recv_cmd_list)

    def receive_command(self) -> List[Optional[str]]:
        recv_cmd_list = self.admin.tcp_service.receive_message()
        LogMessage.receive_command(recv_cmd_list)
        return recv_cmd_list

    def report_admin_error(self):
        self.admin.status = ClientStatus.ERROR
