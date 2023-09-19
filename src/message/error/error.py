from enum import Enum


class ErrorType(Enum):
    pass


class NetworkErrorType(ErrorType):
    # TODO: change to error code if needed
    ADMIN_DISCONNECT = ""
    LEVEL_DISCONNECT = "L-ERROR-levelling controller disconnects"
    MASS_DISCONNECT = "M-ERROR-moving mass controller disconnects"
    GYRO_DISCONNECT = "G-ERROR-gyro controller disconnects"
    VISION_DISCONNECT = "V-ERROR-vision system disconnects"


class OperationError(ErrorType):
    pass
