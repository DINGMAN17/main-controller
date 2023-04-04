class UnknownClientException(ValueError):
    pass


class IntendedClientDoesNotExistException(Exception):
    pass


class IntendedClientIsNotConnectedException(Exception):
    pass


class NotValidSubsystemException(Exception):
    pass


class SendCommandStatusCheckFailException(Exception):
    pass
