from enum import Enum


class BaseMessageType(Enum):
    # TODO: discuss message type for sub-controllers
    COMMAND = "C"
    DATA = "D"
    INFO = "INFO"
    STATUS = "STATUS"
    ERROR = "ERROR"
    EMERGENCY = "EMERG"
    WARNING = "WARN"


class MessageType(Enum):
    COMMAND = "C"
    LEVEL_COMMAND = "CL"
    MASS_COMMAND = "CM"
    GYRO_COMMAND = "CG"
    LEVEL_DATA = "L"
    MASS_DATA = "M"
    GYRO_DATA = "G"


class LevelCommandType(Enum):
    UP_AUTO = "up_a"
    DOWN_AUTO = "down_a"
    UP_MANUAL = "up_m"
    DOWN_MANUAL = "down_m"
    BATTERY = "battery"
    LEVEL_ONCE = "once"
    LEVEL_AUTO = "auto"
    CONTINUE = "continue"
    COUNT = "count"
    STOP = "stop"
    INIT = "init"
    GET = "get"


class MassCommandType(Enum):
    SET = "set"
    MOVE = "move"
    STOP = "stop"
    INIT = "init"
    GET = "get"


class GyroCommandType(Enum):
    CENTER = "center"
    SPIN = "spin"
    AUTO_ON = "auto_on"
    AUTO_OFF = "auto_off"
    ZERO = "zero"
    STOP = "stop"
    GET = "get"
