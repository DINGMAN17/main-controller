from control.initialisation import Initialisation
from hardware.gyroscope import Gyroscope
from hardware.moving_mass import MovingMass
from hardware.sensors import *
from hardware.winches import Winches


class BaseCommandExecutor:
    pass


class LevellingCommandExecutor(BaseCommandExecutor):
    @staticmethod
    def execute(message, command_queue):
        output = None
        if "initialisation" in message:
            output = LevellingCommandExecutor.initialisation()
        elif "levelonce" in message:
            output = LevellingCommandExecutor.level_once()
        elif "levelauto" in message:
            output = LevellingCommandExecutor.level_auto()
        elif "continue" in message:
            output = LevellingCommandExecutor.level_continue()
        elif "stop" in message:
            output = LevellingCommandExecutor.stop()
        elif "upauto" in message:
            # sample input: CMDLupauto,10
            output = LevellingCommandExecutor.up_auto(message)
        elif "downauto" in message:
            output = LevellingCommandExecutor.down_auto(message)
        elif "downmanual" in message:
            output = LevellingCommandExecutor.down_manual()
        elif "upmanual" in message:
            output = LevellingCommandExecutor.up_manual()
        elif "battery" in message:
            output = LevellingCommandExecutor.check_battery()
        elif "sensor" in message:
            output = LevellingCommandExecutor.request_data()
        elif "count" in message:
            output = LevellingCommandExecutor.request_count()

        if output is not None:
            command_queue.put(output)
            return output
        else:
            raise ValueError("Invalid input" + message)

    @staticmethod
    def stop():
        return Winches.stop()

    @staticmethod
    def up_auto(message):
        distance = int(message.split(",")[-1])
        return Winches.up_auto(distance)

    @staticmethod
    def down_auto(message):
        distance = int(message.split(",")[-1])
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
    def execute(message, command_queue):
        output = None
        if "init" in message:
            output = MassCommandExecutor.init()
        elif "set" in message:
            # CMDMset,X100,Y200
            output = MassCommandExecutor.set_movement(message)
        elif "move" in message:
            output = MassCommandExecutor.move()
        elif "stop" in message:
            output = MassCommandExecutor.stop()
        elif "get" in message:
            output = MassCommandExecutor.get_position()

        if output is not None:
            command_queue.put(output)
            return output
        else:
            raise ValueError("Invalid input" + message)

    @staticmethod
    def init():
        return MovingMass.init()

    @staticmethod
    def set_movement(message):
        pos = message.split(",")[1:]
        return MovingMass.set_movement(pos[0], pos[1])

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
    def execute(message, command_queue):
        output = None
        if "init" in message:
            output = GyroCommandExecutor.init()
        elif "center" in message:
            # CMDMset,X100,Y200
            output = GyroCommandExecutor.center()
        elif "spin" in message:
            output = GyroCommandExecutor.spin()
        elif "stop" in message:
            output = GyroCommandExecutor.stop()
        elif "auto" in message:
            output = GyroCommandExecutor.set_auto()
        elif "zero" in message:
            output = GyroCommandExecutor.set_zero()
        elif "get" in message:
            output = GyroCommandExecutor.get_data()

        if output is not None:
            command_queue.put(output)
            return output
        else:
            raise ValueError("Invalid input" + message)

    @staticmethod
    def init():
        return Gyroscope.init()

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
    def set_auto():
        return Gyroscope.set_auto()

    @staticmethod
    def get_data():
        return Gyro_sensor.get_data()

    @staticmethod
    def set_zero():
        return Gyro_sensor.set_zero()


if __name__ == "__main__":
    MassCommandExecutor.set_movement("CMDMset,X100,Y200")
