from abc import ABC, abstractmethod

from hardware.sensors import Inclinometer
from hardware.winches import Winches


class BaseCommandExecutor(ABC):
    @abstractmethod
    def stop(self):
        pass


class LevellingCommandExecutor(BaseCommandExecutor):

    def stop(self):
        return Winches.stop()

    def up_auto(self, distance):
        return Winches.up_auto(distance)

    def down_auto(self, distance):
        return Winches.down_auto(distance)

    def down_manual(self):
        return Winches.down_manual()

    def up_manual(self):
        return Winches.up_manual()

    def level_once(self):
        return Winches.level_once()

    def level_auto(self):
        return Winches.level_auto()

    def level_continue(self):
        return Winches.level_continue()

    def check_battery(self):
        return Inclinometer.check_battery()


class GyroCommandExecutor(BaseCommandExecutor):
    pass


class MassCommandExecutor(BaseCommandExecutor):
    pass
