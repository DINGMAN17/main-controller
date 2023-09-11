from typing import Tuple, Optional

from src.communication.client import ClientStatus, ClientType
from src.message.command.command import LevelCommandType, IntegrationCommandType
from src.message.command.command_executor import LevellingCommandExecutor, Command
from src.message.info.info import MassInfoType, AdminInfoType, LevelInfoType, GyroInfoType, BaseInfoType


def update_ready_status(client: ClientType) -> Tuple[ClientType, ClientStatus]:
    return client, ClientStatus.READY


class BaseInfoExecutor:
    def __init__(self):
        self._msg_components: Optional[list] = None
        self._info_type: Optional[BaseInfoType] = None
        self.output_dict = dict()
        self._output_info_msg: Optional[str] = None
        self._output_info_type: Optional[AdminInfoType] = None
        self._output_status: list = []

    @property
    def msg_components(self):
        return self._msg_components

    @msg_components.setter
    def msg_components(self, message):
        self._msg_components = message

    @property
    def info_type(self):
        return self._info_type

    @info_type.setter
    def info_type(self, info_type):
        self._info_type = info_type

    def reset(self, info_type, msg_components=None):
        self.info_type = info_type
        self.msg_components = msg_components
        self.output_dict = dict()
        self._output_status = []
        self._output_info_type = self._output_info_msg = None

    def update_outputs(self):
        if self._output_info_type is not None:
            self.output_dict["info_type"] = self._output_info_type
        if self._output_status:
            self.output_dict["status"] = self._output_status


class MassInfoExecutor(BaseInfoExecutor):
    def __init__(self):
        super().__init__()

    def execute(self):
        if self._info_type == MassInfoType.MOVE_DONE:
            self.move_finish()
        elif self._info_type == MassInfoType.MOVE_IN_PROGRESS:
            self.move_in_progress()
        elif self._info_type == MassInfoType.MOVE_HOME:
            self.move_home()
        elif self._info_type == MassInfoType.STOP_DONE:
            self.stop_finish()
        elif self._info_type == MassInfoType.SET_DONE:
            self.set_pos_finish()
        elif self._info_type == MassInfoType.ANTI_SWAY_ON_DONE:
            self.anti_sway_on_finish()
        elif self._info_type == MassInfoType.ANTI_SWAY_OFF_DONE:
            self.anti_sway_off_finish()
        elif self._info_type == MassInfoType.MOVE_ANTI_SWAY_AUTO_DONE:
            self.anti_sway_auto_done()
        self.update_outputs()
        return self.output_dict

    def set_pos_finish(self):
        self._output_info_type = AdminInfoType.M_POS_DONE
        self._output_status.append(update_ready_status(ClientType.MASS))

    def move_finish(self):
        self._output_info_type = AdminInfoType.M_MOVE_DONE
        self._output_status.append(update_ready_status(ClientType.MASS))

    def move_in_progress(self):
        self._output_info_type = AdminInfoType.M_MOVE_IN_PROGRESS

    def stop_finish(self):
        self._output_info_type = AdminInfoType.M_STOP_DONE
        self._output_status.append(update_ready_status(ClientType.MASS))

    def anti_sway_on_finish(self):
        self._output_info_type = AdminInfoType.M_ANTISWAY_ON

    def anti_sway_off_finish(self):
        self._output_info_type = AdminInfoType.M_ANTISWAY_OFF
        self._output_status.append(update_ready_status(ClientType.MASS))

    def move_home(self):
        self._output_info_type = AdminInfoType.M_MOVE_HOME
        # self._output_status.append(update_ready_status(ClientType.MASS))

    def anti_sway_auto_done(self):
        self._output_info_type = AdminInfoType.M_ANTISWAY_AUTO_FINISH


class LevelInfoExecutor(BaseInfoExecutor):
    LOW_BATTERY_LEVEL = 3

    def __init__(self):
        super().__init__()

    def execute(self) -> dict:
        if self._info_type == LevelInfoType.LEVEL_DONE:
            self.level_finish()
        elif self._info_type == LevelInfoType.STOP_DONE:
            self.stop_finish()
        elif self._info_type == LevelInfoType.AUTO_MOVE_DONE:
            self.auto_move_finish()
        elif self._info_type == LevelInfoType.BATTERY:
            self.show_battery()
        elif self._info_type == LevelInfoType.INIT_DONE:
            self.init_finish()
        elif self._info_type == LevelInfoType.CABLE_INIT_DONE:
            self.cable_init_finish()
        elif self._info_type == LevelInfoType.AUTO_LEVEL_ON:
            self.auto_level_on()
        elif self._info_type == LevelInfoType.MANUAL_MOVE_DONE:
            self.manual_move_done()
        self.update_outputs()
        if self._output_info_msg is not None:
            self.output_dict['info_msg'] = self._output_info_msg
        return self.output_dict

    def show_battery(self):
        battery_level = int(self.msg_components[-1])
        if battery_level <= self.LOW_BATTERY_LEVEL:
            output_info_type = AdminInfoType.L_BATTERY_LOW
        else:
            output_info_type = AdminInfoType.L_BATTERY_ENOUGH
        self._output_info_type = output_info_type
        self._output_info_msg = output_info_type.value.strip() + str(battery_level) + "\n"

    def level_finish(self):
        self._output_info_type = AdminInfoType.L_LEVEL_DONE
        self._output_status.append(update_ready_status(ClientType.LEVEL))

    def stop_finish(self):
        self._output_info_type = AdminInfoType.L_STOP_DONE
        self._output_status.append(update_ready_status(ClientType.LEVEL))

    def auto_move_finish(self):
        self._output_info_type = AdminInfoType.L_MOVE_DONE
        self._output_status.append(update_ready_status(ClientType.LEVEL))

    def init_finish(self):
        self._output_info_type = AdminInfoType.L_INIT_DONE
        self._output_status.append(update_ready_status(ClientType.LEVEL))

    def cable_init_finish(self):
        self._output_info_type = AdminInfoType.L_CABLE_INIT_DONE
        self._output_status.append(update_ready_status(ClientType.LEVEL))

    def auto_level_on(self):
        self._output_info_type = AdminInfoType.L_AUTO_LEVEL_ON
        self._output_status.append(update_ready_status(ClientType.LEVEL))

    def manual_move_done(self):
        self._output_info_type = AdminInfoType.L_MANUAL_MOVE_DONE


