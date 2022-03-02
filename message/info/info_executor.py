from typing import List, Tuple, Optional

from communication.client import ClientStatus, ClientType
from message.command.command import LevelCommandType, IntegrationCommandType
from message.command.command_executor import LevellingCommandExecutor
from message.info.info import MassInfoType, AdminInfoType, LevelInfoType, GyroInfoType, BaseInfoType


def update_ready_status(client: ClientType) -> Tuple[ClientType, ClientStatus]:
    return client, ClientStatus.READY


class MassInfoExecutor:

    @staticmethod
    def execute(info_type):
        output_dict = dict()
        output_info: Optional[BaseInfoType] = None
        output_status: Optional[List[Tuple[ClientType, ClientStatus]]] = None
        if info_type == MassInfoType.MOVE_DONE:
            output_info, output_status = MassInfoExecutor.move_finish()
        if info_type == MassInfoType.STOP_DONE:
            output_info, output_status = MassInfoExecutor.stop_finish()
        if info_type == MassInfoType.SET_DONE:
            output_info = MassInfoExecutor.set_pos_finish()
        if output_info is not None:
            output_dict["info"] = output_info
        if output_status is not None:
            output_dict['status'] = output_status
        return output_dict

    @staticmethod
    def set_pos_finish():
        return AdminInfoType.M_POS_DONE

    @staticmethod
    def move_finish() -> (str, List[Tuple[ClientType, ClientStatus]]):
        output_info = AdminInfoType.M_MOVE_DONE
        output_status = update_ready_status(ClientType.MASS)
        return output_info, [output_status]

    @staticmethod
    def stop_finish() -> (str, List[Tuple[ClientType, ClientStatus]]):
        output_info = AdminInfoType.M_STOP_DONE
        output_status = update_ready_status(ClientType.MASS)
        return output_info, [output_status]


class LevelInfoExecutor:
    @staticmethod
    def execute(info_type) -> dict:
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
            output_info = LevelInfoExecutor.show_battery()
        if info_type == LevelInfoType.INIT_DONE:
            output_info, output_status = LevelInfoExecutor.init_finish()
        if output_info is not None:
            output_dict["info"] = output_info
        if output_status is not None:
            output_dict['status'] = output_status
        return output_dict

    @staticmethod
    def show_battery():
        output_info = AdminInfoType.L_BATTERY
        return output_info

    @staticmethod
    def level_finish():
        output_info = AdminInfoType.L_LEVEL_DONE
        output_status = update_ready_status(ClientType.LEVEL)
        return output_info, [output_status]

    @staticmethod
    def stop_finish():
        output_info = AdminInfoType.L_STOP_DONE
        output_status = update_ready_status(ClientType.LEVEL)
        return output_info, [output_status]

    @staticmethod
    def auto_move_finish():
        output_info = AdminInfoType.L_MOVE_DONE
        output_status = update_ready_status(ClientType.LEVEL)
        return output_info, [output_status]

    @staticmethod
    def init_finish():
        output_info = AdminInfoType.L_INIT_DONE
        output_status = update_ready_status(ClientType.LEVEL)
        return output_info, [output_status]


class GyroInfoExecutor:
    @staticmethod
    def execute(info_type: BaseInfoType) -> dict:
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
        output_info = AdminInfoType.G_ZERO_DONE
        output_status = update_ready_status(ClientType.GYRO)
        return output_info, [output_status]

    @staticmethod
    def stop_finish():
        output_info = AdminInfoType.G_STOP_DONE
        output_status = update_ready_status(ClientType.GYRO)
        return output_info, [output_status]

    @staticmethod
    def auto_on_finish():
        output_info = AdminInfoType.G_AUTO_ON_DONE
        output_status = update_ready_status(ClientType.GYRO)
        return output_info, [output_status]

    @staticmethod
    def auto_off_finish():
        output_info = AdminInfoType.G_AUTO_OFF_DONE
        output_status = update_ready_status(ClientType.GYRO)
        return output_info, [output_status]

    @staticmethod
    def center_finish():
        output_info = AdminInfoType.G_CENTER_DONE
        output_status = update_ready_status(ClientType.GYRO)
        return output_info, [output_status]


class IntegratedInfoExecutor:

    @staticmethod
    def execute(info_type: BaseInfoType, integrated_command: IntegrationCommandType):
        output_dict = dict()
        output_info = output_status = output_command = None
        if integrated_command == IntegrationCommandType.MOVE_LEVEL:
            output_info, output_command, output_status = IntegratedInfoExecutor.MassMoveInfo.execute(info_type)
        if output_info is not None:
            output_dict["info"] = output_info
        if output_status is not None:
            if not isinstance(output_status, list):
                output_status = [output_status]
            output_dict['status'] = output_status
        if output_command is not None:
            if not isinstance(output_command, list):
                output_command = [output_command]
            output_dict['command'] = output_command
        return output_dict

    class MassMoveInfo:

        @staticmethod
        def execute(info_type: BaseInfoType):
            output_info = output_command = output_status = None
            if info_type == MassInfoType.MOVE_DONE:
                output_info, output_command = IntegratedInfoExecutor.MassMoveInfo.move_finish()
            elif info_type == MassInfoType.STOP_DONE:
                output_info, output_command = IntegratedInfoExecutor.MassMoveInfo.stop_finish()
            elif info_type == LevelInfoType.STOP_DONE:
                output_info, output_command, output_status = IntegratedInfoExecutor.MassMoveInfo.keep_level_stop_finish()
            elif info_type == LevelInfoType.LEVEL_DONE:
                output_info, output_status = IntegratedInfoExecutor.MassMoveInfo.level_once_finish()
            return output_info, output_command, output_status

        @staticmethod
        def move_finish() -> (str, LevelCommandType):
            # change status, deactivate button, wait for LevelingDone command
            output_command = IntegratedInfoExecutor.MassMoveInfo.stop_keep_level()
            output_info = AdminInfoType.I_MASS_MOVE_DONE
            return output_info, output_command

        @staticmethod
        def stop_finish() -> (str, LevelCommandType):
            output_command = IntegratedInfoExecutor.MassMoveInfo.stop_keep_level()
            output_info = AdminInfoType.I_MASS_STOP_DONE
            return output_info, output_command

        @staticmethod
        def keep_level_stop_finish() -> (str, LevelCommandType):
            output_command = IntegratedInfoExecutor.MassMoveInfo.start_level_once()
            output_info = AdminInfoType.I_KEEP_LEVEL_STOP_DONE
            output_status_level = update_ready_status(ClientType.LEVEL)
            return output_info, output_command, output_status_level

        @staticmethod
        def level_once_finish() -> (str, LevelCommandType):
            output_info = AdminInfoType.I_KEEP_LEVEL_STOP_DONE
            output_status_level = update_ready_status(ClientType.LEVEL)
            output_status_mass = update_ready_status(ClientType.MASS)
            return output_info, [output_status_mass, output_status_level]

        @staticmethod
        def stop_keep_level() -> LevelCommandType:
            return LevellingCommandExecutor.execute(LevelCommandType.STOP)

        @staticmethod
        def start_level_once():
            return LevellingCommandExecutor.execute(LevelCommandType.LEVEL_ONCE)
