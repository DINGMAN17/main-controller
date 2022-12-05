from dataclasses import dataclass
from typing import Optional, List

from src.communication.client import ClientType
from src.control.initialisation import Initialisation
from src.hardware.gyroscope import Gyroscope
from src.hardware.moving_mass import MovingMass
from src.hardware.sensors import Gyro_sensor, MovingMassPos, Inclinometer
from src.hardware.winches import Winches
from src.message.command.command import *


@dataclass(frozen=True)
class Command:
    command_type: BaseCommandType
    recipient: ClientType
    value: str
    busy_command: bool
    lock_system: bool


class BaseCommandExecutor:
    def __init__(self):
        self._command_type: Optional[BaseCommandType] = None
        self._command_to_send: Optional[List[Command]] = None

    @property
    def command_type(self):
        return self._command_type

    @command_type.setter
    def command_type(self, command_type):
        self._command_type = command_type

    @property
    def command_to_send(self):
        return self._command_to_send

    @command_to_send.setter
    def command_to_send(self, command_to_send):
        self._command_to_send = command_to_send

    def execute(self):
        output_msg = self.get_output_message()
        self.create_command(output_msg)

    def get_output_message(self):
        pass

    def create_command(self, output_msg):
        pass


class LevellingCommandExecutor(BaseCommandExecutor):
    BUSY_COMMAND_LIST = [LevelCommandType.LEVEL_AUTO, LevelCommandType.LEVEL_ONCE, LevelCommandType.CABLE_INIT,
                         LevelCommandType.UP_AUTO, LevelCommandType.DOWN_AUTO]

    def __init__(self):
        super().__init__()
        self._command_value: Optional[str] = None

    @property
    def command_value(self):
        return self._command_value

    @command_value.setter
    def command_value(self, value: str):
        self._command_value = value

    def create_command(self, output_msg):
        busy_command = True if self.command_type in LevellingCommandExecutor.BUSY_COMMAND_LIST else False
        lock_system = True if self.command_type == LevelCommandType.STOP else False
        if output_msg is not None:
            recipient = ClientType.LEVEL
            self.command_to_send = [Command(self.command_type, recipient, output_msg, busy_command, lock_system)]

    def get_output_message(self):
        output_msg = None
        if self.command_type == LevelCommandType.INIT:
            output_msg = LevellingCommandExecutor.initialisation()
        elif self.command_type == LevelCommandType.LEVEL_ONCE:
            output_msg = LevellingCommandExecutor.level_once()
        elif self.command_type == LevelCommandType.STATUS:
            output_msg = LevellingCommandExecutor.check_status()
        elif self.command_type == LevelCommandType.LEVEL_AUTO:
            output_msg = LevellingCommandExecutor.level_auto()
        elif self.command_type == LevelCommandType.STOP:
            output_msg = LevellingCommandExecutor.stop()
        elif self.command_type == LevelCommandType.UP_AUTO:
            output_msg = LevellingCommandExecutor.up_auto(self.command_value)
        elif self.command_type == LevelCommandType.DOWN_AUTO:
            output_msg = LevellingCommandExecutor.down_auto(self.command_value)
        elif self.command_type == LevelCommandType.DOWN_MANUAL:
            output_msg = LevellingCommandExecutor.down_manual()
        elif self.command_type == LevelCommandType.UP_MANUAL:
            output_msg = LevellingCommandExecutor.up_manual()
        elif self.command_type == LevelCommandType.BATTERY:
            output_msg = LevellingCommandExecutor.check_battery()
        elif self.command_type == LevelCommandType.GET:
            output_msg = LevellingCommandExecutor.request_data()
        elif self.command_type == LevelCommandType.COUNT:
            output_msg = LevellingCommandExecutor.request_count()
        elif self.command_type == LevelCommandType.CABLE_INIT:
            output_msg = LevellingCommandExecutor.cable_init()
        elif self.command_type == LevelCommandType.STEP:
            output_msg = LevellingCommandExecutor.step(self.command_value)
        return output_msg

    @staticmethod
    def stop():
        return Winches.stop()

    @staticmethod
    def up_auto(distance):
        # sample input: C-L-up_a-10
        distance = int(distance)
        return Winches.up_auto(distance)

    @staticmethod
    def down_auto(distance):
        distance = int(distance)
        return Winches.down_auto(distance)

    @staticmethod
    def down_manual():
        return Winches.down_manual()

    @staticmethod
    def up_manual():
        return Winches.up_manual()

    @staticmethod
    def level_once():
        return Winches.level_once()

    @staticmethod
    def level_auto():
        return Winches.level_auto()

    @staticmethod
    def request_count():
        return Winches.get_count()

    @staticmethod
    def check_battery():
        return Inclinometer.check_battery()

    @staticmethod
    def request_data():
        return Inclinometer.request_data()

    @staticmethod
    def initialisation(ppvc_type="1ton_prototype", pulley_num=6):
        ppvc_init = Initialisation(ppvc_type, pulley_num)
        return ppvc_init.run()

    @staticmethod
    def cable_init():
        return Winches.cable_init()

    @staticmethod
    def step(value):
        return "Linit20" + value + "\n"

    @staticmethod
    def check_status():
        return Winches.check_status()


