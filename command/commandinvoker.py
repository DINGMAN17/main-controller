import logging

from command.command_executor import *
from communication.message import *


class CommandInvoker:
    @staticmethod
    def invoke(message, command_queue):
        # sample message: CL-init, C:command; L:levelling
        try:
            msg_components = message.split("-", 2)
            command_type = CommandInvoker.get_command_type(msg_components[0])
            if command_type == MessageType.LEVEL_COMMAND:
                command = CommandInvoker.get_level_command(msg_components[1])
                LevellingCommandExecutor.execute(command, msg_components, command_queue)
            elif command_type == MessageType.MASS_COMMAND:
                command = CommandInvoker.get_mass_command(msg_components[1])
                MassCommandExecutor.execute(command, msg_components, command_queue)
            elif command_type == MessageType.GYRO_COMMAND:
                command = CommandInvoker.get_gyro_command(msg_components[1])
                GyroCommandExecutor.execute(command, command_queue)
        except (ValueError, IndexError) as e:
            logging.exception("wrong command %s", message)

    @staticmethod
    def get_command_type(command_type):
        return MessageType(command_type.upper())

    @staticmethod
    def get_level_command(command):
        return LevelCommandType(command)

    @staticmethod
    def get_mass_command(command):
        return MassCommandType(command)

    @staticmethod
    def get_gyro_command(command):
        return GyroCommandType(command)
