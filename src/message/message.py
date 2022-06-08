from enum import Enum


class BaseMessageType(Enum):
    COMMAND = "C"
    DATA = "D"
    INFO = "INFO"
    STATUS = "STATUS"
    ERROR = "ERROR"
    EMERGENCY = "EMERGE"
    WARNING = "WARN"
    DEBUG = "DEBUG"


class MessageRecipientType(Enum):
    LEVEL = "L"
    MASS = "M"
    GYRO = "G"
    MULTIPLE = "I"