class MassCommandExecutor(BaseCommandExecutor):
    #TODO: add busy command finish messages
    BUSY_COMMAND_LIST = [MassCommandType.MOVE, MassCommandType.SET]

    def __init__(self):
        super().__init__()
        self._command_value: Optional[str] = None

    @property
    def command_value(self):
        return self._command_value

    @command_value.setter
    def command_value(self, value: str):
        self._command_value = value

    def create_command(self, output_msg):
        busy_command = True if self.command_type in MassCommandExecutor.BUSY_COMMAND_LIST else False
        lock_system = True if self.command_type == MassCommandType.STOP else False
        if output_msg is not None:
            recipient = ClientType.MASS
            self.command_to_send = [Command(self.command_type, recipient, output_msg, busy_command, lock_system)]

    def get_output_message(self):
        output = None
        if self.command_type == MassCommandType.SET:
            output = MassCommandExecutor.set_position(self.command_value)
        elif self.command_type == MassCommandType.MOVE:
            output = MassCommandExecutor.auto_move()
        elif self.command_type == MassCommandType.STOP:
            output = MassCommandExecutor.stop()
        elif self.command_type == MassCommandType.GET:
            output = MassCommandExecutor.get_position()
        elif self.command_type == MassCommandType.MOVE_AUTO_X_PLUS:
            output = MassCommandExecutor.manual_move_X_positive()
        elif self.command_type == MassCommandType.MOVE_AUTO_X_MINUS:
            output = MassCommandExecutor.manual_move_X_negative()
        elif self.command_type == MassCommandType.MOVE_AUTO_Y_PLUS:
            output = MassCommandExecutor.manual_Move_Y_positive()
        elif self.command_type == MassCommandType.MOVE_AUTO_Y_MINUS:
            output = MassCommandExecutor.manual_Move_Y_negative()
        elif self.command_type == MassCommandType.MOVE_AUTO_X_STOP:
            output = MassCommandExecutor.manual_Move_X_stop()
        elif self.command_type == MassCommandType.MOVE_AUTO_Y_STOP:
            output = MassCommandExecutor.manual_Move_Y_stop()
        return output

    @staticmethod
    def set_position(value):
        # sample command: A-C-M-set-X100,Y200
        position = value.split(",")
        return MovingMass.set_movement(position[0], position[1])

    @staticmethod
    def auto_move():
        return MovingMass.move()

    @staticmethod
    def stop():
        return MovingMass.stop()

    @staticmethod
    def get_position():
        return MovingMassPos.get_position()

    @staticmethod
    def manual_move_X_positive():
        return "Mass_JogXPlus\n"

    @staticmethod
    def manual_move_X_negative():
        return "Mass_JogXMinus\n"

    @staticmethod
    def manual_Move_X_stop():
        return "Mass_JogXStop\n"

    @staticmethod
    def manual_Move_Y_positive():
        return "Mass_JogYPlus\n"

    @staticmethod
    def manual_Move_Y_negative():
        return "Mass_JogYMinus\n"

    @staticmethod
    def manual_Move_Y_stop():
        return "Mass_JogYStop\n"


