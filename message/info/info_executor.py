from typing import List

from communication.client import ClientStatus
from message.command.command import LevelCommandType
from message.command.command_executor import LevellingCommandExecutor
from message.info.info import *


def update_ready_status() -> ClientStatus:
    return ClientStatus.READY


class MassInfoExecutor:

    @staticmethod
    def execute(info_type):
        output_dict = dict()
        output_info = None
        output_status = None
        output_command = None
        if info_type == MassInfoType.MOVE_DONE:
            output_info, output_command, output_status = MassInfoExecutor.move_finish()
        if info_type == MassInfoType.STOP_DONE:
            output_info, output_command, output_status = MassInfoExecutor.stop_finish()
        if info_type == MassInfoType.SET_DONE:
            output_info = MassInfoExecutor.set_pos_finish()
        if output_info is not None:
            output_dict["info"] = output_info
        if output_status is not None:
            output_dict['status'] = output_status
        if output_command is not None:
            output_dict['command'] = output_command
        return output_dict

    @staticmethod
    def set_pos_finish():
        return AdminInfoType.M_POS_DONE.value

    @staticmethod
    def move_finish() -> (str, List[LevelCommandType]):
        # change status, deactivate button, wait for LevelingDone command
        output_command = MassInfoExecutor.require_levelling()
        output_info = AdminInfoType.M_MOVE_DONE.value
        output_status = update_ready_status()
        return output_info, output_command, output_status

    @staticmethod
    def stop_finish() -> (str, List[LevelCommandType]):
        output_command = MassInfoExecutor.require_levelling()
        output_info = AdminInfoType.M_STOP_DONE.value
        output_status = update_ready_status()
        return output_info, output_command, output_status

    @staticmethod
    def require_levelling() -> List[LevelCommandType]:
        stop_command = LevellingCommandExecutor.execute(LevelCommandType.STOP)
        level_once = LevellingCommandExecutor.execute(LevelCommandType.LEVEL_ONCE)
        return [stop_command, level_once]


class LevelInfoExecutor:
    @staticmethod
    def execute(info_type, msg=None) -> dict:
        output_dict = dict()
        output_info = None
        output_status = None
        if info_type == LevelInfoType.LEVEL_DONE:
            output_info, output_status = LevelInfoExecutor.level_finish()
        if info_type == LevelInfoType.STOP_DONE:
            output_info, output_status = LevelInfoExecutor.stop_finish()
        if info_type == LevelInfoType.AUTO_MOVE_DONE:
            output_info, output_status = LevelInfoExecutor.auto_move_finish()
        if info_type == LevelInfoType.BATTERY:
            output_info = LevelInfoExecutor.show_battery(msg)
        if info_type == LevelInfoType.INIT_DONE:
            output_info, output_status = LevelInfoExecutor.init_finish()
        if output_info is not None:
            output_dict["info"] = output_info
        if output_status is not None:
            output_dict['status'] = output_status
        return output_dict

    @staticmethod
    def show_battery(msg: str):
        output_info = AdminInfoType.L_BATTERY.value + msg[-1]
        return output_info

    @staticmethod
    def level_finish():
        output_info = AdminInfoType.L_LEVEL_DONE.value
        output_status = update_ready_status()
        return output_info, output_status

    @staticmethod
    def stop_finish():
        output_info = AdminInfoType.L_STOP_DONE.value
        output_status = update_ready_status()
        return output_info, output_status

    @staticmethod
    def auto_move_finish():
        output_info = AdminInfoType.L_MOVE_DONE.value
        output_status = update_ready_status()
        return output_info, output_status

    @staticmethod
    def init_finish():
        output_info = AdminInfoType.L_INIT_DONE.value
        output_status = update_ready_status()
        return output_info, output_status


class GyroInfoExecutor:
    @staticmethod
    def execute(info_type: GyroInfoType) -> dict:
        output_dict = dict()
        output_info = None
        output_status = None
        if info_type == GyroInfoType.ZERO_DONE:
            output_info, output_status = GyroInfoExecutor.zero_finish()
        if info_type == GyroInfoType.STOP_DONE:
            output_info, output_status = GyroInfoExecutor.stop_finish()
        if info_type == GyroInfoType.AUTO_ON_DONE:
            output_info, output_status = GyroInfoExecutor.auto_on_finish()
        if info_type == GyroInfoType.AUTO_OFF_DONE:
            output_info, output_status = GyroInfoExecutor.auto_off_finish()
        if info_type == GyroInfoType.CENTER_DONE:
            output_info, output_status = GyroInfoExecutor.center_finish()
        if output_info is not None:
            output_dict["info"] = output_info
        if output_status is not None:
            output_dict['status'] = output_status
        return output_dict

    @staticmethod
    def zero_finish():
        output_info = AdminInfoType.G_ZERO_DONE.value
        output_status = update_ready_status()
        return output_info, output_status

    @staticmethod
    def stop_finish():
        output_info = AdminInfoType.G_STOP_DONE.value
        output_status = update_ready_status()
        return output_info, output_status

    @staticmethod
    def auto_on_finish():
        output_info = AdminInfoType.G_AUTO_ON_DONE.value
        output_status = update_ready_status()
        return output_info, output_status

    @staticmethod
    def auto_off_finish():
        output_info = AdminInfoType.G_AUTO_OFF_DONE.value
        output_status = update_ready_status()
        return output_info, output_status

    @staticmethod
    def center_finish():
        output_info = AdminInfoType.G_CENTER_DONE.value
        output_status = update_ready_status()
        return output_info, output_status
