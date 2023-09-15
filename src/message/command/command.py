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
    COUNT = "count"
    STOP = "stop"
    INIT = "init"  # no init for 1-ton due to hardware problem
    GET = "get"
    CABLE_INIT = "cable_init"  # for testing only
    STEP = "step"  # move winch individually, follow init command format


class MassCommandType(BaseCommandType):

    SET_MOVE_FAST = "move_fast"
    SET_MOVE_SLOW = "move_slow"
    # manual move 4 directions
    MOVE_AUTO_X_PLUS = "move_x_plus"
    MOVE_AUTO_X_MINUS = "move_x_minus"
    MOVE_AUTO_X_STOP = "move_x_stop"
    MOVE_AUTO_Y_PLUS = "move_y_plus"
    MOVE_AUTO_Y_MINUS = "move_y_minus"
    MOVE_AUTO_Y_STOP = "move_y_stop"
    ANTI_SWAY_ON = "sway_on"
    ANTI_SWAY_OFF = "sway_off"

    SET = "set"  # Y0
    MOVE = "move"
    STOP = "stop"
    INIT = "init"
    GET = "get"


class GyroCommandType(BaseCommandType):
    CENTER = "center"  # busy
    AUTO_ON = "auto_on"
    AUTO_OFF = "auto_off"
    MOVE_CUSTOM_ANGLE = "move_angle"  # A-C-G-move_angle-@_5
    STOP_MOVE_CUSTOM_ANGLE = "move_angle_stop"
    ZERO = "zero"
    STOP = "stop"
    GET = "get"


class IntegrationCommandType(BaseCommandType):
    MOVE_LEVEL = "move_level"  # A-C-I-move_level
    E_STOP = "Estop"
    SYSTEM_CHECK = "check"