class GyroCommandExecutor(BaseCommandExecutor):

    busy_command_list = [GyroCommandType.ZERO, GyroCommandType.AUTO_ON, GyroCommandType.AUTO_OFF]

    def __init__(self):
        super().__init__()
        self._command_value: Optional[str] = None

    @property
    def command_value(self):
        return self._command_value

    @command_value.setter
    def command_value(self, value: str):
        self._command_value = value

    def create_command(self, output):
        busy_command = True if self.command_type in GyroCommandExecutor.busy_command_list else False
        lock_system = True if self.command_type == GyroCommandType.STOP else False
        if output is not None:
            recipient = ClientType.GYRO
            self.command_to_send = [Command(self.command_type, recipient, output, busy_command, lock_system)]

    def get_output_message(self):
        output = None
        if self.command_type == GyroCommandType.CENTER:
            output = GyroCommandExecutor.center()
        elif self.command_type == GyroCommandType.STOP:
            output = GyroCommandExecutor.stop()
        elif self.command_type == GyroCommandType.AUTO_ON:
            output = GyroCommandExecutor.on_auto()
        elif self.command_type == GyroCommandType.AUTO_OFF:
            output = GyroCommandExecutor.off_auto()
        elif self.command_type == GyroCommandType.MOVE_CUSTOM_ANGLE:
            output = GyroCommandExecutor.move_custom_angle(self.command_value)
        elif self.command_type == GyroCommandType.STOP_MOVE_CUSTOM_ANGLE:
            output = GyroCommandExecutor.stop_custom_angle()
        elif self.command_type == GyroCommandType.ZERO:
            output = GyroCommandExecutor.set_zero()
        elif self.command_type == GyroCommandType.GET:
            output = GyroCommandExecutor.get_data()
        return output

    @staticmethod
    def stop():
        return Gyroscope.stop()

    @staticmethod
    def center():
        return Gyroscope.center()

    @staticmethod
    def on_auto():
        return Gyroscope.on_auto()

    @staticmethod
    def off_auto():
        return Gyroscope.off_auto()

    @staticmethod
    def move_custom_angle(angle):
        return Gyroscope.move_angle(angle)

    @staticmethod
    def stop_custom_angle():
        return Gyroscope.move_angle_stop()

    @staticmethod
    def get_data():
        return Gyro_sensor.get_data()

    @staticmethod
    def set_zero():
        return Gyro_sensor.set_zero()


class IntegrationCommandExecutor(BaseCommandExecutor):
    # TODO: consider how to stop integrated process

    def __init__(self):
        super().__init__()

    def execute(self):
        if self.command_type == IntegrationCommandType.MOVE_LEVEL:
            self.command_to_send = IntegrationCommandExecutor.move_level()
        elif self.command_type == IntegrationCommandType.E_STOP:
            self.command_to_send = IntegrationCommandExecutor.E_stop()
        elif self.command_type == IntegrationCommandType.SYSTEM_CHECK:
            self.command_to_send = IntegrationCommandExecutor.system_check()

    @staticmethod
    def move_level() -> List[Command]:
        mass_executor = MassCommandExecutor()
        mass_executor.command_type = MassCommandType.MOVE
        mass_executor.execute()
        level_executor = LevellingCommandExecutor()
        level_executor.command_type = LevelCommandType.LEVEL_AUTO
        level_executor.execute()
        return mass_executor.command_to_send + level_executor.command_to_send

    @staticmethod
    def E_stop() -> List[Command]:
        pass
        # mass_cmd = MassCommandExecutor.execute(MassCommandType.STOP)
        # level_cmd = LevellingCommandExecutor.execute(LevelCommandType.STOP)
        # gyro_cmd = GyroCommandExecutor.execute(GyroCommandType.STOP)
        # return [mass_cmd, level_cmd, gyro_cmd]

    @staticmethod
    def system_check():
        # TODO: confirm system check commands
        return ""
