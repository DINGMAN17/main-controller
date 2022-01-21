import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class LogMessage:

    @staticmethod
    def add_client(client_name, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("%s is added", client_name)

    @staticmethod
    def wrong_client(log_name="error"):
        log = logging.getLogger(log_name)
        err = "ERROR: wrong client type"
        log.exception(err)
        return err

    @staticmethod
    def disconnect(client_name=None, log_name="main"):
        log = logging.getLogger(log_name)
        if client_name is None:
            client_name = "Unidentified client"
        log.exception("%s is disconnected from server", client_name)

    @staticmethod
    def bad_request(data="", log_name="error"):
        log = logging.getLogger(log_name)
        err = "ERROR: bad request/format" + data
        log.exception(err)
        return err

    @staticmethod
    def wrong_command(message, log_name="error"):
        log = logging.getLogger(log_name)
        log.exception("wrong command %s", message)

    @staticmethod
    def send_command(command, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("command sent to sub-controller: %s", command)

    @staticmethod
    def remove_user(log_name="main"):
        log = logging.getLogger(log_name)
        log.info("Connection error while sending data to user, remove user from list")

    @staticmethod
    def send_to_user(data, log_name="main"):
        log = logging.getLogger(log_name)
        log.info("sent to user-%s", data)

    @staticmethod
    def receive_data(data, log_name="data"):
        log = logging.getLogger(log_name)
        log.info("sensor data-%s", data)
