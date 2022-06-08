from enum import Enum


class AdminWarnType(Enum):
    LEVEL_BATTERY_LOW = "A-WARN-inclinometer battery running low, please recharge"


class MassWarnType(Enum):
    pass


class LevelWarnType(Enum):
    pass


class GyroWarnType(Enum):
    pass
