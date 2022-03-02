from enum import Enum


class BaseCommandType(Enum):
    pass


class LevelCommandType(BaseCommandType):
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
    INIT = "init"  # no init for 1-ton due to hardware problem
    GET = "get"
    MOVE = "move"  # for testing only
    CABLE_INIT = "cable_init"  # for testing only
    STEP = "step"  # move winch individually, follow init command format


class MassCommandType(BaseCommandType):
    SET = "set"
    MOVE = "move"
    STOP = "stop"
    INIT = "init"
    GET = "get"


class GyroCommandType(BaseCommandType):
    CENTER = "center"  # busy
    AUTO_ON = "auto_on"
    AUTO_OFF = "auto_off"
    ZERO = "zero"
    STOP = "stop"
    GET = "get"


class IntegrationCommandType(BaseCommandType):
    MOVE_LEVEL = "move_level"  # A-C-I-move_level
    E_STOP = "Estop"
    SYSTEM_CHECK = "check"
