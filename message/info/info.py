from enum import Enum


class MassInfoType(Enum):
    MOVE_START = "move"
    MOVE_DONE = "moved"
    STOP_START = "stop"
    STOP_DONE = "stopped"


class LevelInfoType(Enum):
    LEVEL_ONCE_START = "level once start"
    LEVEL_ONCE_DONE = "level once done"
    KEEP_LEVEL_START = "keep level start"
    STOP_START = "stop"
    STOP_DONE = "stopped"


class GyroInfoType(Enum):
    pass