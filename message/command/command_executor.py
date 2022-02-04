from typing import List

from control.initialisation import Initialisation
from hardware.gyroscope import Gyroscope
from hardware.moving_mass import MovingMass
from hardware.sensors import *
from hardware.winches import Winches
from message.command.command import *


class BaseCommandExecutor:
    pass


class LevellingCommandExecutor(BaseCommandExecutor):
    busy_command_list = [LevelCommandType.LEVEL_AUTO, LevelCommandType.LEVEL_ONCE, LevelCommandType.CABLE_INIT,
                         LevelCommandType.UP_AUTO, LevelCommandType.DOWN_AUTO]

    @staticmethod
    def execute(command_type, command=None):
        output = None
        command_to_send = None
        if command_type == LevelCommandType.INIT:
            output = LevellingCommandExecutor.initialisation()
        elif command_type == LevelCommandType.LEVEL_ONCE:
            output = LevellingCommandExecutor.level_once()
        elif command_type == LevelCommandType.STATUS:
            output = LevellingCommandExecutor.check_status()
        elif command_type == LevelCommandType.LEVEL_AUTO:
            output = LevellingCommandExecutor.level_auto()
        elif command_type == LevelCommandType.CONTINUE:
            output = LevellingCommandExecutor.level_continue()
        elif command_type == LevelCommandType.STOP:
            output = LevellingCommandExecutor.stop()
        elif command_type == LevelCommandType.UP_AUTO:
            output = LevellingCommandExecutor.up_auto(command)
        elif command_type == LevelCommandType.DOWN_AUTO:
            output = LevellingCommandExecutor.down_auto(command)
        elif command_type == LevelCommandType.DOWN_MANUAL:
            output = LevellingCommandExecutor.down_manual()
        elif command_type == LevelCommandType.UP_MANUAL:
            output = LevellingCommandExecutor.up_manual()
        elif command_type == LevelCommandType.BATTERY:
            output = LevellingCommandExecutor.check_battery()
        elif command_type == LevelCommandType.GET:
            output = LevellingCommandExecutor.request_data()
        elif command_type == LevelCommandType.COUNT:
            output = LevellingCommandExecutor.request_count()
        elif command_type == LevelCommandType.MOVE:  # for testing only
            output = LevellingCommandExecutor.move()
        elif command_type == LevelCommandType.CABLE_INIT:
            output = LevellingCommandExecutor.cable_init()
        elif command_type == LevelCommandType.STEP:
            output = LevellingCommandExecutor.step(command)

        busy_command = True if command_type in LevellingCommandExecutor.busy_command_list else False
        if output is not None:
            recipient = ClientType.LEVEL
            command_to_send = Command(command_type, recipient, busy_command)
            command_to_send.set_value(output)
        return command_to_send

    @staticmethod
    def stop():
        return Winches.stop()

    @staticmethod
    def up_auto(command):
        # sample input: CL-up_a-10
        distance = int(command[-1])
        return Winches.up_auto(distance)

    @staticmethod
    def down_auto(command):
        distance = int(command[-1])
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
    def level_continue():
        return Winches.level_continue()

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
    def move():
        return Winches.move()

    @staticmethod
    def cable_init():
        return Winches.cable_init()

    @staticmethod
    def step(command):
        return "Linit20" + command[-1] + "\n"

    @staticmethod
    def check_status():
        return Winches.check_status()


class MassCommandExecutor(BaseCommandExecutor):
    busy_command_list = [MassCommandType.MOVE, MassCommandType.INIT]

    @staticmethod
    def execute(command_type, command=None):
        output = None
        command_to_send = None
        if command_type == MassCommandType.INIT:
            output = MassCommandExecutor.init()
        elif command_type == MassCommandType.SET:
            output = MassCommandExecutor.set_position(command)
        elif command_type == MassCommandType.MOVE:
            output = MassCommandExecutor.move()
        elif command_type == MassCommandType.STOP:
            output = MassCommandExecutor.stop()
        elif command_type == MassCommandType.GET:
            output = MassCommandExecutor.get_position()

        busy_command = True if command_type in MassCommandExecutor.busy_command_list else False
        if output is not None:
            recipient = ClientType.MASS
            command_to_send = Command(command_type, recipient, busy_command)
            command_to_send.set_value(output)
        return command_to_send

    @staticmethod
    def init():
        return MovingMass.init()

    @staticmethod
    def set_position(command):
        # sample command: CM-set-X100,Y200
        position = command[-1].split(",")
        return MovingMass.set_movement(position[0], position[1])

    @staticmethod
    def move():
        return MovingMass.move()

    @staticmethod
    def stop():
        return MovingMass.stop()

    @staticmethod
    def get_position():
        return MovingMassPos.get_position()


class GyroCommandExecutor(BaseCommandExecutor):
    busy_command_list = [GyroCommandType.ZERO]

    @staticmethod
    def execute(command_type):
        output = None
        command_to_send = None
        if command_type == GyroCommandType.CENTER:
            output = GyroCommandExecutor.center()
        elif command_type == GyroCommandType.STOP:
            output = GyroCommandExecutor.stop()
        elif command_type == GyroCommandType.AUTO_ON:
            output = GyroCommandExecutor.on_auto()
        elif command_type == GyroCommandType.AUTO_OFF:
            output = GyroCommandExecutor.off_auto()
        elif command_type == GyroCommandType.ZERO:
            output = GyroCommandExecutor.set_zero()
        elif command_type == GyroCommandType.GET:
            output = GyroCommandExecutor.get_data()

        busy_command = True if command_type in GyroCommandExecutor.busy_command_list else False
        if output is not None:
            recipient = ClientType.GYRO
            command_to_send = Command(command_type, recipient, busy_command)
            command_to_send.set_value(output)
        return command_to_send

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
    def get_data():
        return Gyro_sensor.get_data()

    @staticmethod
    def set_zero():
        return Gyro_sensor.set_zero()


class IntegrationCommandExecutor(BaseCommandExecutor):
    @staticmethod
    def execute(command_type):
        output = None
        if command_type == IntegrationCommandType.MOVE_LEVEL:
            output = IntegrationCommandExecutor.move_level()
        elif command_type == IntegrationCommandType.SYSTEM_CHECK:
            output = IntegrationCommandExecutor.system_check()
        return output

    @staticmethod
    def move_level() -> List[Command]:
        mass_command = MassCommandExecutor.execute(MassCommandType.MOVE)
        level_command = LevellingCommandExecutor.execute(LevelCommandType.LEVEL_AUTO)
        return [mass_command, level_command]

    @staticmethod
    def system_check():
        # TODO: confirm system check commands
        return ""


if __name__ == "__main__":
    msg = IntegrationCommandExecutor.execute(IntegrationCommandType.MOVE_LEVEL)
    command_list = msg.split("\n")
    new_list = [command_list.append(cmd + "\n") for cmd in command_list]
    print(command_list)
