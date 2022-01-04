from enum import Enum


class MessageType(Enum):
    COMMAND = "C"
    LEVEL_DATA = "L"
    MASS_DATA = "M"
    GYRO_DATA = "G"


data_dict = {}
