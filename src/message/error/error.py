from enum import Enum


class ErrorType(Enum):
    pass


class NetworkErrorType(ErrorType):
    # TODO: change to error code if needed
    ADMIN_DISCONNECT = ""
    LEVEL_DISCONNECT = "A-ERROR-levelling controller disconnects"
    MASS_DISCONNECT = "A-ERROR-moving mass controller disconnects"
    GYRO_DISCONNECT = "A-ERROR-gyro controller disconnects"
    VISION_DISCONNECT = "A-ERROR-vision system disconnects"


class OperationError(ErrorType):
    pass
