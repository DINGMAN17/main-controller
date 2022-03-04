from typing import Tuple

from message.command.command_executor import *
from message.command.command_executor import Command
from message.message import MessageRecipientType
from utils import LogMessage


class CommandInvoker:
    @staticmethod
    def invoke(message: str) -> Tuple[BaseCommandType, List[Command]]:
        # sample message: L-C-init, C:command; L:levelling
        try:
            command = None
            commands_to_send = []
            msg_components = message.split("-")
            recipient_type = MessageRecipientType(msg_components[1])
            if recipient_type == MessageRecipientType.LEVEL:
                command = CommandInvoker.get_level_command(msg_components[2])
                command_to_send = LevellingCommandExecutor.execute(command, msg_components)
                commands_to_send.append(command_to_send)
            elif recipient_type == MessageRecipientType.MASS:
                command = CommandInvoker.get_mass_command(msg_components[2])
                command_to_send = MassCommandExecutor.execute(command, msg_components)
                commands_to_send.append(command_to_send)
            elif recipient_type == MessageRecipientType.GYRO:
                command = CommandInvoker.get_gyro_command(msg_components[2])
                command_to_send = GyroCommandExecutor.execute(command)
                commands_to_send.append(command_to_send)
            elif recipient_type == MessageRecipientType.MULTIPLE:
                command = CommandInvoker.get_integration_command(msg_components[2])
                command_to_send = IntegrationCommandExecutor.execute(command)
                commands_to_send.extend(command_to_send)
            return command, commands_to_send
        except (ValueError, IndexError) as e:
            LogMessage.wrong_command(message)

    @staticmethod
    def get_level_command(command: str):
        return LevelCommandType(command)

    @staticmethod
    def get_mass_command(command):
        return MassCommandType(command)

    @staticmethod
    def get_gyro_command(command):
        return GyroCommandType(command)

    @staticmethod
    def get_integration_command(command):
        return IntegrationCommandType(command)
