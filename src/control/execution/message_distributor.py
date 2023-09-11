from typing import Optional

from src.control.execution.command_processor import CommandProcessor
from src.control.process.admin_controller import AdminController
from src.control.process.subsystem_controller import SubsystemController


class MessageDistributor:
    """
    Distribute messages to different clients and update the status based on the messages sent

    Two types of messages:
    - Commands to sub-controllers
    - Updates to admin
    """

    def __init__(self):
        self.command_processor: Optional[CommandProcessor] = None
        self.admin_controller = None
        self.subsystem_controller = None

    def set_admin_controller(self, admin_controller: AdminController):
        self.admin_controller = admin_controller

    def set_subsystem_controller(self, subsystem_controller: SubsystemController):
        self.subsystem_controller = subsystem_controller

    def set_command_processor(self, command_processor: CommandProcessor):
        self.command_processor = command_processor

