from command.command_executor import *


class CommandInvoker:
    @staticmethod
    def invoke(message, command_queue):
        if message.startswith("CMDL"):
            LevellingCommandExecutor.execute(message, command_queue)
        elif message.startswith("CMDM"):
            MassCommandExecutor.execute(message, command_queue)
        elif message.startswith("CMDG"):
            GyroCommandExecutor.execute(message, command_queue)


