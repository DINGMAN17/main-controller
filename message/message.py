from enum import Enum


class BaseMessageType(Enum):
    COMMAND = "C"
    DATA = "D"
    INFO = "INFO"
    STATUS = "STATUS"
    ERROR = "ERROR"
    EMERGENCY = "EMERG"
    WARNING = "WARN"


class MessageRecipientType(Enum):
    LEVEL = "L"
    MASS = "M"
    GYRO = "G"
    MULTIPLE = "I"

