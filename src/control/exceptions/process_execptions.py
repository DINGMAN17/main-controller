class UnknownClientException(ValueError):
    pass


class IntendedClientDoesNotExistException(Exception):
    pass


class IntendedClientIsNotConnectedException(Exception):
    pass


class NotValidSubsystemException(Exception):
    pass


class SubsystemDisconnectException(Exception):
    pass


class ClientDisconnectException(Exception):
    pass


class AdminDisconnectException(ClientDisconnectException):
    pass


class SendCommandStatusCheckFailException(ClientDisconnectException):
    pass
