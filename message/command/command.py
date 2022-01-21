from enum import Enum


class Command:
    def __init__(self, command_type, recipient, busy_command=False):
        self.command_type = command_type
        self.recipient = recipient
        self.busy_command = busy_command
        self.value = None

    def set_value(self, value):
        self.value = value


class LevelCommandType(Enum):
    UP_AUTO = "up_a"
    DOWN_AUTO = "down_a"
    UP_MANUAL = "up_m"
    DOWN_MANUAL = "down_m"
    BATTERY = "battery"
    STATUS = "status"
    LEVEL_ONCE = "once"
    LEVEL_AUTO = "auto"
    CONTINUE = "continue"
    COUNT = "count"
    STOP = "stop"
    INIT = "init"
    GET = "get"
    MOVE = "move"  # for testing only
    CABLE_INIT = "cable_init"  # for testing only
    STEP = "step"  # move winch individually, follow init command format


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


class IntegrationCommandType(Enum):
    MOVE_LEVEL = "move_level"  # A-C-I-move_level
    SYSTEM_CHECK = "check"
