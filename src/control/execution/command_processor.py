from queue import Queue
from typing import List, Optional

from src.control.exceptions.process_execptions import SendCommandStatusCheckFailException
from src.control.operation.system_all import IntegratedStatusController
from src.message.command.command_executor import Command
from src.message.command.command_invoker import CommandInvoker
from src.message.exceptions.command_exception import InvalidCommandTypeException


class CommandProcessor:
    """
    Process and verify the commands received from the admin, i.e. operator's app

    Process the raw text message to Command object. Based on the specific command, verify:
    Two types of checks:
    - Integrated system status check
    - Individual sub system status check
    """

    def __init__(self, status_controller: IntegratedStatusController):
        self.status_controller = status_controller
        self.command_invoker = CommandInvoker()
        self.unprocessed_cmd_from_admin_queue = Queue.queue()
        self.processed_cmd_queue = Queue.queue()
        self._current_processing_cmd: Optional[str] = None
 
    def add_new_unprocessed_command_list(self, recv_cmd: List[str]):
        self.unprocessed_cmd_from_admin_queue.put(recv_cmd)

    def get_unprocessed_cmd(self):
        return self.unprocessed_cmd_from_admin_queue.get()

    def add_processed_cmd_for_sending(self, processed_cmd: Command):
        return self.processed_cmd_queue.put(processed_cmd)

    def get_processed_cmd(self) -> Command:
        return self.processed_cmd_queue.get()

    def process_commands_list(self):
        unprocessed_cmd_list = self.get_unprocessed_cmd()
        [self.process_single_raw_command_from_admin(cmd) for cmd in unprocessed_cmd_list]

    def process_single_raw_command_from_admin(self, unprocessed_cmd: str):
        self._current_processing_cmd = unprocessed_cmd
        commands_to_send = self.get_system_command_list()
        try:
            self.verify_commands(commands_to_send)
        except SendCommandStatusCheckFailException:
            pass

    def get_system_command_list(self) -> List[Command]:
        # TODO: how to handle the command related error (rarely occur)
        try:
            self.command_invoker.msg_components = self._current_processing_cmd
            self.command_invoker.invoke()
            return self.command_invoker.commands_to_send
        except InvalidCommandTypeException:
            pass
        except SendCommandStatusCheckFailException:
            pass

    def verify_commands(self, commands_to_send: List[Command]):
        """
        verify the command before sending it out
        steps:
        1. check system status if required
        2. check sub system status if required
        is any of the checks fails, raise error
        """
        for cmd in commands_to_send:
            is_check_ok = self.verify_single_command(cmd)
            if not is_check_ok:
                raise SendCommandStatusCheckFailException()

    def verify_single_command(self, cmd: Command):
        required_system_status = cmd.system_status_required
        required_subsystem_status = cmd.clientStatus_required
        if required_system_status is None and required_subsystem_status is None:
            return True

        is_system_check_ok = (
                required_system_status is None
                or self.status_controller.check_system_status(required_system_status)
        )

        is_subsystem_status_ok = (
                required_subsystem_status is None
                or self.status_controller.check_subsystem_status(cmd.recipient, required_subsystem_status)
        )
        return is_system_check_ok and is_subsystem_status_ok
