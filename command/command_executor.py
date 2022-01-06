from communication.message import *
from control.initialisation import Initialisation
from hardware.gyroscope import Gyroscope
from hardware.moving_mass import MovingMass
from hardware.sensors import *
from hardware.winches import Winches


class BaseCommandExecutor:
    pass


class LevellingCommandExecutor(BaseCommandExecutor):
    @staticmethod
    def execute(command_type, command, command_queue):
        output = None
        if command_type == LevelCommandType.INIT:
            output = LevellingCommandExecutor.initialisation()
        elif command_type == LevelCommandType.LEVEL_ONCE:
            output = LevellingCommandExecutor.level_once()
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

        if output is not None:
            command_queue.put(output)
        return output

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


class MassCommandExecutor(BaseCommandExecutor):
    @staticmethod
    def execute(command_type, command, command_queue):
        output = None
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

        if output is not None:
            command_queue.put(output)
        return output

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
    @staticmethod
    def execute(command_type, command_queue):
        output = None
        if command_type == GyroCommandType.CENTER:
            output = GyroCommandExecutor.center()
        elif command_type == GyroCommandType.SPIN:
            output = GyroCommandExecutor.spin()
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

        if output is not None:
            command_queue.put(output)
        return output

    @staticmethod
    def stop():
        return Gyroscope.stop()

    @staticmethod
    def spin():
        return Gyroscope.spin()

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


if __name__ == "__main__":
    msg = LevellingCommandExecutor.up_auto("CL-up_a-10")
    print(msg)
