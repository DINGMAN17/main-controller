from message.command.command_executor import LevellingCommandExecutor
from message.info.info import MassInfoType


class BaseInfoExecutor:
    pass


class MassInfoExecutor:

    @staticmethod
    def execute(info_type):
        output_info = None
        output_command = None
        if info_type == MassInfoType.MOVE_DONE:
            output_command = LevellingCommandExecutor.level_once()
            output_info = "M-INFO-moving mass operation done"
        if info_type == MassInfoType.STOP_DONE:
            output_command = LevellingCommandExecutor.level_once()
            output_info = "M-INFO-moving mass stopped"
        return output_info, output_command
