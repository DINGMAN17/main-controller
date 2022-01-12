import logging

from communication.client import ClientType
from message.command.command_executor import *
from message.message import *


class CommandInvoker:
    @staticmethod
    def invoke(message):
        # sample message: C-L-init, C:command; L:levelling
        try:
            command_to_send = None
            msg_components = message.split("-")
            command_type = ClientType(msg_components[1])
            if command_type == ClientType.LEVEL:
                command = CommandInvoker.get_level_command(msg_components[2])
                command_to_send = LevellingCommandExecutor.execute(command, msg_components)
            elif command_type == ClientType.MASS:
                command = CommandInvoker.get_mass_command(msg_components[2])
                command_to_send = MassCommandExecutor.execute(command, msg_components)
            elif command_type == ClientType.GYRO:
                command = CommandInvoker.get_gyro_command(msg_components[2])
                command_to_send = GyroCommandExecutor.execute(command)
            return command_to_send
        except (ValueError, IndexError) as e:
            logging.exception("wrong command %s", message)

    @staticmethod
    def get_level_command(command):
        return LevelCommandType(command)

    @staticmethod
    def get_mass_command(command):
        return MassCommandType(command)

    @staticmethod
    def get_gyro_command(command):
        return GyroCommandType(command)


if __name__ == "__main__":
    msg = CommandInvoker.invoke("C-L-step-10035001000035000400")
    print(msg)