class GyroInfoExecutor(BaseInfoExecutor):
    def __init__(self):
        super().__init__()

    def execute(self) -> dict:
        if self._info_type == GyroInfoType.ZERO_DONE:
            self.zero_finish()
        elif self._info_type == GyroInfoType.STOP_DONE:
            self.stop_finish()
        elif self._info_type == GyroInfoType.AUTO_ON_DONE:
            self.auto_on_finish()
        elif self._info_type == GyroInfoType.AUTO_OFF_DONE:
            self.auto_off_finish()
        elif self._info_type == GyroInfoType.CENTER_DONE:
            self.center_finish()
        elif self._info_type == GyroInfoType.AUTO_ANGLE_ON:
            self.auto_angle_on()
        elif self._info_type == GyroInfoType.AUTO_ANGLE_OFF:
            self.auto_angle_off()
        self.update_outputs()
        return self.output_dict

    def zero_finish(self):
        self._output_info_type = AdminInfoType.G_ZERO_DONE
        self._output_status.append(update_ready_status(ClientType.GYRO))

    def stop_finish(self):
        self._output_info_type = AdminInfoType.G_STOP_DONE
        self._output_status.append(update_ready_status(ClientType.GYRO))

    def auto_on_finish(self):
        self._output_info_type = AdminInfoType.G_AUTO_ON_DONE
        self._output_status.append(update_ready_status(ClientType.GYRO))

    def auto_off_finish(self):
        self._output_info_type = AdminInfoType.G_AUTO_OFF_DONE
        self._output_status.append(update_ready_status(ClientType.GYRO))

    def center_finish(self):
        self._output_info_type = AdminInfoType.G_CENTER_DONE
        self._output_status.append(update_ready_status(ClientType.GYRO))

    def auto_angle_off(self):
        self._output_info_type = AdminInfoType.G_AUTO_ANGLE_DONE
        self._output_status.append(update_ready_status(ClientType.GYRO))

    def auto_angle_on(self):
        self._output_info_type = AdminInfoType.G_AUTO_ANGLE_ON
        self._output_status.append(update_ready_status(ClientType.GYRO))


class IntegratedInfoExecutor(BaseInfoExecutor):

    def __init__(self):
        super().__init__()
        self._integrated_command = None
        self._output_command: Optional[Command] = None

    @property
    def integrated_command(self):
        return self._integrated_command

    @integrated_command.setter
    def integrated_command(self, command):
        self._integrated_command = command

    def reset(self, info_type, msg_components=None):
        super(IntegratedInfoExecutor, self).reset(info_type, msg_components)
        self._output_command = None

    def update_outputs(self):
        super(IntegratedInfoExecutor, self).update_outputs()
        if self._output_status:
            if not isinstance(self._output_status, list):
                self._output_status = [self._output_status]
            self.output_dict['status'] = self._output_status
        if self._output_command is not None:
            if not isinstance(self._output_command, list):
                self._output_command = [self._output_command]
            self.output_dict['command'] = self._output_command

    # only mass move implemented
    def execute(self):
        if self.integrated_command == IntegrationCommandType.MOVE_LEVEL:
            self._output_info_type, self._output_command, self._output_status = IntegratedInfoExecutor.MassMoveInfo.execute(
                self.info_type)
        self.update_outputs()
        return self.output_dict

    class MassMoveInfo:

        @staticmethod
        def execute(info_type: BaseInfoType):
            output_info = output_command = output_status = None
            if info_type == MassInfoType.MOVE_DONE:
                output_info, output_command = IntegratedInfoExecutor.MassMoveInfo.move_finish()
            elif info_type == MassInfoType.STOP_DONE:
                output_info, output_command = IntegratedInfoExecutor.MassMoveInfo.stop_finish()
            elif info_type == LevelInfoType.STOP_DONE:
                output_info, output_command = IntegratedInfoExecutor.MassMoveInfo.keep_level_stop_finish()
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
        def stop_finish():
            output_command = IntegratedInfoExecutor.MassMoveInfo.stop_keep_level()
            output_info = AdminInfoType.I_MASS_STOP_DONE
            return output_info, output_command

        @staticmethod
        def keep_level_stop_finish():
            output_command = IntegratedInfoExecutor.MassMoveInfo.start_level_once()
            output_info = AdminInfoType.I_KEEP_LEVEL_STOP_DONE
            return output_info, output_command

        @staticmethod
        def level_once_finish():
            output_info = AdminInfoType.I_LEVEL_ONCE_DONE
            output_status_level = update_ready_status(ClientType.LEVEL)
            output_status_mass = update_ready_status(ClientType.MASS)
            return output_info, [output_status_mass, output_status_level]

        @staticmethod
        def stop_keep_level():
            level_command_executor = LevellingCommandExecutor()
            level_command_executor.command_type = LevelCommandType.STOP
            level_command_executor.execute()
            return level_command_executor.command_to_send[0]

        @staticmethod
        def start_level_once():
            level_command_executor = LevellingCommandExecutor()
            level_command_executor.command_type = LevelCommandType.LEVEL_ONCE
            level_command_executor.execute()
            return level_command_executor.command_to_send[0]
