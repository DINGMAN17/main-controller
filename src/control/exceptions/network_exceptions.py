class SubsystemDisconnectException(Exception):
    pass


class ClientDisconnectException(Exception):
    pass


class AdminDisconnectException(ClientDisconnectException):
    pass
