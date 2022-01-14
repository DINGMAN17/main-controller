from enum import Enum


class MassInfoType(Enum):
    MOVE_START = "move"
    MOVE_DONE = "moved"
    STOP_START = "stop"
    STOP_DONE = "stopped"