class ClientDisconnectException(Exception):
    pass


class SubsystemDisconnectException(ClientDisconnectException):
    pass


class AdminDisconnectException(ClientDisconnectException):
    pass


class OperationalException(Exception):
    pass


class GyroOperationException(OperationalException):
    pass


class LevelOperationException(OperationalException):
    pass


class MassOperationException(OperationalException):
    pass
