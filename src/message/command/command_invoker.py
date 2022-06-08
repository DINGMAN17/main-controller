from typing import Optional, List

from src.message.command.command import LevelCommandType, MassCommandType, GyroCommandType, \
    IntegrationCommandType
from src.message.command.command_executor import Command, LevellingCommandExecutor, MassCommandExecutor, \
    GyroCommandExecutor, IntegrationCommandExecutor, BaseCommandExecutor
from src.message.exceptions.command_exception import InvalidCommandTypeException
from src.message.message import MessageRecipientType


class CommandInvoker:
    def __init__(self):
        self.level_command_executor = LevellingCommandExecutor()
        self.mass_command_executor = MassCommandExecutor()
        self.gyro_command_executor = GyroCommandExecutor()
        self.integrated_command_executor = IntegrationCommandExecutor()
        self._msg_components: Optional[list] = None
        self._recipient_type: Optional[MessageRecipientType] = None
        self._integrated_command_type: Optional[IntegrationCommandType] = None
        self.commands_to_send: Optional[List[Command]] = None
        self.command_type = None

    @property
    def msg_components(self):
        return self._msg_components

    @msg_components.setter
    def msg_components(self, message: str):
        self._msg_components = message.split("-")

    @property
    def integrated_command_type(self):
        return self._integrated_command_type

    @integrated_command_type.setter
    def integrated_command_type(self, integrated_command: Command):
        self._integrated_command_type = integrated_command

    def invoke(self):
        # sample message: A-C-L-init, C:command; L:levelling
        try:
            self._recipient_type = MessageRecipientType(self.msg_components[2])
            if self._recipient_type == MessageRecipientType.LEVEL:
                self.level_command_executor.command_value = self.msg_components[-1]
                self.process_command(self.level_command_executor)
            elif self._recipient_type == MessageRecipientType.MASS:
                self.mass_command_executor.command_value = self.msg_components[-1]
                self.process_command(self.mass_command_executor)
            elif self._recipient_type == MessageRecipientType.GYRO:
                self.process_command(self.gyro_command_executor)
            elif self._recipient_type == MessageRecipientType.MULTIPLE:
                self.process_command(self.integrated_command_executor)
        except (ValueError, IndexError) as e:
            # LogMessage.wrong_command(self.msg_components)
            pass

    def process_command(self, executor: BaseCommandExecutor):
        self.get_command_type()
        executor.command_type = self.command_type
        executor.execute()
        self.commands_to_send = executor.command_to_send

    def get_command_type(self):
        try:
            if self._recipient_type == MessageRecipientType.LEVEL:
                self.command_type = LevelCommandType(self.msg_components[3])
            elif self._recipient_type == MessageRecipientType.GYRO:
                self.command_type = GyroCommandType(self.msg_components[3])
            elif self._recipient_type == MessageRecipientType.MASS:
                self.command_type = MassCommandType(self.msg_components[3])
            elif self._recipient_type == MessageRecipientType.MULTIPLE:
                self.command_type = IntegrationCommandType(self.msg_components[3])
        except ValueError as e:
            raise InvalidCommandTypeException()
